# Muse Handoff — POLITIK RIUH Token Launch Website
Date: 2026-11-09
Priority: Start Phase 1 implementation planning and first working frontend.

## Objective
Build the dedicated POLITIK RIUH token launch website described in `docs/website-launch-spec.md`. This is a token project site, not the political news portal. Rama manages the X account; do not build X automation or post to X.

## Read first
1. `README.md`
2. `docs/architecture.md`
3. `docs/backlog.md`
4. `docs/risks.md`
5. `docs/token-design.md`
6. `docs/website-launch-spec.md`

## Visual references
- https://asciienv.xyz
- https://form.elysiumshades.xyz
The founder supplied a mobile screenshot of Elysium Shades. Use its centered hero, high-contrast typography, restrained glow, thin-border stat cards, and simple CTA as inspiration. Combine with ASCII ENV's experimental Web3/terminal character. Do not clone either reference.

## Work requested
1. Audit current repository structure and report existing framework/tooling before adding dependencies.
2. Propose the smallest coherent frontend stack consistent with existing architecture; record the decision and rationale.
3. Implement the first responsive landing page and route skeleton for About, Token, Launch, Transparency, and Roadmap.
4. Add a consistent design system: near-black base, restrained red/white accents, muted grey, optional ambient glow, strong typography, thin borders, accessible contrast.
5. Display only grounded project facts. Mark supply and token parameters as proposed until founder approval. Do not invent token ticker, contract/mint address, launch date, holder count, volume, price, or reward metrics.
6. Wallet integration may be read-only connect/disconnect only. No message signing, transaction signing, transfers, swaps, purchase, minting, or private-key handling.
7. Add responsive/accessibility checks, build/test scripts, and documentation for local setup and deployment.
8. Provide mobile and desktop screenshots, test/build logs, changed-file list, commit SHA, and unresolved decisions.

## Non-negotiable boundaries
- No mainnet deployment, real token creation, liquidity, presale, airdrop, custody, or movement of funds.
- No fake counters, countdowns, waitlists, or claims of guaranteed rewards/returns.
- No automatic X posting or X account management.
- Never commit secrets, API keys, wallet seed phrases, or private keys.
- Do not claim completion without verifiable commit and test evidence.
- Keep all work in this repository and report blockers rather than silently making irreversible decisions.

## Founder decisions to leave open
Token name/ticker, final supply/decimals/allocation, launch date/mechanism/venue, official domain/social links, and hosting/deployment ownership. Do not guess these.
