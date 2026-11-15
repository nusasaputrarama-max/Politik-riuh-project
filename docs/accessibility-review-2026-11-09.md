# POLITIK RIUH — Accessibility Review (token site)

Date: 2026-11-09 (WIB). Reviewer: Muse (engineering partner).
Scope: the six static pages in `apps/token-site/` (`index`, `about`,
`token`, `launch`, `transparency`, `roadmap`), `styles.css`, `main.js`.

## Method — and what this is NOT

- Static parse of all six pages (Python `html.parser`): heading outline,
  landmarks, duplicate ids, `aria-labelledby` targets, image inventory,
  link/button accessible names, skip-link target, `<main>` tabindex, `lang`.
- Browser sweep (headless Chrome via CDP): computed contrast for every
  visible text-bearing element on every page (foreground vs effective
  background; WCAG thresholds 4.5:1 normal text, 3:1 large text).
- Stylesheet inspection for the `:focus-visible` rule and the
  `prefers-reduced-motion` block. Live keyboard behaviour is proven by
  `keyboard-test.py` and live reduced-motion behaviour by
  `reduced-motion-test.py` — this review references their logs, it does
  not re-prove them.

**This is a review, not a WCAG conformance claim.** No screen-reader
testing was done. The contrast sweep approximates text drawn over the
decorative hero glow (a radial-gradient sibling element, not an ancestor
background) with the body background `#0a0a0b`; the glow is 10% red at
most and sits behind the hero text, so the approximation is small but it
is an approximation. Keyboard/focus claims rest on `keyboard-test.py`
(real Tab/Enter/Space/Escape input), not on this document.

## Findings

| Dimension | Result |
|---|---|
| `lang="id"` on all six pages | PASS — 6/6 |
| Exactly one `<h1>` per page | PASS — 6/6 |
| Heading order (no level jumps) | PASS — 6/6 |
| Landmarks `header`/`nav`/`main`/`footer` | PASS — 6/6 |
| Duplicate ids | PASS — none |
| `aria-labelledby` targets exist | PASS — all resolve |
| Images / alt text | PASS — no `<img>` elements on any page; decorative hero glow is an `aria-hidden` `<div>`, not an image |
| Link accessible names | PASS — no empty or vague link text |
| Button accessible names | PASS — every button has visible text |
| Skip link → `<main tabindex="-1">` | PASS — 6/6, focus moves to `<main>` (proven live by `keyboard-test.py`) |
| `:focus-visible` outline rule in CSS | PASS — `outline: 2px solid` red, offset 3px |
| `prefers-reduced-motion` block in CSS | PASS — present; live behaviour proven by `reduced-motion-test.py` |
| Forms / data collection | PASS — no `<form>` on any page (also enforced by `checks.sh`) |

## Heading outlines

- **index.html**: h1 “Politik bertemu budaya meme.”, h2 “Token sekilas”, h2 “Lima bagian, satu ekosistem”, h3 “Budaya politik”, h3 “Komunitas”, h3 “Satire & meme”, h3 “Satu token meme”, h3 “Transparansi”, h2 “Tidak ada yang disembunyikan — termasuk ya”, h2 “Pengungkapan risiko”, h2 “Politik Riuh”, h2 “Situs”, h2 “Catatan publik”
- **about.html**: h1 “Politik independen, dibaca lantang”, h2 “Apa yang dikerjakan proyek ini”, h3 “Budaya politik”, h3 “Komunitas”, h3 “Satire & meme”, h3 “Satu token meme”, h3 “Transparansi”, h2 “Apa yang tidak bisa dijanjikan proyek ini”, h2 “Apa yang bukan situs ini”, h2 “Politik Riuh”, h2 “Situs”, h2 “Catatan publik”
- **token.html**: h1 “Satu token meme Solana”, h2 “Pengungkapan risiko”, h2 “Politik Riuh”, h2 “Situs”, h2 “Catatan publik”
- **launch.html**: h1 “Belum diluncurkan”, h2 “Lima gate, satu selesai, empat menunggu”, h3 “Nama token disetujui”, h3 “Mint devnet + bukti pengujian”, h3 “Audit independen atas rencana token”, h3 “Keputusan pendanaan”, h3 “Persetujuan mainnet eksplisit dari founder”, h2 “Apa yang terjadi sebelum mainnet”, h2 “Pendaftaran aplikasi gratis — belum dibuka”, h2 “Yang tidak akan terjadi”, h2 “Politik Riuh”, h2 “Situs”, h2 “Catatan publik”
- **transparency.html**: h1 “Apa yang ada — dan apa yang belum ada”, h2 “Repositori adalah catatannya”, h2 “Politik Riuh”, h2 “Situs”, h2 “Catatan publik”
- **roadmap.html**: h1 “Milestone, disertai bukti”, h2 “Dokumen + scaffold repo Fase 1”, h2 “Spesifikasi situs peluncuran token”, h2 “Keputusan stack frontend”, h2 “Situs peluncuran token, Fase 1”, h2 “Nama token REFORMASI disetujui”, h2 “Review situs untuk pratinjau publik (PR-01”, h2 “Arsitektur whitelist REFORMASI (PR-014)”, h2 “Pendaftaran whitelist dibuka”, h2 “Persetujuan kebijakan editorial v1”, h2 “Daftar sumber v1 + migrasi skema”, h2 “Skeleton ingestor berita (dry-run)”, h2 “Dasbor transparansi v0”, h2 “Token devnet + bukti pengujian”, h2 “Peluncuran mainnet”, h2 “Politik Riuh”, h2 “Situs”, h2 “Catatan publik”

## Computed-contrast sweep (browser, all visible text)

| Page | Text elements checked | Below threshold | Worst ratio |
|---|---|---|---|
| index.html | 64 | 0 | 5.06:1 (`<span>` “budaya meme.”) |
| about.html | 47 | 0 | 5.23:1 (`<a>` “Baca gambaran token”) |
| token.html | 47 | 0 | 5.23:1 (`<a>` “Cara peluncuran bekerja”) |
| launch.html | 63 | 0 | 5.23:1 (`<a>` “Gambaran token”) |
| transparency.html | 47 | 0 | 5.23:1 (`<a>` “Lihat peta jalan”) |
| roadmap.html | 92 | 0 | 6.69:1 (`<span>` “Status —”) |

Notes on the sweep: the worst ratios are the red accent (5.06:1, index
hero) and white text on the primary button (5.23:1); muted `#9a9aa0`
text measures 7.07:1 against the page background (five-pair spot-check
in `checks.sh`). The sweep checks every text element against its own
effective background instead of the five declared pairs; see
`evidence/a11y-review-2026-11-09.log` for the per-element worst
list. Text over the hero glow is approximated with the body background
(see Method).

## Open gaps (not fixed by this review)

- No screen-reader testing (NVDA/VoiceOver/TalkBack) — keyboard and
  contrast evidence is real, but screen-reader behaviour is unverified.
- No manual test with a real keyboard on a real device — the keyboard
  matrix is headless-Chrome CDP input, which is real input but not a
  human pass.
- Contrast sweep approximation over the hero glow (see Method).
- This review does not claim WCAG 2.x conformance at any level.

## Evidence

- This document: `docs/accessibility-review-2026-11-09.md`
- Log: `apps/token-site/evidence/a11y-review-2026-11-09.log`
- Keyboard matrix: `apps/token-site/keyboard-test.py` +
  `apps/token-site/evidence/keyboard-2026-11-09.log`
- Reduced motion: `apps/token-site/reduced-motion-test.py` +
  `apps/token-site/evidence/reduced-motion-2026-11-09.log`
- Palette spot-check: `apps/token-site/checks.sh` §5
