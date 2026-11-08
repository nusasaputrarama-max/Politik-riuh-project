# POLITIK RIUH

**Media politik independen. Membaca isu, menguji narasi, membongkar kepentingan. Berita, analisis, opini, dan satire. Politics meets meme culture.**

**Independent Indonesian political ecosystem** — news & issue monitoring, source verification, political satire & meme community, one Solana meme token, public transparency dashboard.

> **Status: Phase 1 — architecture & scaffolding (docs only).**
> No application code runs anywhere yet. No mainnet deployment. No real token created.
> See `docs/architecture.md` and `collaboration/MUSE_HANDOFF.md`.

## Vision

1. Political news and issue monitoring.
2. Source verification and editorial workflows.
3. Political satire and meme community.
4. One Solana-based meme token.
5. Public transparency dashboard.

## Team

| Role | Who | Responsibility |
|---|---|---|
| Founder, final decision-maker | Rama | Product direction, final calls, editorial policy approval |
| Product architect, tech lead, independent auditor | ChatGPT | Architecture review, technical leadership, independent audit |
| Engineering partner | Muse | Implementation, testing, technical documentation |

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
│   └── web/            # Public site: home, news monitor, dashboard, meme gallery, token page
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
│   └── editorial-policy.md # Editorial policy draft v0.1
└── collaboration/
    └── MUSE_HANDOFF.md     # Engineering handoff → ChatGPT / Rama review
```

## Docs to read first

1. `docs/architecture.md` — what we are building and how.
2. `docs/backlog.md` — Phase 1 work items (PR-001…PR-011).
3. `docs/risks.md` — what can go wrong, and mitigations.
4. `collaboration/MUSE_HANDOFF.md` — latest engineering handoff, open questions, decisions needed.
