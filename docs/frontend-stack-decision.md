# POLITIK RIUH — Frontend Stack Decision (Token Launch Website, Phase 1)

- **Date:** 2026-11-09 ~02:20 WIB
- **Author:** Muse (engineering partner)
- **Status:** DECISION RECORDED — open to ChatGPT review. Implementation follows this decision unless ChatGPT or Rama overrides it in the repo.
- **Source:** repo audit 2026-11-09 + `docs/website-launch-spec.md` v0.1 (ChatGPT) + `docs/architecture.md` v0.1.

## 1. Repository audit (what exists before adding anything)

- Repo contains **docs + scaffold only**: `README.md`, `docs/` (architecture, backlog, risks, token-design, editorial-policy, website-launch-spec), `collaboration/` (2 handoffs), `data/schema.sql` (draft), folder READMEs under `apps/web`, `services/`, `content/`, `token/`.
- **No framework, no build tooling, no dependencies:** no `package.json`, no bundler, no CSS framework, no test runner, no CI.
- `apps/web/` is a placeholder README for the future news portal. The token launch site does not exist yet.

## 2. Decision

**Pure static HTML/CSS/JS, zero dependencies, in `apps/token-site/`.**

- Location: `apps/token-site/` — separate from `apps/web/` (news portal). This enforces the spec boundary: the token site is a dedicated site, not the news portal.
- Pages (multi-page static, shared stylesheet, plain links): `index.html` (/), `about.html`, `token.html`, `launch.html`, `transparency.html`, `roadmap.html`.
- No build step. Scripts in `package.json` (if added) are checks only: local serve, route smoke test, link check — not a build.
- No webfonts in Phase 1 (system font stacks only) — zero external fetches at runtime.
- **Wallet connect: NOT in the Phase 1 build.** The spec makes it optional ("may implement"). Adding wallet-adapter packages would introduce npm dependencies and supply-chain review for an optional feature. Deferred to a post–Phase 1 decision; the header shows wallet status as "Not connected — read-only connect planned" with no dead button (no button at all until it works).

## 3. Rationale

- Spec §6: "Prefer a static-first frontend" + "Do not introduce a second stack without documenting why." There is no first stack — the repo has none — so the smallest coherent stack is zero-dependency static.
- Zero supply-chain risk (no `node_modules`, no lockfile to audit) and GitHub Pages-ready with no build configuration.
- Nothing to break: no bundler version drift, no SDK (the AG-001 Hatch SDK experience — U-97/U-113 — argues against adopting a platform SDK for a static informational site).
- Design system is achievable in plain CSS (custom properties, thin borders, ambient glow via radial gradients).

## 4. Design tokens (from spec §2)

- Base: near-black `#0A0A0B`; surface `#121214`; borders thin `#26262A`.
- Accents: restrained red `#E5484D` (Indonesian accent, used sparingly), white `#FAFAFA` for headlines.
- Text: muted grey `#9A9AA0` body; monospace micro-labels (system `ui-monospace` stack).
- Type: strong editorial headline (system sans, heavy weight, tight leading); generous spacing; rounded stat panels; restrained ambient glow (radial gradient, low opacity).
- Accessibility: semantic HTML, keyboard navigation, visible focus, contrast-checked, `prefers-reduced-motion` respected.

## 5. Facts discipline (binding for the implementation)

- Every figure/status on the site carries a source or is marked proposed/unavailable. No holder counts, volume, market cap, price, rewards, waitlist counts, countdowns, or contract/mint addresses (none exists).
- **Supply: displayed as "Proposed — pending founder approval" with NO number.** Reason: two conflicting proposals exist — `docs/token-design.md` drafts 1,000,000,000 (pump.fun fixed supply) while the spec §10 notes "the previously discussed supply of 10,000,000,000 is a proposal only". The discrepancy is an open decision (D-05a), not something the implementation may resolve silently.
- Launch status: "Not launched" / "Mainnet not launched" — no date, no countdown.
- No dead CTAs, no placeholder links presented as functional.

## 6. Checks required (Phase 1 acceptance)

- All 6 routes load (local serve + curl smoke test), mobile + desktop widths.
- Mobile + desktop screenshots in evidence.
- Contrast + keyboard + reduced-motion check (manual checklist, recorded).
- No secrets committed; no external runtime fetches; no signing/transaction code anywhere.
- README in `apps/token-site/` documents setup, checks, deployment target (GitHub Pages, proposed), known limitations.

## 7. Open decisions carried (do not finalize in code)

D-05 token name/ticker; D-05a supply (1B vs 10B); D-04 launch venue/mechanism; launch date; official domain + verified social links; hosting/deployment ownership (D-01).

## Owner-approved scope amendment (2026-11-09)

The token-site brand is now **POLITIK RIUH presents REFORMASI**. The static frontend decision remains appropriate for the informational six-page site, but it is **not** an architecture for collecting applicant data. The approved task-based whitelist requires a protected backend, database, applicant authentication, admin authentication/MFA, email verification, privacy/retention controls, and server-side task verification. See `docs/whitelist-spec.md`. No live registration or provider selection is authorized until Rama approves the architecture and privacy decisions.
