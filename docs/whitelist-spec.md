# REFORMASI — Whitelist & Community Participation Specification
Version: 0.1
Date: 2026-11-09
Status: Owner-approved product requirements; implementation not started.

## 1. Brand and product boundary

- Presenting brand: **POLITIK RIUH**.
- Token name: **REFORMASI**.
- Proposed ticker/symbol: **REFORMASI**, subject to technical compatibility checks before publication.
- Character: hybrid of Indonesian political satire, internet/meme culture, and community identity.
- Team identity: anonymous. Compensate with operational transparency and verifiable records; do not invent biographies, audits, partnerships, locks, or safety claims.
- Long-term priority: community-first, not launch-day trading volume or token price.
- This work belongs only in `apps/token-site/`. It is not the POLITIK RIUH news portal in `apps/web/`.
- Whitelist participation is an application and review process, not a sale, guaranteed allocation, or investment benefit.

## 2. Participant registration

Required fields:
1. Active email address.
2. Solana public wallet address, entered as text (base58 Solana public key; validate decoded public-key length). Wallet connection is not required.
3. X username/handle.

Requirements:
- Verify control of the email address before allowing an application to progress.
- Validate all fields server-side; client validation is only a usability aid.
- Normalize email and X handle for duplicate checks without exposing them publicly.
- Do not request wallet connection, wallet signature, seed phrase, private key, wallet password, or transaction approval.
- Do not accept EVM `0x` addresses for the Solana wallet field.
- Do not collect additional social accounts unless an enabled task actually requires them.
- Display a privacy notice and obtain affirmative consent before collecting registration data.

## 3. Sequential task flow

A numbered task list appears below registration. Tasks are configurable by an authorized admin and can include following an official X account, reposting/quoting a designated campaign post, liking a designated post, joining Telegram/Discord, or another explicitly described action.

Each task must support:
- Stable task ID and display order.
- Title and clear instructions.
- Required or optional flag.
- Deadline and timezone.
- Target URL and official target account/post.
- Verification mode: supported platform API, manual review, or self-attestation.
- Unlock dependencies (one or more prerequisite task IDs).
- Evidence requirements and reviewer notes where relevant.
- Active/inactive state.

Later required tasks remain LOCKED until their prerequisites reach the configured qualifying state. The server is authoritative for task state; the browser must not unlock tasks by changing client-side state.

### Task states

| State | Meaning | Counts as verified completion? |
|---|---|---:|
| LOCKED | A prerequisite is incomplete, or the task is not yet available. | No |
| OPEN | The applicant can start the task. | No |
| SUBMITTED | The applicant has submitted a completion claim or evidence. | No |
| DONE | The applicant self-attests that the action is complete; it has not been independently verified. | No |
| NEEDS REVIEW | Evidence is awaiting a human reviewer. | No |
| VERIFIED | The configured verification has succeeded (supported API check or documented manual review). | Yes |

The interface must visibly distinguish self-attestation from verified completion. Never show VERIFIED for a like/follow/repost merely because the applicant clicked a button or supplied a screenshot. If an action cannot be verified reliably through a permitted API, route it to manual review or clearly mark it self-attested.

A progress indicator must show verified required tasks / total required tasks. The Apply Whitelist action becomes available only when all required tasks satisfy the configured eligibility rule. Eligibility permits review; it does not guarantee approval or selection.

## 4. Applicant lifecycle and dashboard

Applicant statuses:
- Pending
- Tasks Incomplete
- Under Review
- Approved
- Rejected

Applicants must be able to return to a dashboard and see their own task states, verified progress, current application status, and any published review outcome. The authentication mechanism for returning applicants (for example, email magic link or one-time code) must be selected and reviewed before implementation. Do not expose applicant records through predictable IDs or public URLs.

## 5. Hybrid selection

Selection is HYBRID:
1. System validates required fields, task eligibility, duplicate signals, deadlines, and anti-abuse rules.
2. Eligible applications enter human admin review/selection.
3. Admin records approval or rejection and a reason/category in an auditable decision record.

The whitelist quota is **undecided** and must be configurable by an authorized admin; never hardcode it. If a random draw is used among eligible applicants, publish the method, eligible pool definition, draw time, and auditable result. Do not imply a guaranteed selection or silently use randomness.

## 6. Admin capabilities and access control

Authorized admins must be able to:
- Create, edit, order, activate, and deactivate tasks.
- Configure deadlines, required/optional status, target URLs, verification mode, and unlock dependencies.
- Review submitted evidence and mark it valid/invalid with a reason.
- Flag duplicate or suspicious registrations.
- Set and change the quota, recording who changed it and when.
- Review eligible applicants and approve/reject them.
- Maintain an auditable selection and status-change history.
- Export only approved public Solana wallet addresses when operationally necessary and authorized.

Admin authentication and authorization must be server-side, least-privilege, and protected against session theft. Require MFA or an equivalent strong second factor for admin access. All privileged changes must be logged. Never put admin credentials or service-role keys in browser code.

## 7. Verification policy

- Use platform API verification only when the API, permissions, terms, and available data genuinely support the check.
- Maintain a per-task verification capability note and record the method, timestamp, result, and evidence reference.
- For unsupported follow/like actions, use manual review or self-attestation; never label them automatically verified.
- For repost/quote-post tasks, validate the exact campaign target and the applicant's submitted post where the platform API and permissions support it. Otherwise route to manual review.
- Do not scrape or automate interactions in ways that violate platform rules.
- Evidence must be private by default and visible only to the applicant and authorized reviewers.

## 8. Privacy and security requirements

Registration contains personal data: email, wallet address, and X handle. The wallet address is public on-chain but can be linked to an applicant; treat the combined record as private.

- Publish privacy, selection, retention, and contact/deletion information before opening registration.
- Store applicant records only in a protected backend database, never in Git commits, static files, public issue comments, analytics events, or client-side source.
- Use TLS in transit, encryption at rest, least-privilege database access, parameterized queries, and server-side authorization.
- Do not log raw email addresses, evidence payloads, authentication tokens, or full applicant records.
- Rate-limit registration, email verification, evidence submission, and admin endpoints; add abuse controls and duplicate detection.
- Escape untrusted text and validate URLs to prevent XSS, injection, and unsafe redirects.
- Keep an append-only audit trail for admin decisions and configuration changes without unnecessarily duplicating personal data.
- Define a retention period and deletion workflow before collecting data.
- No private keys, seed phrases, wallet passwords, wallet signatures, transactions, token purchases, or funds movement.

## 9. Architecture decision gate

The existing token site is static HTML/CSS/JS with no backend, database, authentication, or forms. It cannot securely collect and manage whitelist applications by itself.

Before implementing live registration, record and review:
- Backend/hosting provider and deployment ownership.
- Database and backup strategy.
- Applicant authentication and admin authentication.
- Email verification/delivery provider.
- Secret management and environment separation.
- Privacy notice, consent wording, retention period, deletion process, and incident contact.
- X/Telegram/Discord official accounts and which actions are actually verifiable.
- Operational quota and selection policy.

Do not select a provider or deploy a live form silently. A static UI prototype may use clearly labeled dummy data only; it must not accept or transmit real applicant data.

## 10. Implementation acceptance criteria

- Registration accepts only a valid email, valid Solana base58 public key, and normalized X handle; server-side validation is tested.
- Email verification is required before application eligibility.
- Task order and unlock dependencies are enforced server-side and covered by tests.
- Client self-attestation cannot produce VERIFIED or unlock a dependent task.
- Each verification mode is explicit; unsupported platform actions route to manual review/self-attestation.
- Applicant status transitions and admin actions are permission-checked and auditable.
- Admin task management and quota are configurable, not hardcoded.
- Applicant dashboard exposes only the authenticated applicant's own data.
- Email and evidence remain private; public exports contain only approved wallet addresses when explicitly authorized.
- Privacy, consent, retention, and deletion flows are present before registration opens.
- Rate limits, duplicate controls, safe input handling, and admin MFA are tested.
- No secrets are committed; no wallet signing, transactions, minting, purchase, or funds movement exists.
- Reproducible tests, desktop/mobile screenshots, deployment/rollback plan, and a security review are attached before any public registration opens.

## 11. Founder decisions still required

- Whitelist quota (must remain configurable).
- Backend/database/hosting provider and deployment ownership.
- Applicant dashboard authentication method.
- Email delivery provider and operational sender identity.
- Data retention period and deletion/contact process.
- Official X/Telegram/Discord account URLs and exact campaign actions.
- Whether any selection step uses a random draw; if yes, its auditable procedure.
- Final token supply, decimals, allocations, launch venue/date, and domain remain separate decisions.

## 12. Source decisions

This specification consolidates the founder's approved decisions recorded in the comments on GitHub issue #1 (REFORMASI whitelist requirements, hybrid/anonymous/community-first direction, and sequential task-flow reference). Those issue comments remain the source of approval. This document translates them into implementation and security acceptance criteria; it does not authorize public registration, website deployment, token creation, or launch.
