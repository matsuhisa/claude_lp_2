# claude_lp_2

Claude Code のスキル `build-lp-for-b2` を使って、ブランドトークンに沿ったB2B向けランディングページ(LP)を単体HTMLファイルとして生成するためのプロジェクトです。ブランドトークンをFigmaの変数として使うための `export-figma-tokens` スキルも含みます。

## 使い方

Claude Code のセッションで次のように依頼すると、スキルが自動的に(または `/build-lp-for-b2` で明示的に)起動します。

```
/build-lp-for-b2
```

- 初回はブランドトークン(`tokens/brand.css` / `tokens/brand.json`)の `TODO` を埋めるよう案内されます。
- `spec/<取り組み名>/` を使うかどうか、使う場合は `content.md`(確定原稿)と `content-draft.md`(ドラフト)のどちらを元にするかを聞かれます。
- 生成されたHTMLと、PC/スマホ幅のキャプチャー画像は `spec/<取り組み名>/src/` に保存されます。

詳細な挙動は [`.claude/skills/build-lp-for-b2/SKILL.md`](.claude/skills/build-lp-for-b2/SKILL.md) を参照してください。

## ディレクトリ構成

```
.claude/skills/build-lp-for-b2/
├── SKILL.md            # スキル本体の指示書
├── tokens/
│   ├── brand.css        # 色・フォント・角丸・余白などのデザイントークン
│   ├── brand.draft.css  # ドラフト用グレースケール配色
│   └── brand.json       # 社名・タグライン・ロゴ・トーン&マナー
├── rules/
│   ├── coding.md         # CSSクラス命名・HTML構造・ブレイクポイントの規約
│   ├── component/c-*/    # 再利用コンポーネント(html+css)
│   ├── project/p-*/      # コンポーネントを組み合わせたレイアウト単位
│   ├── layout/l-*/       # ヘッダー・フッターなどページ骨格
│   └── styles/u-*.css    # タイポグラフィーなどのユーティリティ
├── index.html            # token.html / token-editor.html / components.html への入口
├── token.html            # トークンの確認用ページ
├── token-editor.html     # トークンの調整・書き出し用ページ
└── components.html       # 登録済みコンポーネントのプレビュー

spec/                     # 個別LPの作業ディレクトリ(gitignore対象、リポジトリには含まれない)
└── <取り組み名>/
    ├── content-draft.md  # 検討中のドラフト構成・コピー
    ├── content.md        # 確定原稿
    ├── assets/            # このLP限定のロゴ・写真・トークン上書き
    └── src/               # 生成したHTML・キャプチャー画像の出力先

spec_sample/               # spec/ の運用イメージを示すサンプル(コミット対象)
```

## ブランドトークンの確認・編集

`.claude/skills/build-lp-for-b2/index.html` をブラウザで開くと、`token.html`(確認)・`token-editor.html`(編集)・`components.html`(コンポーネント一覧)にまとめてアクセスできます。

## ブランドトークンをFigmaへエクスポート

`export-figma-tokens` スキルを使うと、`brand.css` の色・spacingなどをFigmaの「Variables」インポート機能が読み込めるJSON(`Mode 1.tokens.json` など)に変換できます。詳細は [`.claude/skills/export-figma-tokens/SKILL.md`](.claude/skills/export-figma-tokens/SKILL.md) を参照してください。

## 注意事項

- `spec/` は `.gitignore` で除外されているため、個別LPの原稿・生成物はこのリポジトリにコミットされません。
- 生成するHTMLは外部CDN・外部フォントに依存しない単体ファイルが原則です(未確定の画像に限り `placehold.jp` のダミー画像を使用可)。詳細は `rules/coding.md` を参照してください。
