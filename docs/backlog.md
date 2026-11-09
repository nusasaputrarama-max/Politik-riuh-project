# POLITIK RIUH — Phase 1 Development Backlog

- **Date:** 2026-11-09
- **Status:** Active. PR-001 and PR-012 are complete; PR-013 is **IN REVIEW — NOT ACCEPTED** (PR #4, latest head `7ae3174b72980cf1829a7c7ab3d73d72173fcb0f`); PR-014 is **DESIGN ONLY — SECURITY REVIEW REQUIRED** (PR #5, latest head `e4d997a00ddf2da8cec64fe60225abed92681526`). No provider is selected and no whitelist implementation is authorized.
- **Owners (proposed):** Rama = final decisions; ChatGPT = architecture/audit; Muse = implementation/docs.
- **Rule:** no item is "done" without evidence in this repo (commit + file, test log where applicable). No fabricated results.

| ID | Item | Owner | Status | Acceptance criteria | Depends on |
|---|---|---|---|---|---|
| PR-001 | Repo + docs scaffold (architecture, backlog, risks, token design, editorial policy, handoff) | Muse | **DONE** (this handoff) | Repo exists, docs committed + pushed, handoff filed | — |
| PR-002 | Editorial policy v1 approval | Rama + ChatGPT | TODO | `docs/editorial-policy.md` reviewed, approved or amended in repo | PR-001 |
| PR-003 | Source list v1 (10–20 Indonesian political news RSS sources) | Muse | TODO | List in repo with URL + liveness check evidence (each feed fetched once, status recorded) | PR-002 |
| PR-004 | Ingestor skeleton (RSS poll → SQLite, dry-run) | Muse | TODO | Polls allowlisted feeds, writes `articles` rows, dedups by URL hash, fails closed on dead feeds; SSRF guard present; dry-run log in repo | PR-003, PR-010 |
| PR-005 | Schema migration 0001 + seed sources | Muse | TODO | `data/schema.sql` applied to a local SQLite file; seed sources inserted; migration log in repo | PR-003 |
| PR-006 | Static landing page (informational, honest status) | Muse | TODO | Public page: identity, status banner (what works / what does not), repo link; no forms, no fetch, no wallet | PR-002 |
| PR-007 | Transparency dashboard v0 (read-only) | Muse | TODO | Public page reading published rows only: counts, decision log, corrections log; no draft data exposed | PR-005 |
| PR-008 | Meme submission queue + satire labeling rules | Muse | TODO | Queue doc + labeling rules in `content/`; first 3 curated memes labeled as satire | PR-002, D-07 |
| PR-009 | Token design v1 (concept, supply, distribution, devnet plan) | Muse | TODO | `docs/token-design.md` completed with concept decided by Rama; devnet steps listed; mainnet gates stated | D-04, D-05 |
| PR-010 | Security review by ChatGPT (ingestor SSRF guard, auth model, secrets policy) | ChatGPT | TODO | Written review in repo; findings tracked as issues/items, not just comments | PR-004 |
| PR-011 | Threat model: impersonation (fake token, fake accounts, fake news sites) | Muse + ChatGPT | TODO | `docs/risks.md` § impersonation completed with detection + response plan | PR-009 |
| PR-012 | Token launch website Phase 1 (static site: landing + About/Token/Launch/Transparency/Roadmap) | Muse | **DONE** (2026-11-09 ~02:35 WIB) | `apps/token-site/` 16 files, 6 routes, zero-dep static per `docs/frontend-stack-decision.md`; checks: routes 8/8 HTTP 200, HTML 6/6, contrast AA pass, screenshots in `apps/token-site/evidence/`; commits `15b3b6f`, `91cdf4a`, `63757c9`; facts discipline kept (supply shown proposed with NO number — D-05a still open) | Website handoff (ChatGPT 02:16 WIB) |
| PR-013 | Review and prepare token-site for public preview | Muse + ChatGPT | **IN REVIEW — NOT ACCEPTED** (PR #4; latest head `7ae3174b72980cf1829a7c7ab3d73d72173fcb0f`) | Latest CI run `42556069910` SUCCESS: 8/8 routes, 6/6 HTML/copy/security/heading checks, click-based nav test 3/3, 12/12 fresh screenshots; artifact `13647213466`, ZIP SHA-256 `db3e3f41fd88c051edb86cec78d1cbf1b24e98f6158bf7560a4d5d137ff83742`, manifest SHA-256 `3088b07ca6e422ff82ca904812b66fa851b6247d8d23de7a930f9d78f7f0f91c`, 20/20 checksums verified (see PR comment `6732082342`). Remaining: real keyboard-only sequence/focus matrix; browser/OS reduced-motion verification; broader WCAG review; founder decision on public GitHub URL exposing owner handle; deliberate sync with current main. No deployment.
| PR-014 | REFORMASI whitelist architecture and secure participation flow | Muse (design) + ChatGPT (security review) | **DESIGN ONLY — SECURITY REVIEW REQUIRED** (PR #5, head `e4d997a00ddf2da8cec64fe60225abed92681526`) | Three options compared; no provider selected. ADR specifies caller JWT/RLS, restricted service-role, server-side AAL2, tamper-evident audit log with external anchor, manual Telegram/Discord verification, and first-party pricing/region evidence gate. Remaining: explicit applicant-isolation and AAL1-deny/AAL2-allow test plan; reconcile shared docs after PR-013 acceptance; founder decisions on provider/region/login/MFA recovery/email/retention/privacy/quota/selection. No backend or applicant data.

## Notes

- Phase 1 is **docs + skeleton + dry-runs**. No live service, no mainnet, no real token.
- Backlog changes go through the repo (commit), not chat. Rama approves scope changes; ChatGPT audits security-relevant items.
- If a PR is blocked (e.g. awaiting a Rama decision), record the blocker + what was tried + the alternative path, per the sustainability principles used on AG-001. Do not go silent, do not fake progress.
