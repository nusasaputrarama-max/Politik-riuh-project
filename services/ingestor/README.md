# services/ingestor

News/RSS monitoring: polls an allowlisted feed list, writes `articles` rows (status `unverified`), dedups by URL hash.

**Status: NOT STARTED** (PR-004). Design constraints: SSRF guard on every fetch (allowlist hosts, no private IPs, redirect limits, timeout, size cap); RSS fields only in Phase 1 — no full-article scraping; fail-closed on dead feeds.
