# Muse Handoff — PR-013 Review and PR-014 Whitelist Architecture
Date: 2026-11-09
Priority: Fix public-preview blockers, then prepare secure whitelist architecture.

## Read first
- `docs/website-audit-2026-11-09.md`
- `docs/website-launch-spec.md`
- `docs/whitelist-spec.md`
- GitHub issue #1 and its owner comments.

## PR-013 — finish the static token-site preview review
Current implementation exists in `apps/token-site/` and is a static six-page prototype. Do not rewrite the stack without a documented reason.

Required changes:
1. Translate all six pages and all participant-facing metadata/navigation/status/risk copy into natural Indonesian. Set `lang="id"` where the page is Indonesian.
2. Align identity to: **POLITIK RIUH presents REFORMASI**. Token name REFORMASI; proposed ticker REFORMASI pending technical compatibility check. Remove stale candidate names NENGOK/GORENG/DER from public-facing copy.
3. Update homepage, token, launch, roadmap, and site README consistently. Keep numeric supply unpublished; the 1B/10B conflict is unresolved.
4. Add an accurate distinction: whitelist registration is a free application/review flow, not a whitelist sale or guaranteed allocation. Do not imply the whitelist is live until a backend and owner-approved deployment exist.
5. Complete the GitHub Pages feasibility note: exact artifact source for `apps/token-site/`, workflow or branch options, custom-domain requirements, HTTPS behavior, environment/security implications, and rollback. Do not enable Pages or deploy.
6. Re-run the documented local checks, add reproducible commands and exit codes, refresh screenshots, and submit a PR from a feature branch.
7. Keep the site separated from `apps/web/` and do not add X automation.

Acceptance:
- Six routes and internal links pass reproducible smoke tests.
- All public copy is consistent Indonesian and REFORMASI identity.
- No unapproved tokenomics, fake metrics, fake countdowns, or claims that the token/whitelist is live.
- Mobile and desktop screenshots plus local test evidence are attached.
- Deployment feasibility and rollback are documented, but no deployment settings are changed.

## PR-014 — whitelist architecture decision record (design only)
Use `docs/whitelist-spec.md` as the requirements baseline. Before writing live forms or handling applicant data:
1. Compare at least two viable architectures for backend/API, database, applicant login, admin authentication, email verification, hosting, secrets, backups, and audit logs.
2. Provide a simple data-flow diagram or equivalent written flow.
3. Include expected cost at current scale, limits, data residency/privacy implications, abuse controls, recovery/rollback, and vendor lock-in.
4. Specify how admin MFA, role-based access, applicant isolation, retention/deletion, evidence privacy, rate limits, and append-only audit records will be enforced.
5. Provide a verification capability matrix for X/Telegram/Discord tasks. Clearly identify which actions are API-verifiable, manual-review only, or self-attested.
6. Recommend one option with rationale, but leave provider selection and privacy/retention decisions to Rama.
7. A static prototype may use dummy data only and must state clearly that it does not submit or store real applications.
8. Review `docs/token-design.md` venue economics. Attach dated primary-source URLs/evidence and show calculations for fees, creator economics, migration thresholds, and graduation claims. If a claim cannot be verified, remove it or label it unverified. Do not treat Muse's venue preference as an owner decision.

Acceptance:
- Architecture decision record committed in a feature branch/PR.
- No live registration form, database with real applicant data, email sending, admin endpoint, or public deployment.
- No private keys, seed phrases, wallet signatures, or transaction functionality.
- Security review checklist and unresolved founder decisions included.

## Current owner-approved requirements
- POLITIK RIUH presents REFORMASI; token name and proposed symbol are REFORMASI, subject to compatibility check.
- Anonymous team; hybrid satire/meme/community identity; community-first long-term priority.
- Required registration: email, Solana public wallet address (base58, typed manually), X handle.
- Sequential task flow with explicit task states; server-side dependencies and verification.
- Hybrid eligibility checks plus human selection; configurable quota remains undecided.
- Applicant dashboard; admin task/deadline/evidence/quota/review/export controls.
- API verification only where genuinely supported; otherwise manual review/self-attestation.
- No whitelist approval guarantee, no token launch claims, and no real registration until approved architecture and deployment.
