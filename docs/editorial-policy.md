# POLITIK RIUH — Editorial Policy (Draft v0.1)

- **Date:** 2026-11-09
- **Status:** DRAFT — needs approval by Rama and review by ChatGPT (PR-002). Nothing here is final policy yet.

## 1. Principles

1. **Accuracy before speed.** Being second and right beats being first and wrong.
2. **Provenance or it is unverified.** A claim without a source URL, retrieval time, and reviewer is `unverified`, whatever its plausibility.
3. **Satire is satire.** Satire is labeled in-image and in-caption, kept in its own gallery, and never appears in the news feed unlabeled.
4. **No defamation.** Named-person claims need two independent sources plus evidence links. If it cannot be verified, it is not published as verified.
5. **No anonymous smears.** No claim sourced only to an anonymous account with no corroboration.
6. **Corrections are public.** A wrong verified item is corrected in place, with the correction logged (what changed, when, why). No silent edits, no silent deletions.
7. **No personal data.** Addresses, phone numbers, private family details are never published.
8. **Editorial independence from the token.** Token price, holdings, and trading never influence a verification verdict. Team holdings (if any) are disclosed on the transparency dashboard.

## 2. Verification states

| State | Meaning | Display |
|---|---|---|
| `unverified` | Ingested, not yet reviewed | Badge "Belum terverifikasi", never shown as fact |
| `in_review` | A reviewer is working on it | Badge "Dalam peninjauan" |
| `verified` | Two independent sources + evidence links + reviewer sign-off | Badge "Terverifikasi" + sources listed |
| `disputed` | Credible sources disagree, or evidence is contested | Badge "Dipersoalkan" + both sides summarized |
| `false` | Evidence shows the claim is false | Badge "Tidak benar" + the refuting evidence |

## 3. Workflow

1. Ingestor collects an item → `unverified`.
2. Editor picks it up → `in_review` (claim text extracted, sources attached).
3. Editor checks: primary source? corroboration? original context (not a clipped quote)? → verdict + evidence links + notes.
4. Verdict published with provenance. Every state change writes a row to the append-only decision log.
5. New evidence reopens the item; the correction is logged, not hidden.

## 4. Satire rules

- Satire is labeled **SATIRE / SATIR** in the image and the caption.
- No doctored image presented as a real photo. No fake quote presented as a real quote.
- No satire targeting private individuals (public figures only), no harassment, no hate content.
- Satire queue is curated by a human; community submissions are reviewed before publication.

## 5. Source list principles (PR-003)

- Indonesian political news outlets with working RSS feeds.
- Spanning ownership/editorial lines where possible; the list and the inclusion criteria are public.
- A source that repeatedly fails verification is flagged, not quietly dropped — the flag is public.
