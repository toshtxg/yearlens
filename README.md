# YearLens

YearLens is a Streamlit app for generating personal year-ahead readings from sidereal astrology. It computes a natal chart, extracts real yearly transit change points, groups them into readable time windows, and renders each period in concise or detailed mode from the same structured interpretation object.

The build is intentionally optimized for solo shipping:

- one Streamlit app
- modular Python services inside the same repo
- deterministic chart math and rule-based interpretations
- optional Supabase persistence later
- optional LLM narrative layer later

## Current Status

Milestone 2 is underway and already usable for local testing.

What works now:

- validated birth input flow
- real `swisseph`-backed natal chart calculation
- sidereal zodiac with Lahiri ayanamsa
- whole-sign houses
- true or mean node toggle
- yearly transit change points from real ingresses, retrograde stations, and eclipse dates
- period segmentation compressed into a readable yearly timeline
- concise and detailed report rendering from the same period object
- optional manual latitude, longitude, and timezone overrides

What is still evolving:

- richer interpretation rules
- stronger confidence modeling
- saved report UX
- optional LLM narrative provider
- optional Supabase persistence

## Product Shape

Inputs:

- birth date
- birth time
- birth location
- target year

Optional advanced overrides:

- latitude
- longitude
- timezone ID
- node type

Outputs:

- year overview
- 8 to 18 timeline periods in the default configuration
- concise mode for scanning
- detailed mode for explanation

## Architecture

```text
yearlens/
├── app/
│   ├── main.py                  # Streamlit entrypoint
│   ├── core/                    # Deterministic calculation + rules
│   ├── providers/               # Narrative providers
│   ├── storage/                 # Persistence adapters
│   ├── tests/                   # Pytest suite
│   └── ui/                      # Streamlit UI helpers
├── docs/                        # Context, plan, and progress
├── sql/                         # Supabase starter schema
├── YearLens.md                  # PRD addendum
└── deep-research-report.md      # Deep research source
```

## Core Decisions

- zodiac: `sidereal`
- ayanamsa: `lahiri`
- house system: `whole_sign`
- node type: `true` by default
- year anchor: `birthday`
- narrative provider: deterministic template provider first

## Technical Notes

### Astrology engine

YearLens now uses the `swisseph` Python wrapper. If you do not configure ephemeris files, Swiss Ephemeris will fall back to its built-in Moshier backend. The app surfaces that backend in the debug payload so accuracy assumptions stay visible.

To point the app at local ephemeris files:

```bash
export SWISSEPH_EPHE_PATH="/path/to/ephemeris/files"
```

### Location handling

The app supports two paths:

1. `birth_location` string geocoded through Nominatim
2. manual latitude, longitude, and timezone override

For stable local testing, the manual override path is the most reliable because it avoids network-dependent geocoding.

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

## Run Tests

```bash
source venv/bin/activate
pytest app/tests
```

## Docs

- [docs/context.md](docs/context.md)
- [docs/implementation-plan.md](docs/implementation-plan.md)
- [docs/progress.md](docs/progress.md)

## Near-Term Roadmap

1. deepen the meaning engine so transit type and natal context influence domain scoring more precisely
2. tighten change-point selection and confidence reporting
3. add save/load flows and optional Supabase persistence
4. keep LLM usage optional and downstream of deterministic output
