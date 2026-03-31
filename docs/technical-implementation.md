# YearLens Technical Implementation

## Stack

- Python 3.13
- Streamlit
- `pysweph` / Swiss Ephemeris wrapper
- `lunar-python`
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
  Year overview rendering plus trust/data-handling cues.
- [timeline.py](/Users/toshgoh/projects/yearlens/app/ui/timeline.py)
  Period timeline rendering with plain-English summaries, score bars, and explanation blocks.
- [styles.py](/Users/toshgoh/projects/yearlens/app/ui/styles.py)
  Global UI styling and responsive layout tuning.

### Core Logic

- [input_schema.py](/Users/toshgoh/projects/yearlens/app/core/input_schema.py)
  Input validation with Pydantic.
- [location_service.py](/Users/toshgoh/projects/yearlens/app/core/location_service.py)
  Geocoding, coordinate normalization, timezone lookup.
- [astro_engine.py](/Users/toshgoh/projects/yearlens/app/core/astro_engine.py)
  Natal chart computation, reading window logic, yearly change points.
- [bazi_engine.py](/Users/toshgoh/projects/yearlens/app/core/bazi_engine.py)
  Exact BaZi pillar calculation plus visible five-element decomposition and lightweight balancing suggestions.
- [period_engine.py](/Users/toshgoh/projects/yearlens/app/core/period_engine.py)
  Boundary merging, splitting, and segment compression.
- [meaning_engine.py](/Users/toshgoh/projects/yearlens/app/core/meaning_engine.py)
  Weighted driver selection, domain scoring, signals, explanations, and confidence breakdown.
- [narrative_engine.py](/Users/toshgoh/projects/yearlens/app/core/narrative_engine.py)
  Structured narrative attachment and overview generation.
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

Important current-state note:

- the live app flow does not call the storage adapters
- reports are kept in the current Streamlit session
- no database or report-file write happens during normal use

## Request Flow

1. Streamlit form collects input.
2. `UserInput` validates the payload.
3. `location_service` resolves location context.
4. `astro_engine` computes the sidereal natal chart and yearly change points.
5. `bazi_engine` computes the exact BaZi four pillars from the local birth datetime and derives the visible five-element mix.
6. `period_engine` converts event dates into readable periods.
7. `meaning_engine` selects dominant drivers, scores domains, creates soft guidance signals, and builds explanation blocks plus confidence breakdowns.
8. `template_narrative` converts structured period data into headline and summary copy.
9. UI renders the overview, optional BaZi balance section, and the year timeline.

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

Privacy implication:

- if the text location path is used, the place name is sent to the geocoder to resolve coordinates
- timezone lookup is then performed locally from the resolved coordinates
- the same resolved local timezone is reused for both sidereal chart math and BaZi pillar calculation

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
- BaZi pillar and element-balance regression cases
- period generation
- meaning-engine output shape and signal surfacing
- narrative output shape
- year-anchor regression cases

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
- BaZi balancing guidance is intentionally heuristic and limited to visible pillars plus lightweight color cues
- heuristic interpretation rules still need refinement

## Recommended Next Technical Steps

1. calibrate the new meaning heuristics against more real reading examples
2. refine threshold tuning for when signals should surface or stay hidden
3. add local save/load UX only if persistence becomes a real user need
4. add optional Supabase-backed report storage
5. optionally extract core logic into a service only when the Streamlit monolith becomes too crowded
