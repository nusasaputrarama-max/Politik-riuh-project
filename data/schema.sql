-- POLITIK RIUH — Draft SQLite schema (v0.1)
-- Status: DRAFT — not applied anywhere, no database file exists yet.
-- Apply only via an explicit migration step (PR-005) with a log in the repo.
-- All timestamps are UTC ISO-8601 text.

CREATE TABLE IF NOT EXISTS sources (
  id            INTEGER PRIMARY KEY,
  name          TEXT NOT NULL,
  url           TEXT NOT NULL UNIQUE,
  feed_url      TEXT,
  type          TEXT NOT NULL DEFAULT 'rss',   -- rss | manual
  reliability_note TEXT,
  is_active     INTEGER NOT NULL DEFAULT 1,
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS articles (
  id            INTEGER PRIMARY KEY,
  source_id     INTEGER NOT NULL REFERENCES sources(id),
  url           TEXT NOT NULL,
  url_hash      TEXT NOT NULL UNIQUE,          -- sha256(url), dedup key
  title         TEXT,
  summary       TEXT,
  published_at  TEXT,
  fetched_at    TEXT NOT NULL DEFAULT (datetime('now')),
  status        TEXT NOT NULL DEFAULT 'unverified' -- unverified | in_review | verified | disputed | false
);

CREATE TABLE IF NOT EXISTS claims (
  id            INTEGER PRIMARY KEY,
  article_id    INTEGER NOT NULL REFERENCES articles(id),
  text          TEXT NOT NULL,
  status        TEXT NOT NULL DEFAULT 'unverified',
  created_by    TEXT NOT NULL,                 -- reviewer pseudonym
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS verifications (
  id            INTEGER PRIMARY KEY,
  claim_id      INTEGER NOT NULL REFERENCES claims(id),
  verdict       TEXT NOT NULL,                 -- verified | disputed | false
  evidence_urls TEXT NOT NULL,                 -- JSON array of URLs
  reviewer      TEXT NOT NULL,
  notes         TEXT,
  reviewed_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Append-only editorial decision log. Rows are never updated or deleted;
-- a reversal is a new row.
CREATE TABLE IF NOT EXISTS decisions (
  id            INTEGER PRIMARY KEY,
  entity_type   TEXT NOT NULL,                 -- article | claim | meme | source
  entity_id     INTEGER NOT NULL,
  action        TEXT NOT NULL,                 -- e.g. verify, dispute, correct, remove, publish
  actor         TEXT NOT NULL,
  reason        TEXT NOT NULL,
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS memes (
  id            INTEGER PRIMARY KEY,
  title         TEXT NOT NULL,
  image_path    TEXT,
  author        TEXT,
  status        TEXT NOT NULL DEFAULT 'queued', -- queued | published | rejected
  satire_label  INTEGER NOT NULL DEFAULT 1,     -- always 1: satire is always labeled
  created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
