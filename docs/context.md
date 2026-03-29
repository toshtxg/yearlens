# YearLens Context

## Source Documents

- PRD addendum: [YearLens.md](/Users/toshgoh/projects/yearlens/YearLens.md)
- deep research: [deep-research-report.md](/Users/toshgoh/projects/yearlens/deep-research-report.md)

## Product Goal

Build a personal yearly reading app that:

- collects birth date, birth time, birth location, and target year
- computes a sidereal natal chart and yearly change points
- converts those into 8 to 18 variable-length periods
- scores major life domains for each period
- explains every period in concise and detailed modes
- keeps the core deterministic and keeps LLM usage optional

## Chosen Build Direction

The repo is scaffolded as a Streamlit monolith with internal Python modules because that is the fastest path that still preserves separation of concerns.

- UI lives in `app/ui`
- deterministic logic lives in `app/core`
- narrative implementations live in `app/providers`
- persistence abstractions live in `app/storage`
- schema and table setup lives in `sql/schema.sql`

This follows the PRD recommendation: simple enough for a solo builder now, clean enough to split into FastAPI later if needed.

## Defaults Pulled From The Research + PRD

- zodiac: sidereal
- ayanamsa: Lahiri
- house system: whole sign
- node type: true nodes
- year anchor: birthday-to-birthday
- period count target: 8 to 18
- period bounds: roughly 10 to 60 days
- interpretation stance: deterministic facts first, rule-based meanings second, optional narrative polishing third

## V1 Scope

In scope for the first real implementation:

- validated input form
- natal chart computation
- yearly transit change points
- period generation
- rule-based meaning engine
- concise and detailed text from the same structured object
- local JSON persistence or no persistence

Current status:

- the repo now has a real `swisseph`-backed natal and transit pipeline
- location resolution supports both geocoding and manual coordinate overrides
- the meaning engine is still intentionally lightweight and is the next place to deepen

Deferred from V1:

- OCR note ingestion
- personal calibration from historical notes
- account system
- multi-user support
- cloud jobs
- FastAPI split

## Important Constraints

### Privacy

Birth date, birth time, and location are sensitive personal data. The app should stay local-first by default and only add remote storage when there is a clear reason.

### Licensing

The research flags Swiss Ephemeris licensing as architecture-shaping. Before wiring real chart math into production, decide between AGPL-compatible distribution or a professional license.

### Time Zone Accuracy

Swiss Ephemeris does not resolve local time zones for you. Historical timezone conversion needs an explicit IANA tzdb-backed layer when the real astrology engine is implemented.

## Milestone 2 Caveat

`app/core/astro_engine.py` now performs real calculations through the Swiss Ephemeris wrapper, but the default local setup may still use the Moshier fallback unless ephemeris files are provided through `SWISSEPH_EPHE_PATH`.

That is acceptable for the initial Milestone 2 build because:

- it gives deterministic real chart math immediately
- it keeps local setup simple
- it preserves a clean upgrade path to full Swiss ephemeris files later

## Replacement Map

- deepen `app/core/period_engine.py` boundary weighting as more real event types are added
- expand `app/core/meaning_engine.py` with richer planet, house, and transit rules
- optionally wire `app/providers/llm_narrative.py` after template output is stable
- optionally add true Swiss ephemeris files via `SWISSEPH_EPHE_PATH` for higher-fidelity production runs
