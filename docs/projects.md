# 🚀 Projects

## SignalDeck

X/Twitter idea and catalyst intake engine. Scrapes tracked accounts, extracts ticker signals, scores and ranks them.

**Path:** `projects/x-stock-signal-index/`

**Tracked accounts (10 active):**

| Handle | Active |
|---|---|
| @pepemoonboy | ✅ |
| @daniel_koss | ✅ |
| @aleabitoreddit | ✅ |
| @ParadisLabs | ✅ |
| @FinnStockinger | ✅ |
| @Kaizen_Investor | ✅ |
| @Sandeman52 | ✅ |
| @DeepValueBagger | ✅ |
| @BULLOFBRITAIN | ✅ |
| @frsinvesting | ✅ |


**Output:** Nightly rankings PDF pushed to Telegram at 23:45 London.

**Data flow:**
1. Nitter RSS → scrape recent posts from tracked accounts
2. Import → parse ticker mentions, direction, conviction
3. Score → multi-factor ranking algorithm
4. Report → PDF generation + Telegram delivery

---

## RS Screener

Price and relative-strength confirmation engine. Scans broad US market universe with sector/industry mapping and liquidity filters.

**Path:** `projects/rs-screener/` (TBC)

**Status:** Active. Nightly scan of US market universe with sector/industry mapping.

---

## Deep Alpha

Extracts market-moving alpha from executive transcripts and interviews into structured data.

**Path:** `projects/deep_alpha/`

**Status:** 🟡 In development — transcript ingestion pipeline working, extraction model tuning in progress.

---

## Personal Ops

Cross-references Google Calendar, Contacts, and local context for relationship-aware reminders and prep notes.

**Path:** `personal_ops/`

**Capabilities:**
- Calendar context briefs
- RSS/news signal digest (weekday mornings)
- Event rules engine (draft)

**RSS Digest:** Available (last generated: check [Reports](reports.md))

**Calendar:** Read-only Google Calendar integration active.

---

## Rocket Wiki

This wiki itself. Auto-rebuilt and deployed on a schedule.

**Path:** `rocket-wiki/`
**Deploy:** GitHub Pages
