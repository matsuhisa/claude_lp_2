---
name: build-lp-for-b2
description: Build a self-contained, single-file HTML B2B landing page (LP) styled with this project's brand tokens. Use this skill whenever the user asks to create, draft, redesign, or update a landing page, product page, sales page, or marketing page for a B2B product, service, or offer — even if they don't say "landing page" explicitly (e.g. "make a page for our new feature launch", "I need something to send to prospects", "build a page pitching X to enterprise customers", "LP作って"). Always read `.claude/tokens/brand.json` first for brand colors, fonts, and voice before writing any HTML.
---

# Build LP for B2B

Produces a single self-contained HTML file for a B2B landing page, styled using this project's brand tokens, following a conversion-focused B2B section structure. Can optionally be published via the Artifact tool for instant preview/sharing.

## Before you start

1. **Read `.claude/tokens/brand.json`** in this project. It holds brand colors, fonts, logo, radius, spacing, and voice/tone for every LP built with this skill — treat it as the single source of truth for styling.
   - If fields still contain `TODO:` placeholders, tell the user which ones are missing and ask for the real values (or ask them to fill in the file) before finalizing colors. Silently using placeholder colors produces an off-brand page, which defeats the point of having tokens.

2. **Ask the user for the content basics** if not already given in the conversation:
   - Product/service name and one-line value proposition
   - Target buyer persona (e.g. "IT director at mid-size SaaS companies")
   - Primary CTA (e.g. "Book a demo", "Start free trial", "Contact sales")
   - Any real proof points: customer logos, testimonials, case study stats, pricing tiers
   - Whether this is for a specific campaign/channel (affects tone and urgency)

## Section structure

Default to this order — it's a standard B2B conversion structure — unless the user asks for something different:

1. **Hero** — headline, subheadline, primary CTA, optional hero visual
2. **Problem / pain points** — 2-4 pain points the persona recognizes
3. **Solution / key features** — 3-6 features tied to outcomes, not just capabilities
4. **How it works** — short 3-4 step flow
5. **Social proof** — customer logos or case study stats
6. **Testimonials** (optional) — only if the user provides real quotes
7. **Pricing** (optional) — only if the user provides real tiers
8. **FAQ** — 4-6 objections a B2B buyer would actually have (security, integration, implementation time, pricing, contract terms)
9. **Final CTA** — repeat the primary CTA, lower-friction framing
10. **Footer** — company info, links

Skip sections the user has no real content for rather than filling them with filler — an LP with 7 solid sections beats one with 10 where 3 are empty-sounding.

## Output requirements

- **Single self-contained HTML file**: inline `<style>`, inline or data-URI assets, no external CDN/font/script dependencies. This also makes it publishable as an Artifact, which has a strict CSP.
- **Apply brand tokens directly** as CSS custom properties at the top of the stylesheet, sourced from `.claude/tokens/brand.json`. Don't invent colors or fonts that aren't in the token file.
- **Mobile-responsive**: stacked layout on narrow viewports, no horizontal scroll, tap-friendly CTA buttons.
- **Real, specific copy** — no lorem ipsum, no generic "Feature 1 / Feature 2" placeholders. If there isn't enough detail for a section, ask the user rather than inventing stats, logos, or customer names.
- **Never fabricate social proof** — customer names, logos, testimonial quotes, or metrics must come from the user. Making these up is misleading even as a draft.
- **Accessible**: semantic HTML (`<header>`, `<section>`, `<nav>`, heading hierarchy), sufficient color contrast using the token colors, alt text on images.

## After building

Ask the user whether they'd like the page published as an Artifact for instant preview/sharing. If yes, use the Artifact tool — load the `artifact-design` skill first, per its own instructions, and use `logo.faviconEmoji` from the token file as the favicon. Otherwise, just save the HTML file at the path the user specifies.
