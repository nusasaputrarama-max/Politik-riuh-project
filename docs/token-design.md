# POLITIK RIUH — Token Design (v0.1, DESIGN ONLY)

- **Date:** 2026-11-09
- **Status:** DESIGN ONLY. No mint, no distribution, no contract — on any network.
- **Rules in force:** no Mainnet, no real tokens, no presale, no paid launch services.

## 1. Purpose

One Solana-based meme token for the POLITIK RIUH community. The token is a community/meme artifact, not an investment product, not a share in the project, and not a claim on revenue. It must never influence editorial decisions (see `docs/risks.md` R-T05).

## 2. Venue options (decision open — D-04)

| Venue | Create cost (verified 2026-11-09) | Tradeable immediately | Creator economics | Control | Notes |
|---|---|---|---|---|---|
| pump.fun | 0 SOL + network fee/rent (~0.02 SOL ballpark for first buy) | Yes — bonding curve, auto-migrates to PumpSwap at ~85 SOL buy volume | 0.30% of trades to creator | Low: supply 1B fixed, 6 decimals, name/symbol/image only | Fastest zero-capital path; ~1.4% lifetime graduation rate (May–Jun 2026 study) |
| Own SPL mint | Rent only (~0.002 SOL mint + ~0.01 SOL metadata) | No — needs a liquidity pool, which needs capital | None automatic | Full: supply, decimals, metadata, authorities | "From scratch" but not tradeable without LP funding |

Recommendation (Muse): **pump.fun for the first token** — it is the only route that yields a tradeable coin at ~zero capital. Own SPL mint remains an option for a second-phase token if LP funding appears.

Sources: pump.fun fee page (checked Oct 2026 via public guides); four.meme ~0.005 BNB for the BSC comparison (not used — chain is Solana).

## 3. Concept / name (decision open — D-05, Rama final)

Candidates carried over from the standalone meme-coin thread (2026-11-09):

| Candidate | Ticker | Lore |
|---|---|---|
| NENGOK | $NENGOK | "Nengok dulu, baru beli." — the peek-first mascot, from Rama's nickname. |
| GORENG | $GORENG | "Koin gorengan" — self-aware Indonesian shitcoin joke. |
| DER | $DER | Rama's signature address word. |

A project-native name (tied to POLITIK RIUH / "riuh" = noisy/rowdy) is also possible — e.g. a name playing on "riuh" (the noise of politics). Rama decides; no name is reserved or checked for collisions yet (uniqueness check is part of PR-009).

## 4. Supply & distribution (draft — to be fixed in PR-009)

- Supply: 1,000,000,000 (1B) if pump.fun (fixed by venue); if own SPL mint, 1B proposed for consistency.
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
