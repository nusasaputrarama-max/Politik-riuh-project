# POLITIK RIUH

**Media politik independen. Membaca isu, menguji narasi, membongkar kepentingan. Berita, analisis, opini, dan satire. Politics meets meme culture.**

**Independent Indonesian political ecosystem** — political satire and meme community, one Solana meme token, and a separate future newsroom/transparency program. News monitoring, source verification, and a public dashboard are not yet implemented.

> **Status: Phase 1 — static token launch website implemented as a local prototype; whitelist and deployment are not implemented.**
> The six-page site is in `apps/token-site/`. It is not publicly deployed. No whitelist backend, no mainnet deployment, and no real token created.
> See `apps/token-site/README.md`, `docs/website-audit-2026-11-09.md`, and `docs/whitelist-spec.md`.

## Vision

1. Future political news and issue monitoring (**not implemented**).
2. Future source verification and editorial workflows (**not implemented**).
3. Political satire and meme community.
4. One Solana-based meme token.
5. Public transparency dashboard (**planned; not implemented**).

## Governance

The project team is anonymous. The founder retains final decision authority; individual identities are not published in public-facing project materials. Product, editorial, and technical decisions are recorded in GitHub.

## Rules (standing)

- Do not deploy anything to Mainnet.
- Do not create or distribute real tokens.
- Do not expose private keys or credentials.
- Do not fabricate completed work or test results.
- Keep all implementation evidence in GitHub.
- Wait for review before irreversible actions.

## Repository structure

```
.
├── README.md
├── apps/
│   ├── token-site/     # Static token launch prototype: landing + About/Token/Launch/Transparency/Roadmap
│   └── web/            # Separate future political-news portal (scaffold only)
├── services/
│   ├── ingestor/       # News/RSS monitoring → SQLite (no auto-publish)
│   └── verifier/       # Verification workflow support (states, provenance, decision log)
├── content/            # Editorial policy, meme submission queue, satire rules
├── token/              # Token DESIGN only (devnet plan). No mainnet code in Phase 1.
├── data/
│   └── schema.sql      # DRAFT SQLite schema — not applied anywhere yet
├── docs/
│   ├── architecture.md     # Initial technical architecture proposal
│   ├── backlog.md          # Phase 1 development backlog
│   ├── risks.md            # Security, editorial, technical risks
│   ├── token-design.md     # Token design (devnet only)
│   ├── website-launch-spec.md # Token-site product specification
│   ├── whitelist-spec.md   # REFORMASI whitelist requirements and security criteria
│   ├── website-audit-2026-11-09.md # Current audit and next work order
│   └── editorial-policy.md # Editorial policy draft v0.1
└── collaboration/
    └── MUSE_HANDOFF.md     # Engineering handoff → technical and founder review
```

## Docs to read first

1. `docs/architecture.md` — ecosystem architecture.
2. `docs/backlog.md` — implementation work items and status.
3. `docs/website-audit-2026-11-09.md` — latest verified token-site audit and next work order.
4. `docs/whitelist-spec.md` — owner-approved REFORMASI whitelist requirements.
5. `docs/risks.md` — security, editorial, and technical risks.
6. `collaboration/MUSE_HANDOFF.md` and `collaboration/MUSE_WHITELIST_HANDOFF.md` — engineering handoffs.

## Token launch website

The dedicated token launch prototype is in `apps/token-site/`. It is a static informational site only; there is no whitelist backend or live registration. REFORMASI whitelist requirements are in `docs/whitelist-spec.md`. No mainnet deployment, minting, wallet signing, or fund movement is authorized.
