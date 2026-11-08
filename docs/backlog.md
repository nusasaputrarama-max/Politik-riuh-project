# POLITIK RIUH — Phase 1 Development Backlog

- **Date:** 2026-11-09
- **Status:** TODO, except PR-001 (done in this handoff).
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

## Notes

- Phase 1 is **docs + skeleton + dry-runs**. No live service, no mainnet, no real token.
- Backlog changes go through the repo (commit), not chat. Rama approves scope changes; ChatGPT audits security-relevant items.
- If a PR is blocked (e.g. awaiting a Rama decision), record the blocker + what was tried + the alternative path, per the sustainability principles used on AG-001. Do not go silent, do not fake progress.
