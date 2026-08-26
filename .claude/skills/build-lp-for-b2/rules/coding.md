# コーディングルール(生成LP用)

- build-lp-for-b2 が生成するHTML/CSSに適用する規約。
- ブランドトークン(`tokens/brand.css` / `tokens/brand.draft.css` / `tokens/brand.json`)とは別に、構造・命名の一貫性を保つためのルール。

## CSSクラス命名

- FLOCSS、BEM を基本にする
  - ヘッダー・フッターなどページ全体の骨格を決める class （ layout ）は、`l-*` が接頭辞になる
  - 使い回す class （ component ）は、`c-*` が接頭辞になる
    - Block には margin を含めない
  - component を複数集めてレイアウトを決める class （ project ）は、 `p-*` が接頭辞になる
  - タイポグラフィーなどのどこでも使う class （ utility ）は、`u-*` が接頭辞になる
- kebab-case で単語を区切る
- クラス名は、略称をさける
  - ボタンであれば、`.c-button` にする。`btn` などにしない
- 固有のクラス名は、そのセクションの役割を表す英単語1〜2語にする(例: `hero`, `final-cta`)。連番や意味のない名前(`.section1`, `.box2`)は、原則使わない。
- `u-*`(utility)の実装は `.claude/skills/build-lp-for-b2/rules/styles/u-*.css` に置く(例: `u-typography.css`)。新しいユーティリティ群を作る場合もこの命名(`styles/u-<用途>.css`)に揃える。
- `c-*`(component)は `component/c-<名前>/` にコンポーネントごとのディレクトリを作り、`c-<名前>.html` と `c-<名前>.css` を1組にして置く(html/cssを一緒に編集できるように)。`c-<名前>.html` には、必須/任意のフィールドが決まっている場合、TypeScriptの `interface` 風コメント(必須はそのまま、任意は `field?: type` + `// 任意`)とマークアップを同じファイルに置く。プレースホルダーはJSXに合わせて単一の波括弧 `{value}` を使い、属性値もクォートで囲まず `attr={value}` の形にする(例: `.claude/skills/build-lp-for-b2/rules/component/c-cta-link/c-cta-link.html` + `c-cta-link.css`)。`p-*` の実装が増えたら、同様に `project/p-<名前>/p-<名前>.css` を作る。
- `l-*`(layout)は `layout/l-<名前>/` にディレクトリを作り、`l-<名前>.html` と `l-<名前>.css` を1組にして置く。ページ全体で1回しか使わない前提の骨格(ヘッダー・フッターなど)が対象で、`c-*`/`p-*` と同じくpropsが決まっている場合はTypeScriptの `interface` 風コメントを添える(例: `layout/l-header/l-header.html` + `l-header.css`)。


## レスポンシブ / ブレイクポイント

- PCとスマートフォンの2段階のみ。境界は以下で固定する。
  - スマートフォン: 〜768px
  - PC: 769px以上
- モバイルファーストで書く。まずスマートフォン向けのスタイルを通常のルールとして書き、PC向けの上書きを `@media (min-width: 769px) { ... }` に書く。
- CSSカスタムプロパティ(`var(--...)`)は `@media` の条件式内では使えないため、`tokens/brand.css` にブレイクポイント用の変数は作らない。`769px` の値は各コンポーネント/セクションのCSS内で直接書き、このルール(coding.md)を唯一の基準とする。

## HTMLセクションの方針

- 1セクション = `SKILL.md` の「セクション構成」の1項目に対応する `<section>` 要素1つ。複数の項目を1つの `<section>` に詰め込まない。
  - 1セクションのなかに、コンテンツが複数ある場合は、`<article>` を使う
- ナビゲーション・CTAから `#id` でアンカーされるセクションは、`id` とスタイリング用 `class` の両方を付与する(例: `<section id="lineup" class="lineup">`)。アンカー不要なセクションは `class` のみでよい。`id` だけを付けてそれをCSSセレクタとして直接使うのは避ける。
- 各セクションは `<section class="wrap">` で内側を包み、幅・左右余白を揃える。
- 見出し階層: `<h1>` はヒーローの1箇所のみ。各セクションのメイン見出しは `<h2>`。カード・サブセクションの見出しは `<h3>`。それより下の階層は作らない。
- ヘッダー/フッターはセマンティックタグを使う(`<header">` / `<main>` /`<footer>`)。
