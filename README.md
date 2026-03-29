# YearLens

YearLens is a Streamlit-first scaffold for a personal yearly reading app built from the existing PRD in [YearLens.md](/Users/toshgoh/projects/yearlens/YearLens.md) and the research in [deep-research-report.md](/Users/toshgoh/projects/yearlens/deep-research-report.md).

The repo is intentionally optimized for fast solo production:

- one Streamlit app
- modular Python services inside the same repo
- deterministic core logic first
- optional Supabase persistence later
- optional LLM narrative layer behind a clean interface

The current scaffold is implementation-ready, but the astrology engine is still a deterministic placeholder. It exists to unblock UI, data flow, tests, and documentation before Swiss Ephemeris is wired in.

## Docs

- [docs/context.md](/Users/toshgoh/projects/yearlens/docs/context.md) — distilled product context and build decisions
- [docs/implementation-plan.md](/Users/toshgoh/projects/yearlens/docs/implementation-plan.md) — approach, milestones, and module ownership
- [docs/progress.md](/Users/toshgoh/projects/yearlens/docs/progress.md) — live checklist

## Project Structure

```text
yearlens/
├── app/
│   ├── main.py
│   ├── core/
│   ├── providers/
│   ├── storage/
│   ├── tests/
│   └── ui/
├── docs/
├── sql/
├── .env.example
├── requirements.txt
├── YearLens.md
└── deep-research-report.md
```

## Default Product Decisions

- zodiac: `sidereal`
- ayanamsa: `lahiri`
- house system: `whole_sign`
- node type: `true`
- year window: `birthday` anchor by default
- periods per year: target `8-18`
- narrative mode: `template` first, LLM optional

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

## Current Build Status

Milestone 1 is scaffolded:

- input form
- schema validation
- placeholder report pipeline
- concise vs detailed rendering
- local report repository abstraction
- Supabase schema stub

Next is replacing the placeholder astrology with Swiss Ephemeris-backed computation and tightening the rule engine.

