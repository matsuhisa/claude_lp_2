---
name: export-figma-tokens
description: build-lp-for-b2 のブランドトークン(`.claude/skills/build-lp-for-b2/tokens/brand.css`)を、Figmaの「Variables(変数)」インポート/エクスポート機能が読み込めるJSON形式(`<モード名>.tokens.json`、例: `Mode 1.tokens.json`)に変換するスキル。ユーザーが「トークンをFigmaに持っていきたい」「brand.cssの色/spacingをFigmaの変数として使いたい」「Mode 1.tokens.json を作って/更新して」「デザイントークンをエクスポートして」のように依頼したときに使う。色(hex→Figmaのfloat32精度RGB)・spacing・radius・border-width・font-sizeなど、brand.css内のCSSカスタムプロパティを対象とする。
---

# Export Figma Tokens

`build-lp-for-b2` スキルが使っているブランドトークン(`brand.css`)を、Figma純正の「Variables(変数)のインポート/エクスポート」機能が読み込める `.tokens.json` ファイルに変換する。`brand.css` を唯一の情報源(single source of truth)とし、色やスペーシングを変更したらこのスキルで再生成する運用を想定している。

## 対象フォーマットについて

Figmaの変数インポート/エクスポートJSONは、W3C Design Tokens(DTCG)形式をベースに `com.figma.*` の拡張情報を加えたもの。以下がこのスキルが理解しているルール:

- **ファイル全体 = 1つのモード**。ルート直下に `"$extensions": {"com.figma.modeName": "<モード名>"}` を置き、そのファイルがFigma変数のどのモード(例: `Mode 1`)に対応するかを示す。
- **トップレベルのキー = Figmaの変数コレクション名**(例: `Color`, `Spacing`)。任意の英語ラベルでよい。
- **各トークン**は `$type` と `$value` を持つオブジェクト:
  - `$type: "color"` の場合、`$value` は `{ colorSpace: "srgb", components: [r, g, b] (0〜1のfloat), alpha, hex }`。`components` はFigma内部が32bit floatで色を保持しているため、素朴な `hex/255` ではなく float32精度に丸めた値にする(このスキルの `generate_tokens.py` が対応済み)。
  - `$type: "number"` の場合、`$value` は単位なしの数値(pxの値をそのまま数値として入れる。Figmaの数値変数=FLOAT型に対応)。
  - `$type: "string"` の場合、`$value` はそのまま文字列(フォントファミリーなど)。
  - **他のトークンを参照する場合**(CSSの `var(--x)` に相当)は、`$value` を `"{コレクション名.トークン名}"` という文字列にする(例: `"{Font Size.font-size-32}"`)。参照先のトークンも同じファイルに含まれている必要がある。
  - 任意で `$description`(注記)を付けられる。
  - 任意で `$extensions.com.figma.codeSyntax.WEB` に実装側の変数名(例: `--color-primary`)を入れると、Figma側の変数インスペクタでコード上の名前が確認できる。**このスキルは常にこれを付与する**(brand.cssとの対応が追えるようにするため)。
  - `com.figma.variableId` は、既存のFigma変数を更新する場合に一致させるためのID。**このスキルは付与しない**(実際のFigmaファイル固有のIDを持っていないため)。付けなければFigma側は新規変数として作成する。

## 使い方

1. **入力元を確認する**: 通常は `.claude/skills/build-lp-for-b2/tokens/brand.css`。`brand.draft.css`(ドラフト用グレースケール)やLP限定の `assets/brand-override.css` から書き出したい場合はユーザーに確認する。
2. **対象グループを確認する**: どのトークン群を書き出すかユーザーに確認する(過去のやり取りで指定済みならそれに従う)。指定が無ければ `Color,Spacing` をデフォルトとする。選べるグループ:
   - `Color` — 色トークン(`--color-*`)
   - `Spacing` — 余白トークン(`--spacing-*`)
   - `Radius` — 角丸トークン(`--radius-*`)。ただし `radius-full`(`50%`)のようなpx以外の値は変換できずスキップされる
   - `Border Width` — 枠線太さ(`--border-width-*`)
   - `Font Size` — フォントサイズのプリミティブ(`--font-size-*`)
   - `Font Family` — フォントファミリー(`--font-family-*`、文字列として出力)
   - `Font` — 見出し/本文/ラベルなどセマンティックなフォントトークン(`--font-heading-1` など)。多くは `var(--font-size-*)` の参照なので、参照先が指定グループになくても自動的に追加解決される
   - `elevation-*`(box-shadowの複合値)は非対応。常にスキップされ、実行結果に理由付きで表示される
3. **出力先とモード名を確認する**: デフォルトは `.claude/skills/build-lp-for-b2/tokens/Mode 1.tokens.json`、モード名は `Mode 1`。ユーザーが別のFigmaモード名・出力先を指定したらそれに従う。
4. **スクリプトを実行する**:

   ```
   python3 .claude/skills/export-figma-tokens/scripts/generate_tokens.py \
     --input .claude/skills/build-lp-for-b2/tokens/brand.css \
     --output ".claude/skills/build-lp-for-b2/tokens/Mode 1.tokens.json" \
     --groups "Color,Spacing" \
     --mode-name "Mode 1"
   ```

   実行結果には、書き出したトークン数・グループ内訳に加えて、`brand.css` 上でまだ `TODO` コメント付きの仮値であるトークンの一覧、変換できずスキップしたトークンとその理由が表示される。
5. **結果をユーザーに報告する**: TODO(未確定の仮値)が含まれている場合は、その旨とトークン名を必ず伝える(黙って仮値のまま確定させない)。スキップしたトークンがあれば理由も伝える。

## 再生成のタイミング

`brand.css` を更新した(色を確定した、トークンを追加/変更した)ときは、このスキルで `.tokens.json` を再生成する。生成された `.tokens.json` は `brand.css` から機械的に導出される成果物なので、直接手編集はしない。
