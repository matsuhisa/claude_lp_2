#!/usr/bin/env python3
"""
brand.css の CSS カスタムプロパティを、Figmaの Variables Import/Export 機能が
読み込める "<Mode名>.tokens.json" 形式(W3C Design Tokens 準拠 + com.figma.* 拡張)
に変換する。

使い方:
  python3 generate_tokens.py \
    --input <brand.cssのパス> \
    --output "<出力先>/Mode 1.tokens.json" \
    --groups Color,Spacing \
    --mode-name "Mode 1"

--groups に渡せる値(カンマ区切り、大小文字区別なし):
  Color, Spacing, Radius, "Border Width", "Font Size", "Font Family", Font

未対応(常にスキップし、理由つきで一覧表示):
  - elevation-*(box-shadowの複合値。Figma変数の単純な型で表現できないため)
  - radius-full のような px 以外の単位(%, em など)を持つ値
"""

import argparse
import json
import re
import struct
import sys

# (prefix, Figmaコレクション名, 型, 単位) — 先頭一致は上から順に判定するため、
# より具体的なprefixを先に置くこと(例: font-size- は font- より先)。
GROUP_RULES = [
    ("font-family-", "Font Family", "string", None),
    ("font-size-", "Font Size", "number", "px"),
    ("border-width-", "Border Width", "number", "px"),
    ("color-", "Color", "color", None),
    ("spacing-", "Spacing", "number", "px"),
    ("radius-", "Radius", "number", "px"),
    ("font-", "Font", "number", "px"),  # font-heading-1 などのセマンティックトークン(var()参照が多い)
]

CUSTOM_PROP_RE = re.compile(r"--([a-zA-Z0-9-]+)\s*:\s*([^;]+);(.*)")
VAR_REF_RE = re.compile(r"^var\(--([a-zA-Z0-9-]+)\)$")
HEX_RE = re.compile(r"^#([0-9a-fA-F]{6})$")
PX_RE = re.compile(r"^(-?\d+(?:\.\d+)?)px$")


def f32(x):
    return struct.unpack("f", struct.pack("f", x))[0]


def hex_to_components(hexcode):
    h = hexcode.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return [f32(r), f32(g), f32(b)]


def classify(name):
    for prefix, group, type_, unit in GROUP_RULES:
        if name.startswith(prefix):
            return group, type_, unit
    return None, None, None


def parse_brand_css(path):
    """--name: value; の一覧を { name: {value, group, type, unit, is_todo} } で返す。"""
    text = open(path, encoding="utf-8").read()
    tokens = {}
    for line in text.splitlines():
        m = CUSTOM_PROP_RE.search(line)
        if not m:
            continue
        name, raw_value, trailing = m.group(1), m.group(2).strip(), m.group(3)
        group, type_, unit = classify(name)
        is_todo = "TODO" in trailing
        tokens[name] = {
            "raw": raw_value,
            "group": group,
            "type": type_,
            "unit": unit,
            "is_todo": is_todo,
        }
    return tokens


def build_entry(name, info, tokens):
    """1トークン分の $type/$value/$extensions を組み立てる。解決不能ならNoneを返す。"""
    raw = info["raw"]

    # var(--x) 参照はFigmaのエイリアス記法 {Group.token} に変換する
    m = VAR_REF_RE.match(raw)
    if m:
        ref_name = m.group(1)
        ref = tokens.get(ref_name)
        if ref is None or ref["group"] is None:
            return None, f"参照先 --{ref_name} を解決できません"
        return {
            "$type": ref["type"],
            "$value": f"{{{ref['group']}.{ref_name}}}",
            "$extensions": {"com.figma.codeSyntax": {"WEB": f"--{name}"}},
        }, None

    if info["type"] == "color":
        hm = HEX_RE.match(raw)
        if not hm:
            return None, f"hexカラーとして解釈できない値です: {raw}"
        return {
            "$type": "color",
            "$value": {
                "colorSpace": "srgb",
                "components": hex_to_components(raw),
                "alpha": 1,
                "hex": raw.upper(),
            },
            "$extensions": {"com.figma.codeSyntax": {"WEB": f"--{name}"}},
        }, None

    if info["type"] == "number":
        pm = PX_RE.match(raw)
        if not pm:
            return None, f"px単位の数値として解釈できない値です: {raw}"
        val = float(pm.group(1))
        if val.is_integer():
            val = int(val)
        return {
            "$type": "number",
            "$value": val,
            "$extensions": {"com.figma.codeSyntax": {"WEB": f"--{name}"}},
        }, None

    if info["type"] == "string":
        return {
            "$type": "string",
            "$value": raw,
            "$extensions": {"com.figma.codeSyntax": {"WEB": f"--{name}"}},
        }, None

    return None, "未対応の型です"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="brand.css のパス")
    ap.add_argument("--output", required=True, help="出力する .tokens.json のパス")
    ap.add_argument(
        "--groups",
        default="Color,Spacing",
        help="出力するFigmaコレクション名をカンマ区切りで指定(例: Color,Spacing,Radius)",
    )
    ap.add_argument("--mode-name", default="Mode 1", help="com.figma.modeName に入れるモード名")
    args = ap.parse_args()

    requested_groups = {g.strip().lower() for g in args.groups.split(",") if g.strip()}
    tokens = parse_brand_css(args.input)

    out = {}
    skipped = []
    todo_names = []
    included_names = set()

    def include(name, info):
        entry, err = build_entry(name, info, tokens)
        if err:
            skipped.append((name, err))
            return
        out.setdefault(info["group"], {})[name] = entry
        included_names.add(name)
        if info["is_todo"]:
            todo_names.append(name)

    # 1st pass: 明示的に要求されたグループ
    for name, info in tokens.items():
        if info["group"] and info["group"].lower() in requested_groups:
            include(name, info)

    # 2nd pass: 要求グループ内のトークンがvar()で参照している未要求グループのトークンを追加解決
    changed = True
    while changed:
        changed = False
        for name, entry_dict in list(out.items()):
            pass
        for name, info in tokens.items():
            if name in included_names:
                continue
            m = VAR_REF_RE.match(info["raw"])
            # このトークン自体は要求グループ外でも、要求グループ内の何かから参照されていれば追加する
            # (シンプルにするため、要求グループ内の全エントリのraw値をスキャンする)
            referenced = any(
                VAR_REF_RE.match(tokens[n]["raw"]) and VAR_REF_RE.match(tokens[n]["raw"]).group(1) == name
                for n in included_names
            )
            if referenced:
                include(name, info)
                changed = True

    out["$extensions"] = {"com.figma.modeName": args.mode_name}

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total = sum(len(v) for k, v in out.items() if k != "$extensions")
    print(f"書き出し完了: {args.output}")
    print(f"  トークン数: {total}")
    for g in out:
        if g != "$extensions":
            print(f"    {g}: {len(out[g])}")
    if todo_names:
        print(f"  TODO(brand.css上で未確定の仮値): {', '.join(sorted(todo_names))}")
    if skipped:
        print("  スキップ:")
        for name, reason in skipped:
            print(f"    --{name}: {reason}")


if __name__ == "__main__":
    main()
