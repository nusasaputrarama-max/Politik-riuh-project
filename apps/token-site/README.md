# POLITIK RIUH — Token Launch Website (Phase 1)

Pure static HTML/CSS/JS. **Zero dependencies**: no package manager, no build step, no webfonts, no external requests at runtime. System font stacks only.

## Files

| File | What it is |
|---|---|
| `index.html` | `/` — landing: identity, status, token at a glance, pillars, transparency preview, risk disclosure |
| `about.html` | Purpose, independent positioning, risks and limitations |
| `token.html` | Token overview and facts table |
| `launch.html` | Launch status ("Not launched") and the five mainnet gates |
| `transparency.html` | Allocation / treasury / wallet disclosures (all currently unavailable) |
| `roadmap.html` | Milestones with status labels backed by repository evidence |
| `styles.css` | Shared design system (see below) |
| `main.js` | One behaviour only: the mobile navigation toggle (progressive enhancement) |
| `evidence/` | Screenshots from the checks below |

## Design system

Near-black base `#0A0A0B`, surface `#121214`, thin borders `#26262A`, restrained red accent `#E5484D` (primary buttons use darker `#C93338` so white text passes WCAG AA), muted grey text `#9A9AA0`, monospace micro-labels, strong editorial headline, restrained ambient glow. Semantic HTML, keyboard navigation, visible focus, `prefers-reduced-motion` support. Responsive-first; mobile is a primary layout.

## Local setup

```sh
cd apps/token-site
python3 -m http.server 8000 --bind 127.0.0.1
# open http://127.0.0.1:8000/index.html
```

No build, no install, no environment variables.

## Checks run (2026-11-09, local)

| Check | Result |
|---|---|
| Route smoke test (`curl`, local server) | **8/8 HTTP 200**: `/`, `index/about/token/launch/transparency/roadmap.html`, `styles.css`, `main.js` |
| HTML parse (python `html.parser`) | **6/6 pages, no errors**; exactly one `<h1>` per page; `header/nav/main/footer` landmarks on every page; no duplicate IDs |
| Internal links | All `href`/`src` targets resolve on disk (checked per page) |
| JS syntax | `node --check main.js` — pass |
| Contrast (computed WCAG ratios) | Muted text on bg **7.07:1**; headline **18.96:1**; red accent on bg **5.06:1**; primary button white on `#C93338` **5.01:1**; hover **5.55:1** — all pass AA normal text (4.5:1) |
| Keyboard / accessibility checklist | Skip link on all 6 pages; `:focus-visible` outline; `aria-current="page"` on the current nav item (5 subpages); nav toggle carries `aria-expanded` and updates on click; logical tab order (DOM order) |
| Nav toggle functional test | Temporary test page clicked the toggle in headless Chrome: `NAV-OPEN=true ARIA=true LABEL=Close menu` — pass (test file removed afterwards) |
| Secrets grep | No private keys, API keys, tokens, or passwords found in the tree |
| External requests | None at runtime. The only external URL in the tree is the GitHub repository link (footer + transparency page) |
| Wallet / signing code | None. The only wallet text is the header status line "Wallet — Not connected · Read-only connect planned" (plain text, no button, no code) |
| Screenshots (headless Chrome 157) | `evidence/landing-desktop.png` (1280×2600 full page), `evidence/landing-mobile.png` (390×3800 full page), `evidence/{about,token,launch,transparency,roadmap}-desktop.png` (1280×1000 viewport) |

### Bugs found by the screenshots and fixed

1. **Hero pushed down ~480px (desktop + mobile).** Cause: `.hero > * { position: relative; }` outranked `.glow`'s `position: absolute`, so the glow took flow space. Fixed to `.hero > .wrap`.
2. **Wallet status pill overflowed the viewport on mobile.** Cause: `white-space: nowrap` on a 44-character pill. Fixed: wraps to two lines below 720px.
3. **Primary button contrast failed AA (3.75:1).** White on `#E5484D` is below 4.5:1 for normal text. Fixed: button background darkened to `#C93338` (5.01:1); hover `#BE2E33` (5.55:1).

## Facts discipline (binding)

- **Supply is shown as "Proposed — pending founder approval" with NO number.** Two conflicting proposals exist: `docs/token-design.md` drafts 1,000,000,000 while `docs/website-launch-spec.md` §10 notes 10,000,000,000 as a proposal. That conflict (D-05a) is an open founder decision; the site does not resolve it.
- No ticker, contract/mint address, launch date, holder count, volume, price, or reward metrics anywhere on the site — none exist.
- Launch status is "Not launched" / "Mainnet not launched", with no countdown.
- No fake counters, waitlists, dead CTAs, or placeholder links presented as functional.

## Deployment target (proposed, not configured)

**GitHub Pages (proposed)** — decision D-01 is still open (ChatGPT/Rama). Note: the site lives in a subdirectory (`apps/token-site/`), so Pages needs a workflow that publishes that directory (or a dedicated branch). Nothing is deployed yet; this README documents the target only.

## Known limitations

- **No wallet connection.** Deferred per `docs/frontend-stack-decision.md` §2 (optional in the spec; adding wallet-adapter packages would introduce dependencies for an optional feature). The header shows the status as text only.
- **No backend, no forms, no analytics.** Contact / report channel is not yet configured (stated as plain text in the footer).
- **Token facts are pending founder decisions:** name/ticker (D-05), supply (D-05a: 1B vs 10B), venue (D-04), launch date, official domain and verified social links.
- **Reduced-motion support is verified by code inspection** (the `prefers-reduced-motion` media query is present and disables transitions); it was not tested against a live OS-level reduced-motion setting.
- **Screenshots are local renders** (headless Chrome 157 against a local server), not a deployed-site capture.
- The founder's Elysium mobile screenshot was **not** in the repo and was not used; the design works from the written description of the references only, and does not clone either reference.
