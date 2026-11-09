# POLITIK RIUH — Initial Technical Architecture (Proposal v0.1)

- **Date:** 2026-11-09
- **Author:** Muse (engineering partner)
- **Status:** PROPOSAL — awaiting review by ChatGPT (architect/auditor) and approval by Rama (founder).
- **Source note:** no project blueprint file existed at the time of writing (repo and blueprint were both absent; the repo was created as part of this handoff). This architecture is derived from the project vision in the collaboration invitation: news monitoring, source verification, satire/meme community, one Solana meme token, public transparency dashboard.
- **Rules in force:** no Mainnet, no real tokens, no private keys/credentials in repo, no fabricated evidence, review before irreversible actions.

## 1. Principles

1. **Zero-capital first.** Phase 1 uses only free tiers: static hosting, public RSS feeds, SQLite, devnet. No paid API, no paid host, no paid service.
2. **Human-in-the-loop, always.** Ingestion may be automatic; publication of any political claim is never automatic. A human editor verifies before anything is presented as verified.
3. **Satire is labeled, always.** Satire/memes live in a separate, clearly labeled space. Nothing satirical may appear in a news feed without a satire label.
4. **Public by default, editorial workspace private.** The dashboard, decision log, and verification stats are public. Drafts, reviewer identities, and moderation internals are not.
5. **Token is isolated.** No token logic touches editorial data or decisions. Token code and editorial code share a repo but not a runtime, not a database table, not a decision path.
6. **Evidence over claims.** Every verified item carries provenance: source URL, retrieved-at timestamp, reviewer, evidence links. A claim without provenance is `unverified`.
7. **Reuse hard lessons.** The ingestor fetches external URLs — the same SSRF class of risk that gated AIRDROP GENERATE (AG-001). The SSRF guard, timeouts, and allowlist discipline from AG-001 apply here from day one.

## 2. System overview

```
                        ┌─────────────────────┐
  RSS / public feeds ──▶│ services/ingestor   │──▶ articles (unverified)
                        └─────────────────────┘
                                   │
                        ┌─────────────────────┐
  Editor (human) ──────▶│ services/verifier   │──▶ claims + verifications
                        │  states + provenance│    + append-only decision log
                        └─────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
     apps/web: news        apps/web: dashboard   content/: meme gallery
     (verified only)       (stats + decisions)   (labeled satire)
                                   │
                        ┌─────────────────────┐
                        │ token/ (design only)│──▶ Solana devnet plan
                        │  NO mainnet in P1   │    (no mint in Phase 1)
                        └─────────────────────┘
```

Single data store in Phase 1: **SQLite** (one file, `data/politik-riuh.db`, git-ignored; schema in `data/schema.sql`). The public site reads only published/verified rows.

## 3. Components

### 3.1 `apps/web` — public site (Phase 1: static skeleton → read-only pages)
- Home: project identity, status banner (honest: what works, what does not).
- News monitor: monitored sources + latest items with verification status badges.
- Transparency dashboard: counts (sources, items, verified/disputed), decision log, corrections log.
- Meme gallery: satire, labeled, curated — never mixed into the news feed.
- Token page: status only in Phase 1 (design/devnet, no contract, no buy link).

### 3.2 `services/ingestor` — news monitoring
- Polls a curated allowlist of RSS feeds (Indonesian political news outlets; list in PR-003).
- Stores: source, URL, title, published-at, fetched-at. Dedup by URL hash.
- Phase 1: RSS-provided fields only. **No full-article scraping** — full fetch is a Phase 2 decision (SSRF surface, robots/ToS, copyright).
- Failure mode is fail-closed: a dead feed is logged and skipped, never retried aggressively, never presented as data.

### 3.3 `services/verifier` — verification workflow
- Claim states: `unverified → in_review → verified | disputed | false`.
- Each verification records: verdict, evidence URLs, reviewer, reviewed-at, notes.
- Every state change writes an append-only `decisions` row (who, what, why, when). Decisions are public; reviewer identities may be pseudonymous by policy.
- No auto-verification. Tooling may *suggest* (e.g. "same claim seen at 3 sources") but a human sets the verdict.

### 3.4 `content/` — editorial & community
- Editorial policy (`docs/editorial-policy.md`), meme submission queue (manual curation), satire labeling rules.
- Meme submissions are reviewed before publication. No anonymous smears, no doctored images presented as real, no defamation.

### 3.5 `token/` — Solana meme token (design only in Phase 1)
- One token, Solana. Venue decision open: pump.fun (0 SOL create + rent, instant tradeable, creator fee 0.30%) vs own SPL mint (full control, needs liquidity capital).
- Phase 1 delivers **design only**: name/concept (decision open — see §6), supply/distribution draft, devnet plan, mainnet gates. **No mint, no distribution, no contract on mainnet.**
- Mainnet gates (all required, separate approvals): concept approved by Rama → devnet mint + test evidence → ChatGPT audit → funding decision (~0.02 SOL) → Rama's explicit mainnet go-ahead.

### 3.6 `data/` — storage
- SQLite, schema draft in `data/schema.sql` (sources, articles, claims, verifications, decisions, memes). Draft status: not applied, not seeded, no data yet.

## 4. Hosting & runtime (proposal — decision open)

| Need | Phase 1 proposal | Why | Alternative |
|---|---|---|---|
| Public site | Static hosting (GitHub Pages) | Free, zero ops, honest status page | Hatch space artifact (same pattern as AG-001) if interactivity is needed |
| Ingestor | Manual run / cron on a dev machine | Free, no server to secure | GitHub Actions scheduled run (free tier) |
| Editorial workspace | Local / repo-driven in Phase 1 | No auth surface to secure yet | Small authenticated app in Phase 2 |
| Database | SQLite file | Zero cost, matches AG-001 pattern | Postgres free tier only if concurrency demands it |

Recommendation: start static + manual. Add runtime only when a concrete need (not a hypothetical) requires it.

## 5. Security baseline (from day one)

- **SSRF guard on every outbound fetch** (ingestor): allowlist schemes/hosts, no private/link-local/reserved IP ranges, redirect limits, per-request timeout, response size cap. (AG-001 F-001 class.)
- **No secrets in repo.** `.env`, keys, tokens git-ignored; no credential ever pasted into chat or docs.
- **No auto-publish, no auto-post.** Nothing in this repo posts to X/Telegram or publishes a claim without a human.
- **Dependency discipline:** lockfiles, minimal dependencies, no install scripts from untrusted sources.
- **Token anti-scam:** the official contract address (once one exists, devnet first) is published only via this repo + official channels. No presale, no paid "launch services", no DMs offering allocation.

## 6. Open decisions (for ChatGPT / Rama)

| # | Decision | Options | Needed from |
|---|---|---|---|
| D-01 | Hosting for public site | GitHub Pages static vs Hatch space artifact | ChatGPT (architect) |
| D-02 | Ingestor runtime | Manual/cron vs GitHub Actions schedule | ChatGPT |
| D-03 | Editorial workspace auth | Repo-driven (P1) vs authenticated app (P2) | ChatGPT |
| D-04 | Token venue | pump.fun vs own SPL mint (devnet first either way) | Rama + ChatGPT |
| D-05 | Token concept/name | Candidates NENGOK / GORENG / DER (from the standalone meme-coin thread) vs a project-native name | Rama (final) |
| D-06 | Source list v1 | Which outlets, how many, inclusion criteria | Rama |
| D-07 | Satire boundaries | Which figures/topics are off-limits | Rama |

## 7. Phase 1 scope (and non-goals)

**In scope (Phase 1):** repo + docs (this handoff), source list v1, schema draft → migration 0001, ingestor skeleton (dry-run), static landing page, dashboard v0 (read-only), meme queue + labeling rules, token design v1, ChatGPT security review.
**Non-goals (Phase 1):** no live news service, no auto-publishing, no mainnet, no real token, no user accounts, no comments/social features, no paid services.

## 8. Traceability

- Vision: collaboration invitation, 2026-11-09 (Rama).
- Token cost facts: four.meme ~0.005 BNB / pump.fun 0 SOL + rent — verified 2026-11-09 via public docs/reviews (see `docs/token-design.md`).
- SSRF lessons: AG-001 SSRF remediation design v2.3.29 (repo `nusasaputrarama-max/Airdrop-Generate`).
