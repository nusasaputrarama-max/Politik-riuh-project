# POLITIK RIUH — Token Design (v0.1, DESIGN ONLY)

- **Date:** 2026-11-09
- **Status:** DESIGN ONLY. No mint, no distribution, no contract — on any network.
- **Rules in force:** no Mainnet, no real tokens, no presale, no paid launch services.

## 1. Purpose

One Solana-based meme token for the POLITIK RIUH community. The token is a community/meme artifact, not an investment product, not a share in the project, and not a claim on revenue. It must never influence editorial decisions (see `docs/risks.md` R-T05).

## 2. Venue options (decision open — D-04)

| Venue | Create cost (unverified working estimate) | Tradeable immediately | Creator economics (unverified) | Control | Notes (unverified) |
|---|---|---|---|---|---|
| pump.fun | 0 SOL + network fee/rent (~0.02 SOL ballpark for first buy) | Yes — bonding curve, auto-migrates to PumpSwap at ~85 SOL buy volume | 0.30% of trades to creator | Low: supply 1B fixed, 6 decimals, name/symbol/image only | Fastest zero-capital path; ~1.4% lifetime graduation rate (May–Jun 2026 study) |
| Own SPL mint | Rent only (~0.002 SOL mint + ~0.01 SOL metadata) | No — needs a liquidity pool, which needs capital | None automatic | Full: supply, decimals, metadata, authorities | "From scratch" but not tradeable without LP funding |

Preliminary Muse preference: **pump.fun** for the first token, but this is not an owner decision. It must not be treated as a recommendation until the fee, creator-economics, migration, and graduation claims above are verified from primary sources and compared against the project's budget and risk constraints.

**Source-quality warning:** the fee page and study references were not recorded as direct URLs or archived evidence in this repository. The numerical estimates and graduation-rate claim above are **unverified working notes**, not current verified facts. Do not rely on them for a venue decision or publish them until Muse attaches dated primary-source URLs/evidence and ChatGPT reviews the calculation. The four.meme BSC comparison is out of scope for Solana.

## 3. Concept / name (founder decision recorded — 2026-11-09)

- Token name: **REFORMASI** (approved by Rama in GitHub issue #1).
- Proposed symbol/ticker: **REFORMASI**, subject to technical compatibility checks before publication.
- Brand relationship: **POLITIK RIUH presents REFORMASI**. The token website is not the separate POLITIK RIUH news portal.
- Character: hybrid Indonesian political satire, internet/meme culture, and community identity; long-term priority is community-first.
- Team identity: anonymous. Compensate with operational transparency and verifiable disclosures; do not invent biographies, audits, partnerships, or safety claims.
- The name decision does not finalize supply, decimals, allocations, vesting, venue, or launch date. Those remain separate open decisions.

## 4. Supply & distribution (draft — to be fixed in PR-009)

- Supply: **UNDECIDED**. Earlier drafts contain both 1,000,000,000 (1B) and 10,000,000,000 (10B) proposals. Neither is approved. Do not display a numeric supply or implement final tokenomics until Rama resolves the conflict.
- No presale. No team allocation at launch on pump.fun (venue gives the creator no allocation except voluntary first buys).
- Creator first buy: optional, small, disclosed on the dashboard if it happens.
- No mint authority retained after launch (venue-controlled on pump.fun; explicit revoke step if own SPL mint).

## 5. Devnet plan (Phase 1 — after concept decision)

1. Concept approved by Rama (D-05).
2. Fresh Solana wallet (Phantom/Solflare) — never the drained wallet.
3. Devnet SOL from faucet (free).
4. Create token on Solana devnet (SPL mint via CLI, metadata via Metaplex) OR test the pump.fun flow conceptually (pump.fun has no devnet; devnet test = SPL mint + local checks).
5. Record: mint address, transaction signatures, holder state — in this repo under `token/devnet/`.
6. No value, no trading, no distribution on devnet.

## 6. Mainnet gates (ALL required, in order)

1. Concept approved (Rama).
2. Devnet mint + test evidence in repo.
3. ChatGPT audit of the token plan (contract/venue, supply, distribution, anti-scam).
4. Funding decision: ~0.02 SOL for creation/first buy (Rama).
5. Rama's explicit mainnet go-ahead (separate message, not implied by any earlier approval).

## 7. Anti-scam rules

- The official mint/contract address is published only in this repo and on official project channels. Any other address claiming to be the token is a scam until proven otherwise.
- No presale, no whitelist sale, no "guaranteed allocation", no paid launch services.
- No seed phrase / private key is ever requested, shared, or stored — for the token wallet or any other.
