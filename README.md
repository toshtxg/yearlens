# YearLens

YearLens is a Streamlit app for personal year-ahead readings built from sidereal astrology. It turns birth details into a natal chart, extracts real yearly transit change points, groups them into readable periods, and presents each period with plain-language guidance.

The project is intentionally optimized for fast solo shipping:

- one Streamlit app
- modular Python services in the same repo
- deterministic chart math first
- rule-based interpretation layer
- optional LLM narrative layer later

## What The App Does

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

- a year overview
- a timeline of meaningful periods
- concise mode for scanning
- detailed mode for explanation

## Current Build Status

Working now:

- validated input flow
- real `swisseph`-backed natal chart calculation
- sidereal zodiac with Lahiri ayanamsa
- whole-sign houses
- true or mean node handling
- yearly transit change points from ingresses, retrograde stations, and eclipse dates
- period segmentation into a readable timeline
- softer period-by-period guidance for decisions, politics, relationships, money, and health
- mobile-aware and tighter desktop UI
- optional manual latitude, longitude, and timezone overrides

Still evolving:

- richer interpretation heuristics
- more nuanced confidence scoring
- persistence UX
- optional LLM narrative provider

## Product Philosophy

YearLens is not meant to sound like a hard deterministic oracle. The app uses deterministic chart calculation, but the output layer is framed as reflective guidance:

- it identifies periods and themes
- it suggests what to watch more closely
- it avoids presenting the output as certainty
- it should support judgment, not replace it

## Repo Structure

```text
yearlens/
├── app/
│   ├── main.py                  # Streamlit entrypoint
│   ├── core/                    # Calculation and rule logic
│   ├── providers/               # Narrative providers
│   ├── storage/                 # Persistence adapters
│   ├── tests/                   # Pytest suite
│   └── ui/                      # Streamlit UI helpers
├── docs/                        # Product and implementation docs
├── sql/                         # Supabase starter schema
├── YearLens.md                  # PRD addendum
└── deep-research-report.md      # Research source
```

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

## Deploy On Streamlit Community Cloud

1. Push the repo to GitHub.
2. In Streamlit Community Cloud, create a new app from this repository.
3. Select branch `main`.
4. Set the main file path to `app/main.py`.
5. Deploy.

Notes:

- the app can run without secrets for local-style usage
- geocoding may be less reliable in some hosted environments, so manual latitude/longitude/timezone overrides are still useful
- if you want local Swiss ephemeris files instead of the Moshier fallback, set `SWISSEPH_EPHE_PATH`

## Environment Variables

Defined in [.env.example](.env.example):

- `SWISSEPH_EPHE_PATH`
- `GEOCODER_USER_AGENT`
- `NARRATIVE_PROVIDER`
- `YEARLENS_STORAGE_MODE`
- `OPENAI_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`

## Documentation

- [docs/context.md](docs/context.md)
- [docs/model-logic.md](docs/model-logic.md)
- [docs/technical-implementation.md](docs/technical-implementation.md)
- [docs/implementation-plan.md](docs/implementation-plan.md)
- [docs/progress.md](docs/progress.md)

## Key Caveats

- if `SWISSEPH_EPHE_PATH` is not set, the wrapper may use the Moshier fallback backend
- timezone correctness still matters a lot for birth-time-sensitive outputs
- the interpretation layer is heuristic and still being tuned
- the app is for reflection and guidance, not certainty or guaranteed prediction

