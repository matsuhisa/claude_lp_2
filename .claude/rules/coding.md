# コーディングルール(生成LP用)

- build-lp-for-b2 が生成するHTML/CSSに適用する規約。
- ブランドトークン(`tokens/brand.css` / `tokens/brand.draft.css` / `tokens/brand.json`)とは別に、構造・命名の一貫性を保つためのルール。

## CSSクラス命名

- FLOCSS、BEM を基本にする
  - 使い回す class （ component ）は、`c-*` が接頭辞になる
    - Block には margin を含めない
  - component を複数集めてレイアウトを決める class （ project ）は、 `p-*` が接頭辞になる
  - タイポグラフィーなどのどこでも使う class （ utility ）は、`u-*` が接頭辞になる
- kebab-case で単語を区切る
- クラス名は、略称をさける
  - ボタンであれば、`.c-button` にする。`btn` などにしない
- 固有のクラス名は、そのセクションの役割を表す英単語1〜2語にする(例: `hero`, `final-cta`)。連番や意味のない名前(`.section1`, `.box2`)は、原則使わない。
- `u-*`(utility)の実装は `.claude/rules/utility/u-*.css` に置く(例: `u-typography.css`)。新しいユーティリティ群を作る場合もこの命名(`utility/u-<用途>.css`)に揃える。`c-*` / `p-*` の実装が増えたら、同様に `component/c-*.css` / `project/p-*.css` を作る。


## HTMLセクションの方針

- 1セクション = `SKILL.md` の「セクション構成」の1項目に対応する `<section>` 要素1つ。複数の項目を1つの `<section>` に詰め込まない。
  - 1セクションのなかに、コンテンツが複数ある場合は、`<article>` を使う
- ナビゲーション・CTAから `#id` でアンカーされるセクションは、`id` とスタイリング用 `class` の両方を付与する(例: `<section id="lineup" class="lineup">`)。アンカー不要なセクションは `class` のみでよい。`id` だけを付けてそれをCSSセレクタとして直接使うのは避ける。
- 各セクションは `<section class="wrap">` で内側を包み、幅・左右余白を揃える。
- 見出し階層: `<h1>` はヒーローの1箇所のみ。各セクションのメイン見出しは `<h2>`。カード・サブセクションの見出しは `<h3>`。それより下の階層は作らない。
- ヘッダー/フッターはセマンティックタグを使う(`<header">` / `<main>` /`<footer>`)。
