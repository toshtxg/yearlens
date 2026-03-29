# YearLens Progress

Last updated: 2026-03-28

## Completed

- [x] Reviewed the PRD addendum and deep research already stored in this folder
- [x] Compared neighboring Streamlit project structures in this workspace
- [x] Chose a Streamlit monolith plus modular Python services approach
- [x] Scaffolded the repo layout under `app/`, `docs/`, and `sql/`
- [x] Added a runnable Streamlit entrypoint
- [x] Added input validation with explicit defaults
- [x] Added placeholder astrology, period, meaning, and narrative modules
- [x] Added local storage abstraction and Supabase schema starter
- [x] Added repo-level context and implementation docs

## In Progress

- [ ] Replace placeholder astrology with Swiss Ephemeris-backed logic
- [ ] Refine change-point generation using real transit events
- [ ] Tighten period segmentation toward the PRD target of 8 to 18 meaningful windows
- [ ] Expand rules for planets, houses, nodes, and transit modifiers
- [ ] Improve confidence scoring beyond placeholder heuristics

## Later

- [ ] Add local save/load controls in the UI
- [ ] Add Supabase persistence path when saved reports are needed
- [ ] Add optional LLM narrative provider behind a feature flag
- [ ] Add OCR and note-ingestion only if that becomes a real requirement
- [ ] Add historical calibration only after the deterministic base is trusted

## Open Decisions

- [ ] Confirm Swiss Ephemeris licensing path for the intended deployment model
- [ ] Decide whether V1 needs persistence or can stay stateless
- [ ] Decide whether V1 is birthday-anchored only or also supports calendar-year mode prominently in the UI

