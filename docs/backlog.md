# POLITIK RIUH — Phase 1 Development Backlog

- **Date:** 2026-11-09
- **Status:** Active. PR-001 and PR-012 are complete; PR-013 is **IN REVIEW — NOT ACCEPTED** (PR #4, awaiting ChatGPT re-review); PR-014 ADR submitted as PR #5, awaiting ChatGPT review and founder provider decisions.
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
| PR-013 | Review and prepare token-site for public preview | Muse + ChatGPT | **IN REVIEW — NOT ACCEPTED** (PR #4; source fixes and hardened harness present; public preview awaits final acceptance) | Six-page source corrected; non-deploy CI workflow `.github/workflows/token-site-pr.yml` merged into `main` via PR #6 commit `a480bb4`; PR #4 CI run `42547368159` passed at head `873ca568` (route/copy/security checks, nav toggle 3/3, screenshots 12/12). No deployment. Remaining: final manual accessibility/visual review; contrast remains a five-pair spot-check, not a full-page WCAG audit. | PR-012, owner decisions in issue #1 |
| PR-014 | REFORMASI whitelist architecture and secure participation flow | Muse (design) + ChatGPT (security review) | **ADR SUBMITTED (PR #5, 2026-11-09) — AWAITING REVIEW + FOUNDER DECISIONS** | `docs/whitelist-architecture.md`: 3 options compared (Supabase/VPS/Workers+D1), data-flow, threat model, cost, verification matrix, enforcement spec; recommendation Supabase Pro; no real applicant data or live registration before Rama approval | `docs/whitelist-spec.md`, Rama decisions |

## Notes

- Phase 1 is **docs + skeleton + dry-runs**. No live service, no mainnet, no real token.
- Backlog changes go through the repo (commit), not chat. Rama approves scope changes; ChatGPT audits security-relevant items.
- If a PR is blocked (e.g. awaiting a Rama decision), record the blocker + what was tried + the alternative path, per the sustainability principles used on AG-001. Do not go silent, do not fake progress.
