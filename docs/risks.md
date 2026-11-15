# POLITIK RIUH — Risk Register

- **Date:** 2026-11-09
- **Status:** Initial register (Phase 1). Severities are initial judgments, not audit verdicts. ChatGPT to review (PR-010).
- **Scale:** High / Medium / Low. Status: OPEN / MITIGATED (dev) / ACCEPTED (owner decision).

## 1. Security risks

| ID | Risk | Severity | Description | Mitigation (Phase 1) | Status |
|---|---|---|---|---|---|
| R-S01 | SSRF in the news ingestor | High | The ingestor fetches external URLs. An attacker-controlled feed URL could probe internal networks or exfiltrate via redirects — the same class as AG-001 F-001. | Allowlist hosts; block private/link-local/reserved IPs; redirect limits; per-request timeout; response size cap; no fetch of non-allowlisted hosts. | OPEN (design stated, guard not yet implemented — PR-004/PR-010) |
| R-S02 | Secret / credential leakage | High | A key or token committed to the repo (or pasted in chat) is public forever. | `.gitignore` covers `.env`, keys, DBs; no secrets in docs; pre-commit habit: `git status` review before every push. | OPEN (policy stated) |
| R-S03 | Token impersonation / scam copies | High | Once a token concept is public, scammers deploy same-name tokens and fake "official" channels. | Official contract published only via this repo + official channels; no presale; no paid launch services; impersonation threat model (PR-011). | OPEN |
| R-S04 | Admin/editorial account takeover | Medium | Editorial workspace (Phase 2) becomes a target: publish false "verified" claims. | Phase 1 has no auth surface (repo-driven). Phase 2 auth must be reviewed by ChatGPT before build. | OPEN (deferred to P2 by design) |
| R-S05 | Dependency supply chain | Medium | A compromised dependency could exfiltrate data or inject content. | Minimal dependencies, lockfiles, no install scripts from untrusted sources. | OPEN |
| R-S06 | Scraping / scraping-abuse of our own site | Low | Bots scrape the dashboard or spam the meme queue. | Rate limits and manual curation in Phase 2; no user accounts in Phase 1. | OPEN |
| R-S07 | Whitelist applicant data exposure | High | Email, wallet address, X handle, and evidence become linkable applicant data if stored or exposed together. | Protected backend/database, TLS, encryption at rest, least privilege, no applicant data in GitHub/static assets/logs, privacy notice/consent, retention and deletion workflow. | OPEN — whitelist not implemented |
| R-S08 | Admin account takeover | High | A compromised admin account could alter tasks, quota, evidence decisions, or applicant outcomes. | Server-side RBAC, MFA, short-lived sessions, rate limits, audit trail, and recovery procedure. | OPEN — architecture pending |
| R-S09 | False task verification | High | Self-attested likes/follows/reposts may be presented as independently verified without reliable API evidence. | Per-task verification mode; API capability matrix; otherwise manual review or self-attestation; only VERIFIED unlocks dependencies. | OPEN — whitelist not implemented |
| R-S10 | Whitelist abuse / duplicate applications | Medium | Bots, duplicate emails/wallets, or coordinated submissions may distort eligibility and review. | Server-side validation, rate limits, email verification, duplicate detection, evidence review, auditable admin flags. | OPEN — whitelist not implemented |

## 2. Editorial risks

| ID | Risk | Severity | Description | Mitigation (Phase 1) | Status |
|---|---|---|---|---|---|
| R-E01 | Defamation / UU ITE exposure (Indonesia) | High | Publishing an unverified claim about a named person can create real legal liability under Indonesian defamation / ITE provisions. | Human verification before any "verified" label; named-person claims need two independent sources + evidence links; corrections log; satire never presented as fact. | OPEN (policy draft — PR-002) |
| R-E02 | Hoax / misinformation amplification | High | The monitor can become a megaphone for the very hoaxes it tracks if unverified items are displayed as news. | Unverified items are labeled `unverified` and never shown as verified; no auto-publish; provenance required. | OPEN |
| R-E03 | Satire mistaken for news | High | A satirical meme shared out of context reads as a real claim. | Satire is watermarked/labeled in-image and in-caption; separate gallery; no satire in the news feed. | OPEN |
| R-E04 | Source bias / selective verification | Medium | Verifying only claims that fit one side destroys credibility. | Source list spans outlets (PR-003); verification criteria are written and public; decision log is public. | OPEN |
| R-E05 | Political pressure / takedown demands | Medium | A political actor may demand removal of a verified item. | Decision log records removals with reasons; no silent deletion; Rama decides, with the reason published. | OPEN |
| R-E06 | Doxxing / personal data in content | Medium | A meme or article could expose private addresses, phone numbers, family members. | Editorial policy forbids personal data; meme queue is curated, not auto-published. | OPEN |

## 3. Technical risks

| ID | Risk | Severity | Description | Mitigation (Phase 1) | Status |
|---|---|---|---|---|---|
| R-T01 | RSS feed churn / dead feeds | Medium | Outlets change or block RSS without notice; the monitor silently goes stale. | Liveness checks in PR-003; dead feeds logged, not hidden; dashboard shows per-source freshness. | OPEN |
| R-T02 | Single-maintainer bottleneck | Medium | Rama is the only final decision-maker; ChatGPT/Muse cannot approve scope. | Backlog records blockers + alternatives; decisions are batched and asked once, not drip-fed. | OPEN (accepted) |
| R-T03 | No staging environment | Medium | Changes go straight to the public repo/site with no staging check. | Phase 1 is docs/static only (blast radius ~zero); staging decision deferred to the first live service. | OPEN |
| R-T04 | SQLite concurrency limits | Low | A single SQLite file will not serve concurrent writers if the project grows. | Phase 1 is single-writer by design; revisit only on evidence of contention. | OPEN (accepted) |
| R-T05 | Token/economic conflict of interest | Medium | If the team holds the meme token, editorial choices could be (or appear to be) price-driven. | Holdings disclosure on the dashboard; token never influences verification; no editorial decision may reference token price. | OPEN (policy — PR-002) |

## 4. Impersonation (detail — feeds PR-011)

- Fake token contracts with the same name/ticker on Solana (and copycats on BSC).
- Fake X/Telegram accounts claiming to be POLITIK RIUH.
- Fake "official" news sites mimicking monitored outlets.
- Response plan (draft): publish the single official contract address (devnet first) in this repo; publish the official account list; community reporting channel; takedown requests where the platform supports them; never engage with impersonators from official accounts beyond a single pinned warning.
