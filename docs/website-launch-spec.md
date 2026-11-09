# POLITIK RIUH — Token Launch Website Specification

> **Current scope decisions (supersede conflicting v0.1 text below):** the project presents REFORMASI; token name is REFORMASI and proposed symbol/ticker is REFORMASI pending technical compatibility checks. Phase 1 is a static informational site only: **no wallet connection control, wallet status, wallet-adapter integration, registration form, or backend**. No signing or transactions. The approved whitelist requirements and sequential task flow are specified in `docs/whitelist-spec.md`, but are not implemented. Supply remains unresolved; do not publish a number.

Version: 0.1
Date: 2026-11-09
Status: Approved direction for Phase 1 implementation planning; not production-ready.

## 1. Product boundary
Build a dedicated public website for the POLITIK RIUH token project. This is not the political-news portal and does not automate the founder's X account. The founder manages X personally. The site explains the project, publishes token information, provides launch-status information, and exposes verifiable transparency data.

The token is subordinate to the POLITIK RIUH identity. Editorial coverage, community participation, or token ownership must not grant control over editorial decisions.

## 2. Design references and visual direction
References supplied by the founder:
- https://asciienv.xyz
- https://form.elysiumshades.xyz (mobile screenshot supplied; use as visual reference, not as a source of mechanics).

Direction:
- Combine ASCII ENV's experimental Web3/terminal character with Elysium Shades' centered landing-page composition, restrained statistic cards, strong typography, soft ambient glow, and simple calls to action.
- Distinct POLITIK RIUH identity; do not copy either reference.
- Near-black background; restrained red/white Indonesian accent; muted grey text; optional restrained cyan/green/violet ambient glow.
- Large editorial headline, monospace micro-labels, thin borders, rounded statistic panels, clear hierarchy, generous spacing.
- Avoid generic crypto gradients, excessive flags/political iconography, clutter, fake terminal output, fake activity counters, and decorative elements that obscure information.
- Responsive-first; mobile must be treated as a primary layout, not a compressed desktop.

## 3. Information architecture
Phase 1 public routes:
- / — landing page: identity, concise project explanation, status, primary navigation.
- /about — purpose, independent positioning, risks and limitations; no implied political-party or public-figure affiliation.
- /token — token overview, chain, mint address only when real and verified, supply and allocation disclosures, links to authoritative explorer.
- /launch — launch status and process. Before launch, show "Not launched" / "Coming later"; do not display a fake countdown or fabricated launch date.
- /transparency — allocation, treasury and wallet disclosures, liquidity/lock information, and transaction/explorer links only when evidence exists. Clearly label unavailable or not-yet-finalized data.
- /roadmap — milestones with status labels (planned, in progress, completed) backed by repository evidence.
- wallet integration — **out of scope in Phase 1**; no connect/disconnect control, wallet status, or wallet-adapter code.

## 4. Homepage content hierarchy
1. Header: POLITIK RIUH wordmark and links (About, Token, Launch, Transparency, Roadmap); no wallet status/control.
2. Hero: "Politics meets meme culture." Supporting copy: independent political meme ecosystem; no profit promise.
3. Status strip: network/environment and launch status. Use explicit labels such as "Devnet planning" and "Mainnet not launched".
4. Metrics: show only verified values. Static token supply may be displayed as "proposed" until founder approves final token parameters. Never invent holder counts, volume, market cap, rewards, waitlist counts, or price.
5. Token preview: chain, proposed supply, token status, and clear risk disclosure.
6. Transparency preview: link to verified allocation and treasury disclosures; if not finalized, say so plainly.
7. Footer: official links, disclaimer, contact/report channel placeholder only if configured.

## 5. Wallet integration deferred and security boundary
Wallet integration is **not part of Phase 1**. The static site must not include a wallet-adapter package, connect/disconnect control, connected-address display, wallet-status indicator, signing request, transaction construction, or transaction submission. Do not add read-only connection as an incidental convenience; it changes the privacy and trust boundary and requires a separate founder-approved scope decision.

A future whitelist may ask an applicant to type a public Solana address as text after the backend, privacy notice, consent, retention, and deletion controls are approved. That is not wallet connection and does not authorize a signature. Never request or collect seed phrases, private keys, wallet passwords, or transaction approvals. Any future wallet integration requires a separate threat model, privacy review, dependency review, and explicit founder approval.

## 6. Technical implementation proposal
Muse must inspect the current repository and existing architecture before selecting or adding frameworks. Do not introduce a second stack without documenting why.
- Prefer a static-first frontend for the launch site.
- Keep public display data separate from secrets and operational configuration.
- Environment variables only for non-public configuration; no credentials committed.
- Add basic security headers, safe external-link handling, input validation for any future forms, and dependency audit.
- No backend database is required for the initial static site unless a concrete feature requires it.
- Include accessible semantic HTML, keyboard navigation, visible focus states, sufficient contrast, and reduced-motion support.
- Add loading, empty, error, and mobile states; avoid dead buttons and placeholder links presented as functional.

## 7. Legal, financial, and disclosure requirements
- No guaranteed returns, price predictions, or investment advice.
- Prominently disclose meme-token volatility, potential total loss, and that the token does not represent equity, governance rights, or affiliation unless legally and technically established.
- Do not claim regulatory compliance without qualified review.
- Do not publish token allocation, liquidity, lock, treasury, or launch claims until documented and approved by the founder.
- No mainnet mint, liquidity provision, sale, presale, airdrop, custody, or fund movement in this phase.

## 8. Analytics and privacy
No invasive tracking by default. If analytics are proposed, document provider, events, consent basis, retention, and opt-out. Never log secrets, seed phrases, private keys, or unnecessary wallet-linked personal data.

## 9. Acceptance criteria
- All routes load and navigate correctly on mobile and desktop.
- Visual system follows the approved direction and is recognizably POLITIK RIUH, not a clone.
- All displayed figures and status labels have a documented source or are explicitly marked proposed/unavailable.
- No wallet-adapter dependency, connect/disconnect control, wallet status, signing, or transaction code is present in the Phase 1 static site.
- No dead CTAs, fabricated counters, fake countdowns, or unverified contract addresses.
- Accessibility basics: semantic structure, keyboard navigation, visible focus, contrast, reduced motion.
- Security review finds no committed secrets, private-key handling, unsafe wallet signing, or unnecessary personal-data collection.
- README documents local setup, build, tests, environment variables, deployment target, and known limitations.
- Evidence: screenshots at mobile and desktop widths, test/build output, and a concise implementation report.

## 10. Explicit decisions still required
Do not silently finalize these:
- ~~Token name and ticker.~~ — **DECIDED 2026-11-09 (issue #1, owner comments):** token name REFORMASI; proposed symbol/ticker REFORMASI, subject to technical compatibility checks before publication. (PR-013.)
- Final supply, decimals, allocations, vesting, treasury and liquidity policy.
- Launch date, launch venue and launch mechanism.
- Official domain and verified social links.
- Hosting provider and deployment ownership.
The previously discussed supply of 10,000,000,000 is a proposal only until founder approval.

## 11. Phase boundaries
Phase 1: implement and test the static informational launch website only; no wallet connection or registration.
Later phases require separate founder approval and review before enabling transaction signing, minting, token sale, liquidity, airdrops, or mainnet deployment.
