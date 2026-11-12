# POLITIK RIUH — Token Design (v0.1, DESIGN ONLY)

- **Date:** 2026-11-09
- **Status:** DESIGN ONLY. No production token, mainnet mint, distribution, or contract deployment is authorized. Any devnet-only test mint is a separate non-production test and requires Rama's separate written approval before execution.
- **Rules in force:** no Mainnet, no real tokens, no presale, no paid launch services.

## 1. Purpose

One Solana-based meme token for the POLITIK RIUH community. The token is a community/meme artifact, not an investment product, not a share in the project, and not a claim on revenue. It must never influence editorial decisions (see `docs/risks.md` R-T05).

## 2. Venue options (decision open — D-04)

| Venue | Create cost | Tradeable immediately | Creator economics | Control | Notes |
|---|---|---|---|---|---|
| pump.fun | No platform fee; network fee + account-creation deposit (see §2.1) | Yes — bonding curve; reported graduation threshold is not verified from a primary source (see §2.1) | 0.30% of bonding-curve trades to creator (verified snapshot; re-check before any decision) | Low: platform-defined supply/metadata; fee page uses 1B in market-cap calculation, while decimals still need primary-program verification | Venue remains unselected; graduation rates are window-dependent and not decision-grade without a defined sample/window |
| Own SPL mint | Network fees, account rent, and metadata costs; no budget estimate approved | No — needs a liquidity pool, which needs capital | None automatic | Full: supply, decimals, metadata, authorities | Costs must be measured from current primary requirements and a separately approved devnet test |

No venue preference is a decision: **pump.fun** and own SPL mint remain open options (D-04), and the public site states the venue as **Belum diputuskan**. A venue may only be selected after the remaining unverified items in §2.1 are resolved and the venue is compared against the project's budget and risk constraints.

### 2.1 Venue-claim verification (checked 2026-11-09, PR-013)

Primary source: **pump.fun fee page, https://pump.fun/docs/fees — "Last Updated: 17 October 2026"**, read firsthand 2026-11-09. Secondary corroboration: pump.fun public program docs, https://github.com/pump-fun/pump-public-docs (commit `639b87f`, read 2026-11-09).

| Claim | Status | Evidence / calculation |
|---|---|---|
| Create a coin: no platform fee | **VERIFIED** | Fee page: "Create a coin — No platform fee, for any pairing. You pay only the Solana network transaction fee and the small SOL deposit the network requires to create the token's on-chain accounts." |
| Bonding-curve trade fee 1.25% = creator 0.30% + protocol 0.95% | **VERIFIED** | Fee page bonding-curve table: Creator fee 0.300%, Protocol fee 0.95%, LP fee 0%, Total 1.25%. Worked example: on 100 SOL of curve volume, creator receives 0.30 SOL and the protocol 0.95 SOL. |
| Graduation (migration to PumpSwap) fee 0.015 SOL | **VERIFIED** | Fee page: "When a coin graduates … 0.015 SOL, for every coin regardless of the asset it is paired with. For a SOL-paired coin it is deducted from the bonding curve." |
| PumpSwap canonical-pool fees tiered by market cap (1.25% at 0–420 SOL down to 0.30% at 98,240+ SOL) | **VERIFIED** | Fee page SOL-denominated tier table (25 tiers): 0–420 SOL → creator 0.300%, protocol 0.930%, LP 0.020%, total 1.250%; 98,240 SOL and up → 0.050% / 0.050% / 0.200% / 0.300%. |
| App trades add a Platform Fee 0.45% (0.40% with referral) since 17 Oct 2026 | **VERIFIED** | Fee page "Platform Fee" section: 0.45% of the trade without a referral code, 0.40% with one; not charged on Terminal or third-party interfaces. A curve trade placed in the pump.fun app therefore costs 1.25% + 0.45% = 1.70% in total. |
| Supply 1B fixed, 6 decimals on pump.fun | **VERIFIED (supply) / CORROBORATED (decimals)** | Fee page states PumpSwap market cap is "the current price of the token in SOL or USDC multiplied by 1 billion tokens". Public program docs describe `create_v2` creating a Token-2022 mint with 6 decimals (per independent secondary summaries of the docs; the 6-decimal figure was not re-read in the IDL in this check). |
| Curve completes at ~85 SOL of buy volume | **NOT VERIFIED from primary source** | The fee page does not state a SOL threshold. Multiple independent secondary sources report ~85 SOL (e.g. fee-page summaries read Oct–Nov 2026; one traces the figure to pump.fun's on-chain config read 2026-11-01). Treat ~85 SOL as a reported estimate until it is read directly from the on-chain bonding-curve config. |
| "~0.02 SOL ballpark" for creation + first buy | **NOT VERIFIED as a number** | The fee page gives no SOL figure — only "network fee and the small SOL deposit". ~0.02 SOL is a recurring secondary estimate (rent + first buy). Do not budget on it; the exact creation cost must be measured on devnet first. |
| "~1.4% lifetime graduation rate (May–Jun 2026 study)" | **REMOVED — misattributed and stale** | The 1.4% figure traces to early-2025 Dune data (Foresight News, Aug 2024: ~1.8M tokens deployed, ~1.4% graduated), not to a May–Jun 2026 study. The May–Jun 2026 study (arXiv 2607.02823, 832,941 launches 8 May–10 Jun 2026) reported a pooled 0.198% rate within ~6 minutes of launch, and its v4 (Sep 2026) no longer reports a graduation rate. Other 2026 windows range ~0.63% (Sep 2025, n=655,770) to ~1.76% (Aug 2026, n=1,032,440). No single percentage is decision-grade without its sample size, window, and date. |
| "No team allocation at launch on pump.fun" (§4) | **UNCHANGED — platform mechanic, not a fee claim** | pump.fun creates the full supply on the curve/pool; the creator receives no allocation except voluntary first buys. Still to be confirmed against the current `create_v2` docs before any launch decision. |

**Fees change.** The figures above are a snapshot of the fee page last updated 17 October 2026, read 2026-11-09. Re-read https://pump.fun/docs/fees before any venue or budget decision. The four.meme BSC comparison is out of scope for Solana.

## 3. Concept / name (founder decision recorded — 2026-11-09)

- Token name: **REFORMASI** (approved by Rama in GitHub issue #1).
- Proposed symbol/ticker: **REFORMASI**, subject to technical compatibility checks before publication.
- Public copy rule (PR-013 gate item 3): the public site displays the ticker as **Belum diputuskan** until the compatibility check passes; the proposed symbol is recorded here only as a proposal, not as a decided public value.
- Brand relationship: **POLITIK RIUH presents REFORMASI**. The token website is not the separate POLITIK RIUH news portal.
- Character: hybrid Indonesian political satire, internet/meme culture, and community identity; long-term priority is community-first.
- Team identity: anonymous. Compensate with operational transparency and verifiable disclosures; do not invent biographies, audits, partnerships, or safety claims.
- The name decision does not finalize supply, decimals, allocations, vesting, venue, or launch date. Those remain separate open decisions.

## 4. Supply & distribution (draft — to be fixed in PR-009)

- Supply: **UNDECIDED**. Earlier drafts contain both 1,000,000,000 (1B) and 10,000,000,000 (10B) proposals. Neither is approved. Do not display a numeric supply or implement final tokenomics until Rama resolves the conflict.
- No presale. No team allocation at launch, on whichever venue is selected (on pump.fun the venue gives the creator no allocation except voluntary first buys).
- Creator first buy: optional, small, disclosed on the dashboard if it happens.
- No mint authority retained after launch (venue-controlled on pump.fun; explicit revoke step if own SPL mint).

## 5. Devnet plan (Phase 1 — after concept decision)

1. Concept approved by Rama (D-05).
2. Fresh Solana wallet (Phantom/Solflare) — never the drained wallet.
3. Devnet SOL from faucet (free), only after Rama explicitly approves the separate devnet test plan.
4. Only after Rama's separate written approval for a devnet test: create a test-only SPL mint on Solana devnet (CLI/Metaplex) or review the selected venue flow conceptually. A devnet test is not a production token and does not authorize mainnet activity.
5. Record: mint address, transaction signatures, holder state — in this repo under `token/devnet/`.
6. No value, no trading, no distribution on devnet.

## 6. Mainnet gates (ALL required, in order)

1. Concept approved (Rama).
2. Devnet mint + test evidence in repo.
3. ChatGPT audit of the token plan (contract/venue, supply, distribution, anti-scam).
4. Rama approves a budget only after the selected venue's current first-party fee schedule and required account-rent costs are re-checked. No fixed SOL estimate is approved.
5. Rama's explicit mainnet go-ahead (separate message, not implied by any earlier approval).

## 7. Anti-scam rules

- The official mint/contract address is published only in this repo and on official project channels. Any other address claiming to be the token is a scam until proven otherwise.
- No presale, no whitelist sale, no "guaranteed allocation", no paid launch services.
- No seed phrase / private key is ever requested, shared, or stored — for the token wallet or any other.
