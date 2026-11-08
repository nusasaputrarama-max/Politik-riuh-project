# REFORMASI Whitelist — Architecture Decision Record (PR-014)

- **Date:** 2026-11-09
- **Status:** DESIGN ONLY — no code, no live form, no database, no email sending, no deployment.
- **Author:** Muse (engineering partner)
- **Reviewer:** ChatGPT (security review pending)
- **Decision owner:** Rama (founder). No provider is selected by this document.
- **Requirements baseline:** `docs/whitelist-spec.md` v0.1 (owner-approved, issue #1)
- **Related:** `docs/website-audit-2026-11-09.md`, `collaboration/MUSE_WHITELIST_HANDOFF.md`, GitHub issue #3

> **Boundary.** This record compares architectures and specifies enforcement. It does not authorize building the backend, collecting applicant data, sending email, or deploying anything. Each of those steps needs a separate founder decision after ChatGPT's security review of this record.

## 1. What the system must do

From `docs/whitelist-spec.md`:

- **Registration (free):** active email + Solana public wallet address typed as text (base58, validated server-side) + X handle. No wallet connection, signature, seed phrase, or transaction.
- **Email verification** before an application can progress.
- **Sequential tasks** (follow official X, repost/like a designated post, join Telegram/Discord, or other configured actions) with states LOCKED / OPEN / SUBMITTED / DONE / VERIFIED / NEEDS REVIEW. The server is authoritative; self-attestation is never shown as VERIFIED.
- **Applicant dashboard** (returning-applicant login TBD) and **admin panel** (task/deadline/evidence/quota/review/export controls).
- **Hybrid selection:** system eligibility + anti-abuse checks, then human admin review. Quota is admin-configurable and undecided — never hardcoded.
- **Privacy/security:** applicant records are private; email never public; evidence private to applicant + authorized reviewers; append-only audit trail; rate limits; duplicate detection; retention/deletion defined before collection.
- **Scale assumption for this record:** up to ~1,000 applicants in the first whitelist round; ~5 tasks each; a few evidence screenshots per applicant. If the round grows past ~5,000 applicants, re-check the cost/limits section (§5) before opening registration.

## 2. Options compared

Three viable architectures. All three keep the public site (`apps/token-site/`) static and put all applicant data behind a separate backend — the static site must never collect, store, or display applicant data.

### Option A — Managed BaaS: Supabase (Postgres + Auth + Storage + Edge Functions)

| Layer | Implementation |
|---|---|
| Backend / API | Supabase Edge Functions (Deno/TypeScript) + PostgREST auto-API, with Row Level Security (RLS) as the authorization layer; all privileged writes go through Edge Functions with the service key server-side only |
| Database | Managed Postgres (Supabase). Tables: applicants, tasks, task_states, evidence (metadata only), decisions, audit_log, admin_config |
| Applicant login | Supabase Auth, email magic link (passwordless) — no password to store; session JWT, short expiry, refresh rotation |
| Admin auth | Supabase Auth + a separate admin allowlist table; TOTP MFA enforced in Auth; admin dashboard is a separate app/route that never ships the service key |
| Email verification | Supabase Auth built-in email (magic link doubles as verification) + a transactional provider (e.g. Resend) via SMTP for status mail; verify sender domain before use |
| Hosting | Supabase cloud (region selectable, e.g. Singapore for SEA latency); static site stays on GitHub Pages (separate, PR-013) |
| Secrets | Supabase dashboard secrets + Edge Function secrets; service-role key never in browser code; rotate on admin change |
| Backups | Free tier: none included — manual `pg_dump` exports. Pro: daily backups + point-in-time recovery (add-on) |
| Audit log | Append-only `audit_log` table (insert-only RLS policy; no UPDATE/DELETE grants for any role), plus Supabase Auth admin audit events |

### Option B — VPS self-hosted: Hetzner VPS + Docker + Postgres

| Layer | Implementation |
|---|---|
| Backend / API | Small Node.js/TypeScript (or Python/FastAPI) API in Docker behind Caddy/Nginx (TLS via Let's Encrypt); REST only, no auto-generated API surface |
| Database | Self-managed Postgres 16+ in Docker on the same VPS (separate volume); nightly `pg_dump` to encrypted off-site object storage |
| Applicant login | Email magic link implemented in the API (signed, single-use, 15-minute tokens stored hashed) — or self-hosted auth (e.g. Auth.js / better-auth) |
| Admin auth | Separate admin accounts in the API DB; TOTP MFA (e.g. `otplib`); admin sessions are HTTP-only, SameSite=strict cookies; admin panel served from the same VPS on an allowlisted path |
| Email verification | Transactional provider (e.g. Resend/SES) via API key in the VPS secret store; SPF/DKIM/DMARC on the sender domain |
| Hosting | Hetzner Cloud VPS (EU or Singapore), UFW firewall + fail2ban, automatic security updates, SSH key-only |
| Secrets | Environment file on the VPS (0600, owned by the app user) + a documented rotation procedure; no secrets in the repo |
| Backups | Nightly encrypted `pg_dump` + weekly full-volume snapshot; restore tested before launch |
| Audit log | Append-only `audit_log` table (DB role without UPDATE/DELETE on that table) + append-only file log shipped off the VPS |

### Option C — Serverless edge: Cloudflare Workers + D1 + R2

| Layer | Implementation |
|---|---|
| Backend / API | Cloudflare Workers (TypeScript) as the API; Workers secrets for keys; Turnstile for bot protection on the form |
| Database | D1 (serverless SQLite): applicants, tasks, states, decisions, audit_log. 10 databases/account, 5 GB total on free tier |
| Applicant login | Email magic link implemented in the Worker (signed tokens in D1, hashed) — Cloudflare has no built-in passwordless auth product; Access is not a substitute for applicant login |
| Admin auth | Separate admin login in the Worker + TOTP; admin routes protected by a Worker middleware allowlist; optional Cloudflare Access as a second gate in front of the admin path |
| Email verification | Transactional provider (e.g. Resend) called from the Worker; sender domain verified with SPF/DKIM/DMARC |
| Hosting | Cloudflare edge (global); static site could also move to Pages, but that is a separate decision |
| Secrets | Cloudflare Workers secrets (dashboard/API); per-environment (staging/production) separation |
| Backups | D1 has no automatic backup on the free tier — scheduled Worker exports D1 to R2 (SQL dump) nightly; restore is a manual re-import |
| Audit log | Append-only table in D1 (no UPDATE/DELETE in the Worker code path) + R2-archived JSON lines |

### Comparison matrix

| Criteria | A — Supabase | B — VPS (Hetzner) | C — Workers + D1 |
|---|---|---|---|
| Time to a reviewed MVP | Fastest: auth, DB, storage, email-verify in one product | Slowest: build auth, mail, backups, hardening by hand | Medium: API is fast, but auth + backups must be built |
| Ops burden (solo anonymous team) | Low: patching/backups/HA are the vendor's | High: OS patching, Postgres, TLS, monitoring are ours | Low: no servers; backup export still ours |
| Applicant login quality | Best: battle-tested Auth, magic links, MFA, session handling | Depends on our implementation; easiest to get wrong | Depends on our implementation; easiest to get wrong |
| Admin MFA | Built-in TOTP enforcement | Must implement (TOTP lib + enrolment flow) | Must implement (TOTP lib + enrolment flow) |
| Evidence storage | Storage buckets with signed URLs, RLS policies | Disk/object storage on the VPS; signed URLs must be built | R2 with presigned URLs; access rules in the Worker |
| Audit trail | Postgres table + RLS; Auth admin events included | Postgres table + file log; must wire log shipping | D1 table + R2 archive; must wire export |
| Backups at $0 | None (manual export only) | Manual (scripted, we own it) | Manual (scheduled export to R2) |
| Scale headroom at $0 | 500 MB DB, 50k MAU, 1 GB storage, 5 GB egress; **pauses after 1 week idle** | Full VPS resources; no pause; ~20 TB traffic | 100k req/day, D1 5M rows read/day, R2 10 GB-month |
| Vendor lock-in | Low: plain Postgres — `pg_dump` restores anywhere; Auth user export is the awkward part | Lowest: everything is standard OSS, movable by re-provisioning | Medium: D1 is SQLite-compatible but Workers APIs (KV/R2 bindings, D1 API) are Cloudflare-specific; migration = rewrite of the data layer |
| Data residency control | Region selectable at project creation; data lives in that region | Full control: pick the datacenter (EU/Singapore) | Edge-distributed by design; D1 data location is less directly controllable |
| Failure modes | Free-tier pause; vendor outage; RLS misconfiguration = data leak | VPS compromise = full data access; missed patching; disk full | Daily quota exhaustion = hard errors until UTC reset; D1 restore is manual |

## 3. Data flow

```
                         ┌─────────────────────────────┐
                         │  Static site (GitHub Pages) │
                         │  apps/token-site/ (no data) │
                         └──────────────┬──────────────┘
                                        │ HTTPS, public pages only
                                        ▼
┌──────────┐   1. register    ┌─────────────────────────┐
│ Applicant│ ───────────────► │  API / Edge Function    │   TRUST BOUNDARY
│ (browser)│   email+wallet   │  - validate (server)    │   browser is untrusted:
│          │   + X handle     │  - rate limit, dedupe   │   it never decides state
└──────────┘                  └────────┬────────────────┘
   ▲  2. magic link (email)            │ 3. store (encrypted at rest)
   │                                   ▼
   │                          ┌─────────────────────────┐
   │                          │  Database (private)     │
   │                          │  applicants, tasks,     │
   │                          │  states, evidence meta, │
   │                          │  decisions, audit_log   │
   │                          └────────┬────────────────┘
   │                                   │ 4. task state machine
   │                                   ▼
   │                          ┌─────────────────────────┐
   │                          │  Verification worker    │
   │                          │  (API checks where      │
   │                          │  supported; else queue   │
   │                          │  for manual review)     │
   │                          └────────┬────────────────┘
   │                                   │ 5. outcome → state
   ▼                                   ▼
┌──────────┐   6. dashboard   ┌─────────────────────────┐
│ Applicant│ ◄─────────────── │  API (own rows only)    │
│ dashboard│   own data only  └─────────────────────────┘
└──────────┘
                                        ▲
┌──────────┐   7. admin panel  ┌───────┴─────────────────┐
│  Admin   │ ───────────────► │  Admin API (MFA + RBAC) │
│ (MFA)    │   review/approve │  - evidence review      │
└──────────┘   quota/config   │  - quota + task config  │
               export (auth)  │  - append-only audit    │
                              └─────────────────────────┘
```

Written flow:

1. **Register.** Browser posts email + Solana address + X handle. The API validates server-side (email format + MX sanity, base58 decode to 32 bytes, X handle normalization), checks duplicates on normalized email/handle/wallet, applies rate limits, then creates the applicant in state `Pending` and sends a verification email. Nothing is stored in the browser.
2. **Verify email.** Applicant clicks the magic link (single-use, 15-minute expiry). Only then can tasks start.
3. **Tasks.** The API serves the task list with per-task state. A task becomes OPEN only when its prerequisites are VERIFIED. The browser can claim completion (SUBMITTED/DONE) but cannot set VERIFIED.
4. **Verify.** For each submitted task the verification worker runs the configured mode (§8): a supported platform API check, or queues the evidence for manual review. Results, timestamps, and evidence references are recorded.
5. **Apply.** When all required tasks are VERIFIED, the Apply action unlocks. Applying moves the applicant to `Under Review` — it does not approve them.
6. **Review.** An admin (MFA, RBAC) reviews evidence, approves/rejects with a reason, and the decision is written to the append-only audit log. Quota changes are likewise logged with who/when.
7. **Export.** Only approved public Solana wallet addresses may be exported, only when operationally necessary and authorized; emails are never exported.

Trust boundaries: (a) browser ↔ API — the browser is untrusted, all state transitions are server-side; (b) API ↔ database — least-privilege DB roles, parameterized queries only; (c) admin ↔ API — MFA + RBAC + audit; (d) verification worker ↔ platform APIs — credentials server-side only, responses logged without PII.

## 4. Threat model (summary)

| Threat | Impact | Mitigation (all options) |
|---|---|---|
| Fake registrations / Sybil (many wallets, one person) | Quota gaming, unfair selection | Rate limits, duplicate detection on normalized email/handle/wallet, evidence review, admin flagging; no purely automated approval |
| Applicant reads another applicant's data (IDOR) | Privacy breach | Applicant isolation: every query scoped to the authenticated applicant id; no predictable public URLs; RLS or equivalent server-side check on every row |
| Client-side state tampering (unlock tasks, fake VERIFIED) | Bypass of eligibility | Server is authoritative; task transitions validated against prerequisites in the backend; browser state is display-only |
| Evidence forgery (fake screenshots) | False verification | Screenshots are supporting evidence only; API-verifiable tasks use platform data, not images; manual review checks post URLs/timestamps |
| Admin credential theft / session hijack | Full applicant data + selection control | MFA required; short sessions; separate admin login; audit log of every privileged action; alerts on new admin sessions (if the provider supports them) |
| Secret leak (service key, mail key, platform tokens) | Full backend access | Secrets in provider secret store only; never in repo/browser; rotation procedure; least-privilege keys |
| Email enumeration / spam | Harassment, phishing surface | Generic responses ("if this email is registered, a link was sent"); rate limits on verification sends; SPF/DKIM/DMARC |
| Platform API key abuse / quota burn | Cost, verification outage | Server-side keys only; per-applicant verification budget; verification jobs queued and capped (§8) |
| Data breach / ransomware on the host | Applicant PII exposure | Encryption at rest (provider default), encryption in transit (TLS), least-privilege access, backups kept off the same host, deletion workflow |
| Insider / rogue admin | Silent selection manipulation | Append-only audit log; quota/selection changes need a recorded reason; exports logged; two-person review for the final selection list (process rule, not code) |

## 5. Cost at current scale (snapshot 2026-11-09 — verify before deciding)

Assumptions: ~1,000 applicants, ~5 tasks each, ~3 emails per applicant (verification + 2 status mails), evidence screenshots ~200 KB each, ≤3 per applicant. All prices below are **snapshots from secondary summaries of vendor pricing pages, read 2026-11-09** — re-check the vendor's own pricing page before any purchase.

| Item | Option A — Supabase | Option B — VPS | Option C — Workers + D1 |
|---|---|---|---|
| Hosting / compute at $0 | Free tier $0 (500 MB DB, 50k MAU, 1 GB storage, 5 GB egress, 500k function calls/mo) — **pauses after 1 week idle; no backups** | VPS ~€4–6/mo (Hetzner CX22 class, 2 vCPU/4 GB; prices rose twice in 2026 and CX stock was reported unavailable in Nov 2026 — verify availability) | Free tier $0 (100k req/day, D1 5M rows read/day, R2 10 GB-month) |
| Realistic production cost | **Pro $25/mo** (removes pause, 8 GB DB, 100 GB storage, daily backups) + compute overages | ~€5/mo VPS + ~€1/mo snapshot/backup + domain ~$10–15/yr | **Paid $5/mo min** (10M req/mo) once daily caps are a risk; R2/D1 overages small at this scale |
| Email (~3,000 mails/round) | Auth emails included in MAU allowance; bulk/status mail via Resend-type provider free tier (verify current limits at decision time) | Same transactional provider as A | Same transactional provider as A |
| X API verification (§8) | **Not free.** Pay-per-use since 6 Feb 2026: ~$0.005 per post read, ~$0.010 per profile read. One full verification pass over 1,000 applicants × ~3 X tasks ≈ **$15–45 in reads** (estimate; excludes OAuth app review time). Budget separately; default is manual review. | Same as A | Same as A |
| Telegram / Discord verification | $0 (Bot API / gateway, free) | $0 | $0 |
| Domain + TLS | ~$10–15/yr domain; TLS free (Let's Encrypt / provider) | Same | Same |
| **Total, first round (excl. X API)** | **$0 prototype / ~$25/mo production** | **~€6/mo + ops time** | **$0 prototype / ~$5/mo production** |

Notes: the $0 tiers are all usable for a **staging prototype with dummy data**; none of them is acceptable for real applicant data without the paid step that adds backups and removes pausing/quotas (A: Pro; B: backup add-on; C: Paid + scheduled D1 export). Ops time is the real cost of Option B: patching, monitoring, and incident response fall on a solo anonymous team.

## 6. Residency, privacy, abuse control, recovery, lock-in

- **Data residency.** Applicant data is Indonesian users' personal data (email + X handle + wallet). Option A: pick the region at project creation (Singapore is the nearest Supabase region; changing it later means migrating). Option B: pick the datacenter (Hetzner Singapore or EU). Option C: edge-distributed; D1 storage location is not directly selectable — weakest residency story. **Decision for Rama:** which jurisdiction the applicant database lives in.
- **Privacy.** Minimize collection to the three registration fields + task evidence (§1). Emails are never logged in plaintext, never exported, never put in analytics. Evidence files are private objects (signed URLs, short expiry) visible only to the applicant and reviewers. No third-party analytics on the registration flow. A privacy notice + affirmative consent screen is required before the first field is submitted (wording is a founder decision).
- **Abuse controls.** Per-IP and per-email rate limits on registration, verification sends, evidence uploads, and login attempts; CAPTCHA/Turnstile on the public form; duplicate detection on normalized email, X handle, and wallet; velocity alerts (e.g. >50 registrations/hour); evidence upload size/type limits; admin flagging workflow.
- **Recovery / rollback.** Backups: A Pro daily + PITR add-on; B nightly encrypted dump + snapshot; C nightly D1 export to R2. Restore must be **tested before launch** (a backup that was never restored is not a backup). Rollback of the application: redeploy the previous known-good version (all options support versioned deploys); rollback of data: restore from the last backup — never "undo" by editing the audit log. If the whitelist must be shut down, the procedure is: freeze new registrations, export the decision record, then delete applicant data per the retention policy.
- **Vendor lock-in.** A: low (plain Postgres; Auth is the sticky part). B: lowest (standard OSS). C: medium (Workers/D1 APIs). Exit plan for any option: nightly Postgres/SQL dump in an open format stored outside the provider, so a move is a re-provision, not a rescue.

## 7. Enforcement specification (binding for implementation)

These are requirements, not suggestions. Implementation must demonstrate each one in review before registration opens.

- **Admin MFA.** TOTP (authenticator app) required for every admin account; no admin login without a second factor; enrolment and recovery codes handled by the founder, never stored in the repo.
- **RBAC.** At minimum two roles: `admin` (task/quota/config, approve/reject) and `reviewer` (evidence review only, no quota/config, no export). The service-role key is never held by a reviewer. Permissions are checked server-side on every request, not in the UI.
- **Applicant isolation.** Every applicant query is scoped to the authenticated applicant id. No sequential public ids; use random UUIDs. No applicant data in URLs, logs, or error messages.
- **Retention / deletion.** Retention period is a **founder decision** (propose: delete non-approved applicant records 90 days after the round closes; keep the anonymized selection record permanently). Deletion must remove the applicant row, evidence files, and auth identity, and be recorded in the audit log as "applicant deleted" without copying the PII into the log. A contact address for deletion requests must exist before registration opens.
- **Evidence privacy.** Evidence is stored as private objects with signed, short-lived URLs; metadata (not file contents) in the DB; access logged; reviewers see evidence only for applicants assigned to them.
- **Rate limits.** Registration 5/hour/IP + 3/day/email; verification sends 3/hour/email; evidence uploads 10/hour/applicant; login attempts 5/15 min; admin login 5/15 min + lockout alert. Limits are enforced server-side and return generic errors.
- **Append-only audit record.** `audit_log` accepts INSERT only (no UPDATE/DELETE grants for any application role). Each record: timestamp, actor (admin id or `system`), action, target id, reason/category, and a hash of the previous record (hash chain) so tampering is detectable. Personal data is never copied into audit records.
- **Secrets.** Provider secret store only; separate secrets per environment (staging vs production); rotation on any admin change or suspected leak; no secrets in Git, chat, or the static site.
- **Input handling.** Parameterized queries everywhere; strict validation of email, base58 Solana address (decode to 32 bytes, reject `0x` EVM addresses), and X handle format; URL allowlisting for task targets; HTML-escaping of all untrusted text.

## 8. Verification capability matrix (X / Telegram / Discord)

Status key: **API** = verifiable by a platform API the project can actually use · **MANUAL** = human review of submitted evidence · **SELF** = applicant self-attestation only (never counts as VERIFIED).

| Task | X | Telegram | Discord |
|---|---|---|---|
| Follow official account | **MANUAL** (default). **API only if** the applicant authorizes the project app via OAuth (user context) **and** the project funds pay-per-use reads (~$0.005–0.010 per check, §5). Without both, a follow cannot be verified — do not label it VERIFIED. | n/a | n/a |
| Like a designated post | **MANUAL** (default). Same OAuth + paid-read conditions as follow; likes are user-context data and are not publicly listable. | n/a | n/a |
| Repost / quote a designated post | **MANUAL** (default). **API only if** the applicant submits their post URL and the API can fetch that post (paid read) and match it to the campaign target; quote-post text matching still needs review. | n/a | n/a |
| Join official group / channel | n/a | **API** — Bot API `getChatMember` confirms membership, free. Requires the project bot to be an admin of the group/channel. (Joining via invite link alone, without a bot check, is SELF.) | n/a |
| Join official server | n/a | n/a | **API** — bot with the privileged `GUILD_MEMBERS` intent can confirm membership, free. Requires the bot in the server with the intent enabled. |
| Submit a post / meme / creative task | **MANUAL** — reviewer checks the submitted link/content against the task brief. | **MANUAL** | **MANUAL** |
| Email ownership | **API** (own system) — magic-link verification. | — | — |
| Solana address validity | **API** (own system) — base58 decode to 32 bytes. Ownership is **not** verified (no signature is requested by design). | — | — |

Rules that follow from the matrix:

- The **default verification mode for every X follow/like/repost task is MANUAL** (or SELF where the spec allows it). API verification for X is an opt-in upgrade that needs two founder decisions: funding pay-per-use X credits, and requiring applicants to OAuth-authorize the project app.
- Never display VERIFIED for a like/follow/repost merely because the applicant clicked a button or uploaded a screenshot. A screenshot is evidence for manual review, not verification.
- Each task stores its verification mode, method, timestamp, result, and evidence reference. If a platform changes its API or pricing, the affected tasks fall back to MANUAL — they do not silently become SELF.

## 9. Recommendation

**Recommended: Option A — Supabase (managed BaaS), on the Pro plan before any real applicant data is collected.**

Rationale:

1. **Smallest ops surface for a solo anonymous team.** Auth (magic links, MFA, sessions), Postgres, RLS, Storage, and Edge Functions are one product with one dashboard. Options B and C require hand-built auth and backup plumbing — the two components most likely to be implemented insecurely under time pressure.
2. **Applicant login and admin MFA are built-in, not invented.** Supabase Auth is the only option where magic-link login, TOTP enforcement, and session handling do not depend on our code being correct.
3. **Lowest lock-in among managed options.** The data is plain Postgres; a `pg_dump` restores anywhere, so the project can leave Supabase without a rewrite.
4. **Cost fits the scale.** $0 for a dummy-data staging prototype; $25/mo Pro for production, which also buys the daily backups and removes the free-tier pause that would otherwise take registration offline after a week of inactivity.
5. **Weaknesses are known and mitigable:** the free tier must never hold real data (pause + no backups); RLS policies must be reviewed line-by-line before launch (an RLS mistake is a data leak); Auth user export is the awkward part of an exit.

**Not recommended as first choice:** Option B (cheapest sticker price, but the ops and security burden lands entirely on the team, including auth, patching, and incident response); Option C (good free tier and $5/mo production, but applicant auth and D1 backup/restore must be built by hand, and data-residency control is weakest).

**This recommendation does not select a provider.** Rama still decides: provider (A, B, or C), region, email sender, retention period, and whether to fund X API verification. If Rama prefers B or C, the enforcement spec (§7) and matrix (§8) still apply unchanged.

## 10. Security review checklist (before registration opens)

- [ ] RLS / authorization policies reviewed line-by-line; negative tests prove applicant A cannot read applicant B (all options: equivalent server-side checks).
- [ ] No service-role / admin key in any browser bundle, static file, or repo.
- [ ] Admin MFA enforced; reviewer role cannot change quota, config, or export.
- [ ] Audit log is append-only in practice (attempted UPDATE/DELETE fails in staging).
- [ ] Rate limits tested (registration, verification, upload, login).
- [ ] Duplicate detection tested on normalized email/handle/wallet.
- [ ] Email verification required before tasks unlock; magic links single-use + expiring.
- [ ] Evidence is private (signed URLs, short expiry); no applicant data in logs.
- [ ] Backup created **and restored** in staging; restore procedure documented.
- [ ] Privacy notice, consent wording, retention period, deletion contact, and incident contact published.
- [ ] Official X/Telegram/Discord accounts and exact campaign tasks confirmed by Rama.
- [ ] Quota and selection policy set by an admin in the system (not hardcoded); draw procedure (if any) published.
- [ ] Rollback/shutdown procedure rehearsed: freeze registrations → export decision record → delete per retention policy.
- [ ] ChatGPT security review of this record completed; findings tracked, not just commented.

## 11. What is NOT built in this PR

- No live registration form, no applicant database, no email sending, no admin endpoint, no public deployment.
- No static UI prototype is included in this PR. A future prototype may use **dummy data only** and must state clearly on every screen that it does not submit or store real applications; it must contain no form action, no `fetch()`, and no real applicant fields wired to a backend.
- No wallet connection, signing, transaction, token, mint, or funds movement of any kind.
- No secrets, credentials, or private keys in this record or the repo.

## 12. Founder decisions still required

1. Provider: A (Supabase), B (VPS), or C (Workers + D1) — and region/datacenter.
2. Applicant login method (recommended: email magic link) and session policy.
3. Admin auth provider + who holds admin accounts and MFA recovery.
4. Email delivery provider + operational sender identity + domain (SPF/DKIM/DMARC).
5. Data retention period, deletion workflow, and operational/deletion contact.
6. Official X/Telegram/Discord account URLs and exact campaign tasks.
7. Whitelist quota and selection policy (including whether any draw is used, and its auditable procedure).
8. Whether to fund X API pay-per-use verification, or keep X tasks manual-review by default.
9. Privacy notice and consent wording.
10. Final token supply, decimals, allocations, launch venue/date, and domain (separate token decisions, not this ADR).

## 13. Sources (checked 2026-11-09)

- `docs/whitelist-spec.md` v0.1 — requirements baseline (owner-approved, issue #1).
- Supabase free/pro limits: secondary summaries of Supabase's pricing page/docs, checked Sep–Oct 2026 (free: 500 MB DB, 50,000 MAU, 1 GB storage, 5 GB egress, 500k function calls/mo, pause after 1 week idle, no backups; Pro from $25/mo, 8 GB DB, daily backups). Re-check https://supabase.com/pricing before deciding.
- Cloudflare Workers/D1/R2 free limits: secondary summaries of Cloudflare's pricing/limits docs, checked Oct–Nov 2026 (Workers 100k req/day, 10 ms CPU; D1 5M rows read/day, 100k written/day, 5 GB; R2 10 GB-month; Paid $5/mo min). Re-check https://developers.cloudflare.com/workers/platform/pricing/ before deciding.
- Hetzner CX22 pricing: secondary summaries, Nov 2026 (~€3.79–5.49/mo, 2 vCPU/4 GB/40 GB NVMe; prices rose twice in 2026 and CX availability was reported limited). Re-check https://www.hetzner.com/cloud before deciding.
- X API pricing: secondary summaries of X's pricing page/changelog, Sep–Oct 2026 (pay-per-use since 6 Feb 2026; ~$0.005 per post read, ~$0.010 per profile read, $0.015 per post, $0.20 per post with a link; no free tier for new developers; legacy Basic $200/mo deprecated). Re-check the X developer pricing page before budgeting verification.
- Telegram Bot API `getChatMember` and Discord `GUILD_MEMBERS` intent: platform capabilities as documented in their respective developer docs (not re-read in this check — confirm against the official docs during implementation review).
