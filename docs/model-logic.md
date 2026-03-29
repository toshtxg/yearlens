# YearLens Model Logic

## Goal

The model layer in YearLens is designed to produce readable yearly guidance without making the app depend on an LLM or black-box scoring.

The logic has three layers:

1. deterministic chart and transit calculation
2. rule-based interpretation
3. plain-language rendering

## 1. Deterministic Calculation Layer

Implemented mainly in [astro_engine.py](/Users/toshgoh/projects/yearlens/app/core/astro_engine.py).

Inputs:

- birth date
- birth time
- birth location
- target year
- preferences like ayanamsa and node type

What this layer computes:

- natal chart
- ascendant
- sidereal sign positions
- whole-sign houses
- yearly transit change points inside the selected reading window

Current yearly change points include:

- sign ingresses
- retrograde station changes
- solar eclipses
- lunar eclipses

This layer is deterministic by design. It does not generate prose or make interpretive claims.

## 2. Reading Window Logic

Implemented in `get_year_window()` in [astro_engine.py](/Users/toshgoh/projects/yearlens/app/core/astro_engine.py).

Two anchor modes exist:

- `birthday`
  the reading runs from the birthday in the target year to the day before the next birthday
- `calendar`
  the reading runs from January 1 to December 31 of the target year

This matters because all change points, segments, and summaries are filtered into that chosen window.

## 3. Period Generation

Implemented in [period_engine.py](/Users/toshgoh/projects/yearlens/app/core/period_engine.py).

How it works:

- collect change points inside the reading window
- sort them by date
- create boundaries from those dates
- merge boundaries that are too close together
- split overly long windows
- compress the total number of windows toward the target segment count

Default intent:

- minimum period length around 10 days
- maximum period length around 60 days
- roughly 8 to 18 useful windows per year

## 4. Domain Scoring

Implemented in [meaning_engine.py](/Users/toshgoh/projects/yearlens/app/core/meaning_engine.py).

The app scores six broad life domains for each period:

- career / work
- money / finance
- relationships
- health / emotional
- travel / overseas
- study / growth

The current scoring model uses:

- weighted transit drivers for the period
- event type intensity differences between ingresses, stations, and eclipses
- repeating house emphasis inside the same window
- house-to-domain mappings
- planet-to-domain boosts
- current period tone

This is still a heuristic layer and should be treated as tunable.

## 5. Tone Model

Each period gets a tone such as:

- productive
- mixed
- stress
- busy
- growth
- supportive
- heavy
- unstable
- slow down

These are UI-facing labels mapped from internal tone categories. The labels are intentionally simpler than traditional astrology language.

## 6. Guidance Signals

YearLens now incorporates the kinds of concerns a practitioner might naturally highlight in a reading, but frames them as soft guidance instead of hard prediction.

Current signal categories:

- decision timing
- people / politics
- relationships
- money
- health
- travel / movement
- work / responsibility

Important design choice:

- these signals are attached to each period timeline card
- they are phrased as things to watch, not as certain outcomes
- they are not surfaced as a deterministic “master verdict” for the whole year

Examples of the intended tone:

- `Use extra care with big decisions`
- `Watch people and politics more closely`
- `Handle relationships with extra care`
- `Keep money decisions measured`
- `Mind energy, stress, and health`

## 7. Dominant Drivers

YearLens now picks 1-2 dominant drivers per period instead of blending every change point equally.

The weighting currently considers:

- raw event intensity
- event type
- planet
- house sensitivity
- whether multiple drivers repeat the same house emphasis

This is meant to reduce generic period output and make each window feel more distinct.

## 8. Narrative Layer

Implemented in [template_narrative.py](/Users/toshgoh/projects/yearlens/app/providers/template_narrative.py) and [narrative_engine.py](/Users/toshgoh/projects/yearlens/app/core/narrative_engine.py).

Current provider:

- `TemplateNarrativeProvider`

Planned later:

- optional `LLMNarrativeProvider`

Rule:

- LLMs should never become the source of truth for chart math, event dates, or raw period scoring
- LLM use, if added, should stay downstream of the structured deterministic output

The current deterministic narrative shape is:

- short headline
- plain-English summary
- use this window for
- be more careful with
- detailed explanation blocks for the event, sign, and house

Important UX decision:

- the app now translates the symbolism before jumping to interpretation
- raw phrases like `Lunar eclipse in Leo / House 8` are no longer meant to stand alone without explanation

## 9. Confidence Logic

Confidence is still heuristic, but it is no longer a flat single-factor score.

The current confidence model blends:

- event strength
- signal agreement
- data quality

Data quality currently reflects:

- whether location was manually provided or geocoded
- whether manual timezone was supplied
- whether Swiss ephemeris files were available or Moshier fallback was used

## 10. Softness vs Certainty

This is an explicit model design constraint.

The app should not:

- sound like a guaranteed forecast
- state outcomes too bluntly
- overclaim certainty from heuristic interpretation

The app should:

- point to cleaner vs more sensitive windows
- highlight themes to watch
- support reflection and decision quality
- leave room for user judgment

## 11. Known Model Limits

- the interpretation heuristics still need calibration against real practitioner examples
- confidence scoring is still heuristic and not historically validated
- no birth time uncertainty model yet
- no OCR note ingestion yet
- no historical calibration yet
- no practitioner-specific custom ruleset yet
