# POLITIK RIUH — Repository Audit
Date: 2026-11-09, 03:20 WIB
Auditor: ChatGPT
Scope: repository state, token launch website, Muse implementation evidence, open blockers, and security posture.

## Executive summary

The token launch website is no longer docs-only. Muse has committed a six-page, zero-dependency static prototype under `apps/token-site/`. The prototype has source files, local screenshot evidence, and a README recording local checks. It is not deployed, has no backend, has no whitelist registration, and has no wallet integration or transaction code.

The next review is not a token launch. It is a pre-preview quality pass plus a separate secure whitelist architecture task. The owner has since approved the REFORMASI identity and a task-based, sequential, hybrid whitelist process in comments on issue #1. Those decisions have not yet been reflected in the site code.

## Repository snapshot

- Canonical repository: `nusasaputrarama-max/Politik-riuh-project`.
- Visibility: public.
- Default branch: `main`.
- Latest observed main commit at audit time: `d8f2da8a0ce06061a75d9f7dbf46105867716f00`.
- Main branch protection: not enabled.
- Open pull requests: 0.
- Open issue: #1, PR-013 — review and prepare token site for public preview.
- GitHub Actions workflow runs: 0 observed; no CI result is available.
- GitHub Pages: not enabled; no public deployment verified.

## Recent Muse work (verified in GitHub)

| Commit | Work |
|---|---|
| `b39214e` | Records static zero-dependency frontend stack decision. |
| `15b3b6f` | Adds shared design system and landing page. |
| `91cdf4a` | Adds About, Token, Launch, Transparency, and Roadmap pages. |
| `63757c9` | Adds site README and desktop/mobile screenshot evidence. |
| `d8f2da8` | Marks PR-012 website Phase 1 as done in backlog. |

Tree inspection confirms six HTML pages, shared `styles.css`, `main.js`, site README, and screenshot files in `apps/token-site/evidence/`. The commits are unsigned according to GitHub's verification metadata; this is not by itself proof of malicious activity, but the repository currently has no required signature policy.

## Implementation and test evidence

Muse's `apps/token-site/README.md` records the following local results:
- 8/8 route smoke checks returned HTTP 200.
- 6/6 HTML pages parsed without reported errors, with one H1 and required landmarks.
- Internal links resolved.
- `node --check main.js` passed.
- Reported WCAG AA contrast ratios passed for listed text/button combinations.
- Keyboard navigation checklist and a headless Chrome nav-toggle test passed.
- No secrets, external runtime requests, wallet code, or signing code found by Muse's recorded scan.
- Desktop and mobile screenshots are committed.

These are **reported local results**, not CI results. This audit verified that the evidence files and README exist, but did not rerun Muse's local browser/curl test suite. The repo has zero GitHub Actions runs, so no independent CI confirmation exists.

## Findings requiring correction

### F-01 — Root README is stale (high)
The root `README.md` still says the project is docs-only and that no application code runs anywhere. It omits `apps/token-site/`. This is now factually incorrect and should be updated before a public preview.

### F-02 — Website language does not meet the issue requirement (high)
All six HTML pages are authored with `lang="en"` and user-facing copy is predominantly English. Issue #1 explicitly requires natural Indonesian copy. Translate all participant-facing content, metadata, navigation, status labels, and risk disclosures into consistent Indonesian; keep technical labels only where they are useful and explain them.

### F-03 — Site identity conflicts with owner decision (high)
The site still says the token name is undecided and the Token page lists NENGOK, GORENG, and DER as candidates. The owner has approved **REFORMASI** as token name and **REFORMASI** as proposed symbol/ticker, subject to technical compatibility checks. The home, token, launch, roadmap, and site README must be aligned. Do not mark ticker compatibility as complete without evidence.

### F-04 — Whitelist requirements are not implemented (high)
The current site has no registration form, applicant dashboard, task list, admin interface, backend, database, or authentication. This is consistent with the original static-only scope, but it does not yet satisfy the later owner-approved REFORMASI whitelist specification. A static site must not collect email/wallet/X data without a protected backend.

### F-05 — Token supply remains unresolved (high)
`docs/token-design.md` drafts 1B while `docs/website-launch-spec.md` mentions a 10B proposal. Neither is approved. Keep numeric supply off the public site until Rama resolves the conflict. Do not silently select one.

### F-06 — Deployment feasibility is incomplete (medium)
The site README calls GitHub Pages a proposed target but no Pages configuration, publishing workflow, exact subdirectory artifact configuration, custom-domain plan, HTTPS verification, or rollback procedure is present. Issue #1 requires a deployment feasibility note. Do not publish or change repository deployment settings until owner review.

### F-07 — Roadmap and site documentation need synchronization (medium)
The public Roadmap currently treats token name/ticker decision as still planned. The root README and backlog also need to distinguish the static token site from the separate future news portal in `apps/web/`.

## Security review

### Current static prototype
The present site is a low-complexity static HTML/CSS/JS artifact. The inspected source has no form submission, backend calls, analytics, wallet adapter, signing, transaction construction, or third-party runtime fetches. This keeps its current attack surface small. External GitHub links use `target="_blank"` with `rel="noopener"`.

No deployment is active, so there is no live endpoint to test for headers, TLS, caching, or production behavior. No CI runs were observed.

### Whitelist security boundary
The new whitelist feature changes the risk profile because it will collect an email address, a Solana public wallet address, and an X handle. The combined record is private applicant data even though the wallet address is public on-chain. Do not store applicant data in GitHub, static JSON, issue comments, browser local storage, or public analytics. Live collection requires a backend, server-side validation, email verification, access-controlled database, admin authentication/MFA, rate limits, audit logs, privacy notice/consent, retention/deletion policy, and protected evidence storage.

No wallet connection or signature is needed for the approved registration flow. Never request seed phrases, private keys, wallet passwords, or transactions. Platform actions must be labeled self-attested/manual unless an allowed API genuinely verifies them.

## Owner decisions now recorded

GitHub issue #1 comments record:
- POLITIK RIUH presents REFORMASI.
- Token name and proposed ticker: REFORMASI (ticker compatibility check remains).
- Anonymous team identity; hybrid political satire, internet/meme culture, and community character.
- Long-term priority: community-first.
- Whitelist registration fields: email, Solana public wallet address, X handle.
- Sequential tasks with explicit LOCKED/OPEN/SUBMITTED/DONE/VERIFIED/NEEDS REVIEW states.
- Hybrid eligibility validation plus human selection; quota configurable and undecided.
- API verification only where supported; otherwise manual review/self-attestation.
- No guarantee of whitelist approval or allocation.

The detailed implementation/security requirements are consolidated in `docs/whitelist-spec.md`.

## Current blockers and founder decisions

Before live whitelist registration:
1. Approve backend/hosting and database provider.
2. Approve applicant dashboard authentication and admin access method.
3. Choose email delivery provider and sender identity.
4. Decide privacy notice, retention period, deletion process, and operational contact.
5. Confirm official X/Telegram/Discord account URLs and campaign tasks.
6. Set the admin-configurable whitelist quota and selection rules.

Separate token decisions still open:
- Supply (1B vs 10B conflict), decimals, allocations, vesting.
- Launch venue/mechanism, launch date, official domain.
- Ticker compatibility verification.

## Next work order

1. Muse: complete PR-013 by fixing Indonesian copy, REFORMASI identity, roadmap/status consistency, and the detailed static-hosting feasibility/rollback note. Work on a feature branch and submit a PR; do not deploy.
2. Muse: prepare a whitelist architecture decision record against `docs/whitelist-spec.md`, comparing viable backend/database/auth/email options, threat model, operating costs, data flow, backup/retention, and rollback. No real applicant data and no public registration until Rama approves the architecture.
3. ChatGPT: review the proposed architecture and security controls before implementation.
4. Rama: make the explicit provider/privacy/quota decisions listed above.

## Boundaries

No mainnet deployment, token minting, sale, presale, airdrop, wallet signing, fund movement, public whitelist registration, or production website deployment is authorized by this audit.
