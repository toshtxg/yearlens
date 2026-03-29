# YearLens Implementation Plan

## Goal

Ship YearLens as a fast-moving Streamlit app without locking the repo into a throwaway prototype.

## Approach

Use a single Streamlit app as the shell and keep the business logic modular.

Why this approach:

- it matches how the other folders in this workspace are built
- it minimizes setup and deployment drag
- it is easy for another coding pass to pick up
- it preserves a clean seam for later FastAPI extraction

## Folder Ownership

- `app/main.py`
  Streamlit entrypoint and orchestration.
- `app/ui/`
  Form rendering, overview rendering, period timeline rendering.
- `app/core/`
  Input validation, astrology engine, period segmentation, meaning rules, narrative protocol.
- `app/providers/`
  Template narrative implementation and future LLM implementation.
- `app/storage/`
  Local report saving now, Supabase adapter later.
- `sql/schema.sql`
  Future persistence schema.
- `docs/`
  Pickup context, decisions, and checklist.

## Build Sequence

### Milestone 1

- scaffold repo
- validate input
- render placeholder report end to end

Definition of done:

- app runs
- input validates
- report object renders in concise and detailed modes

### Milestone 2

- replace placeholder astrology with real natal chart + transit computation
- decide Swiss Ephemeris licensing path
- wire timezone handling explicitly

Definition of done:

- deterministic chart output exists
- yearly change points come from real calculations

### Milestone 3

- refine period engine
- merge noisy boundaries
- enforce 10 to 60 day periods
- target 8 to 18 segments per year

### Milestone 4

- expand meaning rules
- make domain scores more deliberate
- improve advice and confidence modeling

### Milestone 5

- harden template narrative output
- improve report UX and scanability
- add save/load from local files

### Milestone 6

- add Supabase persistence if needed
- store profiles, birth profiles, and reports

### Milestone 7

- add optional LLM narrative provider behind a feature flag

## Current Intent

The current repo is beyond the original scaffold and is now in an early-but-usable Milestone 2 state. The immediate next coding pass should focus on:

1. refining the meaning engine so period guidance sounds more like a practitioner's natural phrasing
2. improving event weighting and confidence reporting
3. deciding whether persistence is needed before launch
4. deciding whether to ship with Moshier fallback or provision Swiss ephemeris files

## Practical Guardrails

- keep the app single-page until the report gets crowded
- do not introduce external services before the deterministic pipeline is stable
- avoid making the LLM responsible for math or scoring
- keep report objects structured so they can be saved and re-rendered later
- prefer soft guidance language over blunt deterministic language in the UI
