# YearLens Technical Implementation

## Stack

- Python 3.13
- Streamlit
- `pysweph` / Swiss Ephemeris wrapper
- `geopy`
- `timezonefinder`
- `pydantic`
- `pytest`
- optional Supabase

## Runtime Architecture

YearLens currently ships as a Streamlit monolith with modular Python packages.

Why this shape:

- fast to build
- easy to deploy
- easy to maintain as a solo project
- still clean enough to extract an API later if needed

## Module Map

### UI

- [main.py](/Users/toshgoh/projects/yearlens/app/main.py)
  Entry point, top-level orchestration, intro/disclaimer blocks.
- [form.py](/Users/toshgoh/projects/yearlens/app/ui/form.py)
  User input form and advanced overrides.
- [report.py](/Users/toshgoh/projects/yearlens/app/ui/report.py)
  Year overview rendering.
- [timeline.py](/Users/toshgoh/projects/yearlens/app/ui/timeline.py)
  Period timeline rendering.
- [styles.py](/Users/toshgoh/projects/yearlens/app/ui/styles.py)
  Global UI styling and responsive layout tuning.

### Core Logic

- [input_schema.py](/Users/toshgoh/projects/yearlens/app/core/input_schema.py)
  Input validation with Pydantic.
- [location_service.py](/Users/toshgoh/projects/yearlens/app/core/location_service.py)
  Geocoding, coordinate normalization, timezone lookup.
- [astro_engine.py](/Users/toshgoh/projects/yearlens/app/core/astro_engine.py)
  Natal chart computation, reading window logic, yearly change points.
- [period_engine.py](/Users/toshgoh/projects/yearlens/app/core/period_engine.py)
  Boundary merging, splitting, and segment compression.
- [meaning_engine.py](/Users/toshgoh/projects/yearlens/app/core/meaning_engine.py)
  Domain scoring, tone assignment, period guidance.
- [narrative_engine.py](/Users/toshgoh/projects/yearlens/app/core/narrative_engine.py)
  Concise/detailed narrative attachment and overview generation.
- [config.py](/Users/toshgoh/projects/yearlens/app/core/config.py)
  Constants, mappings, UI labels, and defaults.

### Providers

- [template_narrative.py](/Users/toshgoh/projects/yearlens/app/providers/template_narrative.py)
  Deterministic narrative provider.
- [llm_narrative.py](/Users/toshgoh/projects/yearlens/app/providers/llm_narrative.py)
  Future placeholder for optional LLM narrative support.

### Storage

- [report_repository.py](/Users/toshgoh/projects/yearlens/app/storage/report_repository.py)
  Local report persistence abstraction.
- [supabase_client.py](/Users/toshgoh/projects/yearlens/app/storage/supabase_client.py)
  Optional Supabase hook.
- [schema.sql](/Users/toshgoh/projects/yearlens/sql/schema.sql)
  Starter schema for future persistence.

## Request Flow

1. Streamlit form collects input.
2. `UserInput` validates the payload.
3. `location_service` resolves location context.
4. `astro_engine` computes natal chart and yearly change points.
5. `period_engine` converts event dates into readable periods.
6. `meaning_engine` scores domains and creates soft guidance signals.
7. `template_narrative` converts structured period data into concise and detailed text.
8. UI renders overview plus timeline.

## Ephemeris Behavior

YearLens uses `pysweph`.

If `SWISSEPH_EPHE_PATH` is provided:

- Swiss Ephemeris can use local ephemeris files

If it is not provided:

- the wrapper may fall back to the Moshier backend

The app exposes the backend in the debug payload so this is visible during testing.

## Location And Timezone Handling

There are two supported paths:

1. geocode the text location through Nominatim
2. bypass geocoding by providing manual latitude, longitude, and timezone

The manual path is strongly recommended for repeatable tests and deployment environments where geocoding may be flaky.

## Deployment Notes

### Local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

### Streamlit Community Cloud

- repo: this GitHub repository
- branch: `main`
- main file path: `app/main.py`

You can deploy with no secrets for baseline testing.

Useful optional secrets:

- `SWISSEPH_EPHE_PATH`
- `GEOCODER_USER_AGENT`
- `SUPABASE_URL`
- `SUPABASE_KEY`

## Testing

Current test coverage focuses on:

- schema validation
- astrology engine wiring
- period generation
- meaning-engine output shape

Run:

```bash
source venv/bin/activate
pytest app/tests
```

## Current Technical Limits

- no persistence UI yet
- no user accounts
- no OCR ingestion
- no historical note calibration
- no explicit birth-time uncertainty modeling
- heuristic interpretation rules still need refinement

## Recommended Next Technical Steps

1. deepen the meaning heuristics so they reflect more practitioner-style weighting
2. improve confidence logic beyond a simple driver-based heuristic
3. add local save/load UX
4. add optional Supabase-backed report storage
5. optionally extract core logic into a service only when the Streamlit monolith becomes too crowded

