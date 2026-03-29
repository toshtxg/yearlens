# YearLens Progress

Last updated: 2026-03-29

## Completed

- [x] Reviewed the PRD addendum and deep research already stored in this folder
- [x] Compared neighboring Streamlit project structures in this workspace
- [x] Chose a Streamlit monolith plus modular Python services approach
- [x] Scaffolded the repo layout under `app/`, `docs/`, and `sql/`
- [x] Added a runnable Streamlit entrypoint
- [x] Added input validation with explicit defaults
- [x] Added modular astrology, period, meaning, and narrative modules
- [x] Added local storage abstraction and Supabase schema starter
- [x] Added repo-level context and implementation docs
- [x] Installed local runtime dependencies in `venv`
- [x] Replaced placeholder chart math with a real `swisseph`-backed engine
- [x] Added manual latitude, longitude, and timezone overrides
- [x] Added real yearly change points from ingresses, stations, and eclipses
- [x] Updated the GitHub-facing README to match the current implementation
- [x] Verified the test suite passes locally
- [x] Verified the Streamlit app boots locally
- [x] Added mobile-aware and tighter desktop layout passes
- [x] Added intro, user-guide, and disclaimer content in the app header
- [x] Added softer period guidance around decisions, politics, relationships, money, and health
- [x] Added dedicated documentation for model logic and technical implementation
- [x] Removed the unused `Download JSON` report action
- [x] Added weighted dominant-driver selection for each period
- [x] Added plain-English explanation scaffolding before interpretation
- [x] Added confidence breakdown using event strength, signal agreement, and data quality
- [x] Added trust/data-handling notes to the report and header
- [x] Added tests for narrative shape and anchor regression behavior

## In Progress

- [ ] Calibrate the new meaning rules against more real reading examples
- [ ] Refine change-point weighting so segment boundaries feel more practitioner-like
- [ ] Tighten period segmentation further using driver intensity rather than only date spacing
- [ ] Expand rules for planets, houses, nodes, and transit modifiers
- [ ] Tune thresholds for when signals should surface or stay hidden

## Later

- [ ] Add local save/load controls in the UI
- [ ] Add Supabase persistence path when saved reports are needed
- [ ] Add optional LLM narrative provider behind a feature flag
- [ ] Add OCR and note-ingestion only if that becomes a real requirement
- [ ] Add historical calibration only after the deterministic base is trusted
- [ ] Add persistence UI only if users actually need saved reports

## Open Decisions

- [ ] Confirm Swiss Ephemeris licensing path for the intended deployment model
- [ ] Decide whether to provision local Swiss ephemeris files or accept the Moshier fallback for early testing
- [ ] Decide whether V1 needs persistence or can stay stateless
- [ ] Decide whether V1 is birthday-anchored only or also supports calendar-year mode prominently in the UI
