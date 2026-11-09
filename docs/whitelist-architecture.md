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
| Backend / API | Supabase Edge Functions (Deno/TypeScript) + PostgREST. Applicant-scoped reads/writes use the caller's JWT and RLS. A service-role/secret key bypasses RLS and MUST NOT be used for the applicant request path; reserve it only for narrowly scoped server operations that independently verify identity, role, applicant scope, and required MFA assurance. |
| Database | Managed Postgres (Supabase). Tables: applicants, tasks, task_states, evidence (metadata only), decisions, audit_log, admin_config |
| Applicant login | Supabase Auth, email magic link (passwordless) — no password to store; session JWT, short expiry, refresh rotation |
| Admin auth | Supabase Auth + a separate admin allowlist table; TOTP enrolment plus server-side AAL2 enforcement on every privileged Edge Function/API and database operation. Admin dashboard is separate and never ships a service key. AAL1 and unauthenticated requests must be denied. |
| Email verification | Supabase Auth built-in email (magic link doubles as verification) + a transactional provider (e.g. Resend) via SMTP for status mail; verify sender domain before use |
| Hosting | Supabase cloud (region selectable, e.g. Singapore for SEA latency); static site stays on GitHub Pages (separate, PR-013) |
| Secrets | Supabase dashboard secrets + Edge Function secrets; service-role key never in browser code; rotate on admin change |
| Backups | Free tier: none included — manual `pg_dump` exports. Pro: daily backups + point-in-time recovery (add-on) |
| Audit log | Restricted append path with application roles denied UPDATE/DELETE; do not claim protection from the database owner. Treat the hash chain as tamper-evident and anchor periodic signed chain-head digests outside the database. |

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
| Admin credential theft / session hijack | Full applicant data + selection control | Server-side MFA assurance on every privileged operation (AAL2 for Supabase); short sessions; separate admin login; least privilege; audit log and alerts on new admin sessions where supported |
| Secret leak (service key, mail key, platform tokens) | Full backend access | Secrets in provider secret store only; never in repo/browser; rotation procedure; least-privilege keys |
| Email enumeration / spam | Harassment, phishing surface | Generic responses ("if this email is registered, a link was sent"); rate limits on verification sends; SPF/DKIM/DMARC |
| Platform API key abuse / quota burn | Cost, verification outage | Server-side keys only; per-applicant verification budget; verification jobs queued and capped (§8) |
| Data breach / ransomware on the host | Applicant PII exposure | Encryption at rest (provider default), encryption in transit (TLS), least-privilege access, backups kept off the same host, deletion workflow |
| Insider / rogue admin | Silent selection manipulation | Restricted append-only application path; external signed chain-head anchors; quota/selection changes require a reason; exports logged; two-person review for the final selection list (process rule, not code). Database-owner compromise remains a residual risk. |

## 5. Cost model and evidence quality (not decision-grade)

The scenario of ~1,000 applicants, ~5 tasks each, ~3 emails per applicant, and up to three ~200 KB evidence images per applicant is a planning assumption only, not a measured forecast.

The numeric estimates in the previous draft were assembled from secondary summaries and are **not suitable for provider selection, procurement, or budget approval**. They are removed from this ADR rather than repeated as verified prices. No provider or plan is selected here.

| Cost area | Supabase | Hetzner VPS | Cloudflare Workers + D1/R2 |
|---|---|---|---|
| Compute / base plan | Verify current plan, project region, compute limits, and overages | Verify the exact SKU available in the chosen datacenter; do not apply an EU CX price to Singapore | Verify Workers request and CPU limits, included usage, and overages |
| Data / storage | Separate database disk from object storage; verify egress and backup/PITR charges | Include disk, snapshots, off-site backup storage, traffic, IPv4, and tax | Itemize D1 reads, writes and storage separately from R2 storage, operations and egress |
| Operations | Include backup retention, restore requirements, monitoring and support | Include patching, monitoring, incident response and restore labour | Include export/restore automation, observability and quota monitoring |
| Email / identity | Price transactional email and sender-domain setup separately | Same | Same |
| Optional platform verification | X API is excluded unless separately approved and priced from current first-party terms | Same | Same |

**Cost evidence gate:** before a provider decision, attach dated links or captures from each vendor's own pricing and region documentation; state region, SKU/plan, workload units, included quota, overage rates, backup/restore costs, taxes, and one-time costs. Recalculate using the selected workload. Do not treat free-tier availability as proof that a service is suitable for real applicant PII; backups, restore testing, support, pause behaviour, and quota exhaustion must be assessed explicitly.

No purchase, subscription, domain registration, or provider provisioning is authorized by this ADR.

## 6. Residency, privacy, abuse control, recovery, lock-in

- **Data residency.** Applicant data is Indonesian users' personal data (email + X handle + wallet). Option A: choose only from the Supabase regions currently offered at project creation; verify the exact region and residency terms from first-party documentation before deciding, and assume a later region change requires migration unless the vendor confirms otherwise. Do not assume a specific region is nearest or available without checking. Option B: choose the exact Hetzner datacenter (for example, Singapore or an EU location) and verify the SKU and legal/residency implications. Option C: edge-distributed; confirm where D1 data is stored and which residency controls apply before selection. **Decision for Rama:** which jurisdiction the applicant database lives in.
- **Privacy.** Minimize collection to the three registration fields + task evidence (§1). Emails are never logged in plaintext, never exported, never put in analytics. Evidence files are private objects (signed URLs, short expiry) visible only to the applicant and reviewers. No third-party analytics on the registration flow. A privacy notice + affirmative consent screen is required before the first field is submitted (wording is a founder decision).
- **Abuse controls.** Per-IP and per-email rate limits on registration, verification sends, evidence uploads, and login attempts; CAPTCHA/Turnstile on the public form; duplicate detection on normalized email, X handle, and wallet; velocity alerts (e.g. >50 registrations/hour); evidence upload size/type limits; admin flagging workflow.
- **Recovery / rollback.** Backups: A Pro daily + PITR add-on; B nightly encrypted dump + snapshot; C nightly D1 export to R2. Restore must be **tested before launch** (a backup that was never restored is not a backup). Rollback of the application: redeploy the previous known-good version (all options support versioned deploys); rollback of data: restore from the last backup — never "undo" by editing the audit log. If the whitelist must be shut down, the procedure is: freeze new registrations, export the decision record, then delete applicant data per the retention policy.
- **Vendor lock-in.** A: low (plain Postgres; Auth is the sticky part). B: lowest (standard OSS). C: medium (Workers/D1 APIs). Exit plan for any option: nightly Postgres/SQL dump in an open format stored outside the provider, so a move is a re-provision, not a rescue.

## 7. Enforcement specification (binding for implementation)

These are requirements, not suggestions. Implementation must demonstrate each one in review before registration opens.

- **Admin MFA and assurance.** Every admin/reviewer account must enrol a second factor. For Supabase, require AAL2 server-side on every privileged Edge Function/API and on database operations; checking that a TOTP factor is merely enrolled is insufficient. Deny unauthenticated and AAL1 requests. Add tests proving AAL1 is denied and AAL2 is allowed for each privileged operation.
- **RBAC.** At minimum two roles: `admin` (task/quota/config, approve/reject) and `reviewer` (evidence review only, no quota/config, no export). Permissions are checked server-side on every request, not in the UI.
- **Supabase caller-JWT / service-role boundary.** Applicant-scoped reads and writes use the caller's JWT so RLS evaluates the applicant identity. Never route ordinary applicant requests through a service-role client. A service-role/secret key bypasses RLS; use it only in narrowly scoped server-side operations where unavoidable. Before any such operation, independently validate the caller token, role, applicant scope, requested action, and AAL2 where privileged. Never trust a client-supplied applicant ID as authorization. Keep the key in server-side secret storage only. For other providers, implement and test the equivalent least-privilege boundary.
- **Applicant isolation.** Every applicant query is scoped to the authenticated applicant id. No sequential public ids; use random UUIDs. No applicant data in URLs, logs, or error messages.
- **Retention / deletion.** Retention period is a **founder decision** (propose: delete non-approved applicant records 90 days after the round closes; keep the anonymized selection record permanently). Deletion must remove the applicant row, evidence files, and auth identity, and be recorded in the audit log as "applicant deleted" without copying PII into the log. A contact address for deletion requests must exist before registration opens.
- **Evidence privacy.** Evidence is stored as private objects with signed, short-lived URLs; metadata (not file contents) in the DB; access logged; reviewers see evidence only for applicants assigned to them.
- **Rate limits.** Registration 5/hour/IP + 3/day/email; verification sends 3/hour/email; evidence uploads 10/hour/applicant; login attempts 5/15 min; admin login 5/15 min + lockout alert. Limits are enforced server-side and return generic errors.
- **Audit-log integrity.** Application roles cannot UPDATE or DELETE audit records. Writes go through a narrowly scoped append function/role that validates actor, action, target, and reason; no PII is copied into the log. A hash chain is **tamper-evident, not immutable against a database owner**. Periodically anchor a signed chain-head digest in an independent system outside the applicant database, with access and retention documented. Test that ordinary application/admin roles cannot rewrite or delete records.
- **Secrets.** Provider secret store only; separate secrets per environment (staging vs production); rotation on any admin change or suspected leak; no secrets in Git, chat, or the static site.
- **Input handling.** Parameterized queries everywhere; strict validation of email, base58 Solana address (decode to 32 bytes, reject `0x` EVM addresses), and X handle format; URL allowlisting for task targets; HTML-escaping of all untrusted text.

## 8. Verification capability matrix (X / Telegram / Discord)

Status key: **API** = verifiable by a platform API after an approved identity-linking flow · **MANUAL** = human review of submitted evidence · **SELF** = applicant self-attestation only (never counts as VERIFIED).

| Task | X | Telegram | Discord |
|---|---|---|---|
| Follow official account | **MANUAL** by default. API verification is out of scope until applicant OAuth consent, minimum scopes, current first-party API capability/pricing, and a funded budget are separately approved. | n/a | n/a |
| Like a designated post | **MANUAL**. Do not infer a like from a screenshot or applicant click. API verification requires the same OAuth, capability, and budget gates as follow. | n/a | n/a |
| Repost / quote a designated post | **MANUAL**. A submitted post URL can support manual review; automated verification requires current API capability and separate approval. | n/a | n/a |
| Join official group / channel | n/a | **MANUAL until identity binding is designed and approved.** Future API verification would require a consent-based, single-use bot deep link that binds the applicant to the Telegram user ID, plus a bot with the required group/channel permissions. `getChatMember` alone does not prove which applicant owns a Telegram account. | n/a |
| Join official server | n/a | n/a | **MANUAL until identity binding is designed and approved.** Future API verification would require a state/CSRF-protected OAuth2 account-link flow with minimum scopes, verified callback, and a stored Discord user ID bound to the applicant. The `GUILD_MEMBERS` intent alone does not establish applicant identity. |
| Submit a post / meme / creative task | **MANUAL** — reviewer checks the submitted link/content against the task brief. | **MANUAL** | **MANUAL** |
| Email ownership | **API** (own system) — magic-link verification. | — | — |
| Solana address validity | **API** (own system) — base58 decode to 32 bytes. Ownership is **not** verified (no signature is requested by design). | — | — |

Rules that follow from the matrix:

- X follow/like/repost, Telegram membership, and Discord membership remain **MANUAL** until their identity-binding, platform permissions, API capability, privacy impact, and cost have been reviewed and separately approved.
- Never display VERIFIED merely because an applicant clicked a button or uploaded a screenshot. A screenshot is evidence for manual review, not verification.
- Each task stores its verification mode, method, timestamp, result, and evidence reference. If a platform changes its API or pricing, the affected task remains MANUAL until re-reviewed; it does not silently become SELF or VERIFIED.

## 9. Recommendation

**No provider is selected by this ADR.** Option A (Supabase) may remain a provisional architecture candidate because managed Postgres and Auth can reduce the amount of custom authentication and operations code for a small team. This is not procurement approval, budget approval, or permission to create a project.

The earlier numeric cost comparison is not decision-grade and must not be used to claim that one option is cheapest. Before choosing, compare first-party, region-specific pricing and operational requirements using the evidence gate in §5.

If Rama chooses Option A, the caller-JWT/RLS and service-role separation plus server-side AAL2 controls in §7 are mandatory. If Rama chooses Option B or C, equivalent server-side authorization, MFA assurance, least privilege, audit integrity, backup/restore and applicant-isolation controls remain mandatory; they do not become optional because the provider differs.

The decision remains with Rama: provider, region, email sender, retention period, and whether to fund any platform API verification.

## 10. Security review checklist (before registration opens)

- [ ] Applicant A cannot read or modify applicant B's records; negative tests cover every applicant-facing read/write path.
- [ ] Supabase applicant requests use caller JWT/RLS; service-role is absent from browser bundles and never used for ordinary applicant-scoped requests.
- [ ] Every privileged admin/reviewer API and database operation enforces server-side AAL2; tests prove AAL1 is denied and AAL2 is allowed.
- [ ] Reviewer role cannot change quota, config, or export; authorization is tested server-side, not only in UI.
- [ ] Audit append path is restricted; application roles cannot UPDATE/DELETE records; external signed chain-head anchoring is tested and documented. Do not claim protection from database-owner compromise.
- [ ] Telegram and Discord tasks remain MANUAL unless approved identity-linking flows are implemented and security-tested.
- [ ] X API verification remains opt-in and disabled until current first-party pricing/capability evidence and funding approval exist.
- [ ] Provider/region/plan cost worksheet uses dated first-party sources and itemizes database, object storage, egress, backups, compute, email, operations, and overages.
- [ ] Rate limits tested (registration, verification, upload, login).
- [ ] Duplicate detection tested on normalized email/handle/wallet.
- [ ] Email verification required before tasks unlock; magic links single-use + expiring.
- [ ] Evidence is private (signed URLs, short expiry); no applicant data in logs.
- [ ] Backup created **and restored** in staging; restore procedure documented.
- [ ] Privacy notice, consent wording, retention period, deletion contact, and incident contact published.
- [ ] Official X/Telegram/Discord accounts and exact campaign tasks confirmed by Rama.
- [ ] Quota and selection policy set by an admin in the system (not hardcoded); draw procedure (if any) published.
- [ ] Rollback/shutdown procedure rehearsed: freeze registrations → export decision record → delete per retention policy.
- [ ] ChatGPT security review of the revised ADR completed; findings tracked, not just commented.

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

## 13. Sources (official references; re-check before selection or implementation)

- `docs/whitelist-spec.md` v0.1 — requirements baseline (owner-approved, issue #1).
- Supabase API keys and RLS boundary: https://supabase.com/docs/guides/getting-started/api-keys
- Supabase Edge Function authentication and caller context: https://supabase.com/docs/guides/functions/auth
- Supabase MFA and assurance levels: https://supabase.com/docs/guides/auth/auth-mfa and https://supabase.com/docs/reference/javascript/auth-mfa-getauthenticatorassurancelevel
- Supabase pricing, database disk, object storage, egress and backups: https://supabase.com/pricing, https://supabase.com/docs/guides/platform/manage-your-usage/disk-size, https://supabase.com/docs/guides/platform/manage-your-usage/storage-size, https://supabase.com/docs/guides/platform/manage-your-usage/egress, https://supabase.com/docs/guides/platform/backups
- Cloudflare Workers, D1 and R2 pricing: https://developers.cloudflare.com/workers/platform/pricing/, https://developers.cloudflare.com/d1/platform/pricing/, https://developers.cloudflare.com/r2/pricing/
- Hetzner Cloud regions and pricing: https://www.hetzner.com/cloud/ and https://www.hetzner.com/cloud-singapore/
- X developer platform pricing and API capability: https://developer.x.com/en/products/x-api
- Telegram Bot API: https://core.telegram.org/bots/api
- Discord OAuth2 and privileged intents: https://discord.com/developers/docs/topics/oauth2 and https://support-dev.discord.com/hc/en-us/articles/6207308062871-What-are-Privileged-Intents

Pricing, availability, regional residency, API scopes and platform capabilities are time-sensitive. The links above are research starting points, not evidence that any provider, plan, integration, or price has been selected or approved. Capture current first-party evidence on the date of the founder's decision.
