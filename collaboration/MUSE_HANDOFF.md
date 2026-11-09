# MUSE HANDOFF — POLITIK RIUH, Phase 1 (Architecture + Scaffold)

- **From:** Muse (engineering partner)
- **To:** ChatGPT (product architect / tech lead / independent auditor) and Rama (founder, final decision-maker)
- **Date:** 2026-11-09 ~01:45 WIB
- **Repo:** https://github.com/nusasaputrarama-max/Politik-riuh-project (canonical — created by Rama 2026-11-09 ~01:50 WIB; the Phase 1 work was first pushed to `politik-riuh`, a duplicate repo I created because the named repo did not exist yet, then moved here. The duplicate is left untouched pending Rama's decision to delete it.)
- **Tagline (Rama):** "Media politik independen. Membaca isu, menguji narasi, membongkar kepentingan. Berita, analisis, opini, dan satire. Politics meets meme culture."
- **Status of this handoff:** submitted for review. Nothing here is approved until Rama and ChatGPT say so.

## 1. Two facts the invitation assumed that were not true

1. **The repo did not exist.** `gh repo view nusasaputrarama-max/politik-riuh` returned "Could not resolve to a Repository". I created it as **public** (same visibility as `Airdrop-Generate`) so the handoff could be filed in GitHub as instructed. Rama: confirm public is right, or tell me to switch it to private.
2. **No blueprint file existed.** I searched the workspace and the Airdrop-Generate repo — no POLITIK RIUH blueprint anywhere. The architecture in `docs/architecture.md` is therefore derived from the vision statement in the invitation (5 pillars), not from a blueprint. If a blueprint exists elsewhere, point me to it and I will reconcile.

## 2. What was delivered (this commit)

| File | What it is |
|---|---|
| `README.md` | Vision, team, standing rules, structure map |
| `docs/architecture.md` | Initial technical architecture proposal v0.1 (principles, components, hosting options, security baseline, open decisions D-01…D-07) |
| `docs/backlog.md` | Phase 1 backlog PR-001…PR-011 (PR-001 done here, rest TODO with acceptance criteria) |
| `docs/risks.md` | Risk register: 6 security, 6 editorial, 5 technical risks, incl. defamation/UU ITE and token conflict of interest |
| `docs/token-design.md` | Token design v0.1 — design only, no mint; venue comparison, concept candidates, devnet plan, mainnet gates |
| `docs/editorial-policy.md` | Editorial policy draft v0.1 — needs approval (PR-002) |
| `data/schema.sql` | Draft SQLite schema v0.1 — NOT applied, no DB exists |
| `apps/web`, `services/ingestor`, `services/verifier`, `content/`, `token/`, `data/` | Skeleton folders with status READMEs (NOT STARTED) |
| `.gitignore` | Secrets, keys, DBs, build output |

No application code, no live service, no test run — there is nothing to test yet, and no test result is claimed. Phase 1 is docs + scaffold + dry-runs by design.

## 3. Architecture in one paragraph

Static-first, zero-capital, human-in-the-loop: an RSS ingestor (allowlisted feeds, SSRF-guarded, RSS fields only) writes `unverified` articles to SQLite; a human editor moves claims through `unverified → in_review → verified | disputed | false` with provenance and an append-only public decision log; the public site shows verified news, a transparency dashboard, and a separately labeled satire gallery; the Solana token is design-only in Phase 1 (pump.fun recommended — 0 SOL create + rent, instantly tradeable — vs own SPL mint, which is not tradeable without liquidity capital), isolated from all editorial data and decisions.

## 4. Decisions needed

**From Rama (final):**
- D-05 — token concept/name: NENGOK / GORENG / DER (from the earlier meme-coin thread) or a project-native name? The token is now part of POLITIK RIUH, so a project-native name may fit better.
- D-06 — source list v1: which outlets, how many, inclusion criteria?
- D-07 — satire boundaries: which figures/topics are off-limits?
- Repo visibility: public (as created) or private?
- PR-002 — approve the editorial policy draft, or amend it?

**From ChatGPT (architect/auditor):**
- D-01 — hosting: GitHub Pages static vs Hatch space artifact (AG-001 pattern)?
- D-02 — ingestor runtime: manual/cron vs GitHub Actions schedule?
- D-03 — editorial workspace auth: repo-driven in Phase 1 vs authenticated app in Phase 2?
- D-04 — token venue: pump.fun vs own SPL mint (devnet first either way)?
- PR-010 — security review of the ingestor SSRF guard design, auth model, secrets policy.

## 5. Top risks to weigh first

1. **R-E01 (High) — defamation / UU ITE.** A political project in Indonesia carries real legal exposure. Mitigation is procedural (two sources, evidence links, corrections log), not just technical.
2. **R-S01 (High) — SSRF in the ingestor.** Same vulnerability class that gated AG-001. Guard is designed, not yet implemented.
3. **R-S03 (High) — token impersonation.** Scam copies will appear the moment a concept is public.
4. **R-E03 (High) — satire mistaken for news.** Labeling must be in-image and in-caption, not just a page header.
5. **R-T05 (Medium) — token/editorial conflict of interest.** Holdings disclosure + a hard rule: token price never influences a verdict.

## 6. What happens next (proposed)

1. ChatGPT reviews this handoff + architecture; Rama decides D-05/D-06/D-07 + repo visibility + PR-002.
2. Muse executes PR-003 (source list with liveness evidence) → PR-005 (migration 0001) → PR-004 (ingestor skeleton, dry-run) → PR-006 (landing page).
3. No mainnet, no real token, no live publishing until the gates in `docs/token-design.md` §6 and the PR-010 security review are satisfied.

## 7. Rules compliance (this handoff)

- No Mainnet deployment: none. No real token: none created. No private keys/credentials: none in repo, none requested. No fabricated work: every status above is verifiable in this repo (docs exist, code does not — and is labeled NOT STARTED). All evidence is in GitHub (this commit). No irreversible action was taken except creating the public repo itself — which Rama can delete or privatize at will.
