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

This audit also ran an independent static source scan against the six current HTML files, CSS, and JavaScript from GitHub: all six pages have one H1, skip link, header/nav/main/footer landmarks, no duplicate IDs, and no unresolved local links. All six still declare `lang="en"`. The inspected tree contains no form, `fetch()` call, XMLHttpRequest, localStorage use, or wallet signing/send-transaction method. This is a source scan only; it does not replace browser, server, or deployed HTTPS testing.

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

### F-08 — Token venue economics are not source-auditable (high)
`docs/token-design.md` labels venue costs as verified and includes pump.fun creator economics, migration thresholds, and a graduation-rate estimate, but the source note only refers generally to a fee page/public guides and a study; no direct URLs or archived evidence are attached. These are time-sensitive financial/product claims. Treat them as unverified working estimates until primary-source links, retrieval dates, and calculations are recorded. Muse's venue preference is not an owner decision.

### F-09 — Main branch has no protection (medium)
GitHub reports `main` as unprotected. For a project with token and applicant-data scope, recommend requiring pull requests, at least one review, and passing CI before merge once CI exists. Do not change repository settings without Rama's approval.

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
3. Muse: attach dated primary-source evidence for every token venue fee/economics/migration/graduation claim in `docs/token-design.md`; remove or clearly mark any claim that cannot be verified. ChatGPT reviews before venue selection.
4. ChatGPT: review the proposed architecture and security controls before implementation.
5. Rama: make the explicit provider/privacy/quota decisions listed above.

## Boundaries

No mainnet deployment, token minting, sale, presale, airdrop, wallet signing, fund movement, public whitelist registration, or production website deployment is authorized by this audit.


---

## Audit delta — 2026-11-09, 11:20 WIB

This section supersedes the repository snapshot and CI status above where they conflict. The original 03:20 WIB findings remain historical.

### Current repository state

- `main`: `4707a74b2871c707646943b22405742271ab3d9e`.
- PR #4 / PR-013: open, not merged, current head before this audit-note update `630934fd733dcd73c685d7f9efec18c8690632d9`; GitHub reports mergeable, but acceptance is still blocked.
- PR #5 / PR-014: open, not merged, head `e4d997a00ddf2da8cec64fe60225abed92681526`; GitHub currently reports `mergeable=false`, 12 commits ahead and 10 behind main. Keep it design-only and do not merge ahead of PR-013.
- Root README and `docs/backlog.md` were updated on main and PR-013 to matching content. The README now explicitly says newsroom monitoring, source verification and a public transparency dashboard are not implemented.
- Main branch API reports `protected: false`; repository rulesets endpoint returns `[]`. No required review or status-check enforcement is configured.
- GitHub's classic branch-protection detail endpoint returned 403 to this integration, but the branch object itself reports `protected: false`.

### Current PR-013 implementation and CI

Independent source inspection of all six HTML pages at the current PR-013 branch confirms:

- 6/6 pages declare `lang="id"` and each has exactly one H1.
- No form, fetch/XHR, browser storage, wallet-status UI, wallet signing or transaction code was found.
- The public GitHub repository URL appears in all six pages (two occurrences on Transparency), exposing the owner handle through the site.
- `main.js` toggles the mobile menu through a click listener. The current CDP test invokes a click through `Runtime.evaluate`; it is not a keyboard-only test.
- `styles.css` includes `prefers-reduced-motion: reduce`, but actual browser/OS reduced-motion behaviour has not yet been exercised.

CI evidence:

- Full site-validation run `42556069910` passed on `7ae3174b72980cf1829a7c7ab3d73d72173fcb0f`: 8/8 route checks, 6/6 HTML/copy/security/heading checks, three click-based navigation runs, 12 screenshot captures, checksum generation and artifact upload.
- Owner-side documentation refresh triggered run `42561450697` on `630934fd733dcd73c685d7f9efec18c8690632d9`; GitHub reports the run and every job step as SUCCESS.
- Latest artifact for run `42561450697`: `13649587549`, 2,981,115 bytes, GitHub digest `sha256:064f0aea8287feb0582a6809fb2886af43656e4a8e320bd0494b8080c7c1b6b7`. This latest archive has not been independently downloaded/re-hashed.
- Prior artifact `13647213466` was independently verified in PR comment `6732082342`: downloaded archive digest matched GitHub and `sha256sum -c CI-SHA256SUMS.txt` passed 20/20 entries.
- Five contrast pairs remain a spot-check, not a full WCAG audit.

### Remaining PR-013 acceptance blockers

1. Add actual keyboard-only coverage across all six pages: Tab order, skip link, visible focus, Enter/Space activation, navigation links, Escape/close behaviour and focus return.
2. Test reduced motion using browser media emulation or an actual OS/browser preference.
3. Complete a broader accessibility review; do not claim WCAG conformance from five contrast pairs.
4. Rama must decide whether to retain the public repository footer link, which exposes the owner handle, or remove it. Removing the site link does not anonymize the public GitHub repository itself. Do not invent a replacement URL or organization.
5. Reconcile PR-013 with current main and rerun the relevant checks after source/workflow changes.

### Current PR-014 security posture

The ADR remains design-only. Its revised boundaries are useful but are not implemented or tested:

- Applicant requests must use caller JWT/RLS; service-role bypasses RLS and is limited to narrowly scoped server-side operations.
- Every privileged Supabase operation must enforce AAL2 server-side; tests must prove AAL1 is denied and AAL2 allowed.
- Applicant A must not read applicant B's records; all queries must be scoped to authenticated applicant identity.
- Audit hashes are tamper-evident, not immutable against database-owner compromise; restricted append privileges and external signed chain-head anchors are required.
- Telegram and Discord verification remain MANUAL until consent-based identity binding is designed and security-tested.
- Provider, region, backup/PITR, retention, restore, pricing and email decisions remain open. No provider is selected.

### Muse handoff / attribution

No new Muse implementation commit is visible after the previously recorded site/test-hardening work. The latest PR-013 and PR-014 changes in this audit cycle are owner-side documentation updates. Do not attribute these documentation commits or CI-maintenance commits to Muse.

Next Muse work is the keyboard-only and reduced-motion evidence on PR-013, followed by a deliberate branch update. PR-014 must be reconciled only after PR-013 acceptance and must preserve the security corrections above.

### Safety boundary

No Pages deployment, public preview, backend, live registration, applicant data collection, wallet connection/signing, token mint/distribution, mainnet action or funds movement was performed or authorized.
