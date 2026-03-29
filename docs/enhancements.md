# YearLens UI/UX Enhancements

Spec for making YearLens feel polished for everyday (non-technical) users.
Each section states what to change, where, and exactly how.

Completed: ~~#1 Fix repetitive headlines~~, ~~#2 Soften tone labels~~, ~~#3 Collapse instructions~~, ~~#4 Add a visual year timeline bar~~, ~~#5 Color-code period expander headers by tone~~, ~~#6 Replace or reframe the confidence label~~, ~~#7 Tighten concise mode~~, ~~#8 Highlight the current period~~, ~~#9 Hide debug payload from non-dev users~~, ~~#10 Make the year overview more visual~~

---

## 4. Add a visual year timeline bar

**Problem:** The year is a flat list of expanders — no visual sense of rhythm or proportion.

**Where:** New rendering function in `app/ui/report.py`, called from `main.py` right before the "Read The Year" heading.

**What to render:** A single horizontal stacked bar showing all periods proportionally by duration, color-coded by tone.

**Tone-to-color mapping** (add to `config.py`):
```python
TONE_COLORS = {
    "constructive": "#4ade80",  # green
    "mixed":        "#a78bfa",  # purple
    "stressful":    "#f87171",  # red
    "active":       "#60a5fa",  # blue
    "expansive":    "#34d399",  # teal
    "supportive":   "#fbbf24",  # amber
    "serious":      "#9ca3af",  # gray
    "volatile":     "#fb923c",  # orange
    "reflective":   "#c4b5fd",  # lavender
}
```

**Implementation:** Render a `<div class="yearlens-timeline-bar">` containing one child `<div>` per period. Each child:
- `width` = period duration / total year duration as percentage
- `background-color` = TONE_COLORS[period.tone]
- `title` attribute = "Jan 1 – Mar 4: High-pressure" (for hover tooltip)
- small text label inside showing abbreviated month range if width > 8%

**CSS** (add to `app/ui/styles.py`):
```css
.yearlens-timeline-bar {
    display: flex;
    width: 100%;
    height: 36px;
    border-radius: 8px;
    overflow: hidden;
    margin: 0.75rem 0 1.25rem 0;
    gap: 2px;
}
.yearlens-timeline-bar > div {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    color: #111827;
    font-weight: 600;
    letter-spacing: 0.02em;
    cursor: default;
    transition: opacity 0.15s;
    border-radius: 4px;
}
.yearlens-timeline-bar > div:hover {
    opacity: 0.8;
}
```

**Add a small legend row** below the bar: one colored dot + label per tone that actually appears in the year (not all 9, just the ones used).

**Codex did:** Added `TONE_COLORS` in `app/core/config.py`, built `render_year_timeline_bar()` in `app/ui/report.py`, called it from `app/main.py` before the "Read The Year" section, and added a tone legend that only shows tones present in the current report.

---

## 5. Color-code period expander headers by tone

**Problem:** All period expanders look identical — no visual scanning cue.

**File:** `app/ui/timeline.py`, `render_period_timeline()`

**Approach:** Wrap each `st.expander` in a `<div>` with a data attribute or class for the tone, and use CSS to set a left border color.

Since Streamlit expanders don't support custom classes directly, use a workaround: render a thin colored accent bar immediately before each expander using `st.markdown`.

```python
tone_color = TONE_COLORS[period["tone"]]
st.markdown(
    f"<div class='yearlens-period-accent' style='border-left: 4px solid {tone_color};'></div>",
    unsafe_allow_html=True,
)
```

**CSS:**
```css
.yearlens-period-accent {
    height: 0;
    margin-bottom: -1px;
}
/* Target the next Streamlit expander sibling */
.yearlens-period-accent + div [data-testid="stExpander"] {
    border-left-width: 4px;
    border-left-style: solid;
    border-left-color: inherit;
}
```

If the CSS sibling selector doesn't reliably work with Streamlit's DOM, fall back to wrapping the entire expander content in a `<div style="border-left: 4px solid {color}; padding-left: 12px;">`.

**Codex did:** Implemented a tone-colored accent bar directly above each period expander in `app/ui/timeline.py` using the shared `TONE_COLORS` map, then styled it in `app/ui/styles.py` so each period is easier to scan visually.

---

## 6. Replace or reframe the confidence label

**Problem:** "Mixed but usable signal" reads as "this might be wrong." Non-technical users don't benefit from seeing internal confidence math.

**File:** `app/ui/report.py`, `_year_signal_label()` (line 28) and `render_year_overview()` (line 76)

**Option A — Reframe (recommended):**
```python
def _year_signal_label(confidence: float) -> str:
    if confidence >= 0.8:
        return "Strong signal clarity"
    if confidence >= 0.68:
        return "Moderate signal clarity"
    return "Softer signal — read as general direction"
```

**Option B — Remove entirely:** Drop the confidence pill from the year overview meta row. Keep confidence visible only in the per-period detailed view for users who explicitly want it.

Go with Option A. Also update the per-period `_clarity_label()` in `timeline.py`:

```python
def _clarity_label(confidence: float) -> str:
    if confidence >= 0.8:
        return "Clarity: strong"
    if confidence >= 0.68:
        return "Clarity: moderate"
    return "Clarity: general direction"
```

**Codex did:** Reframed the year-level label to `Strong signal clarity`, `Moderate signal clarity`, and `Softer signal - read as general direction` in `app/ui/report.py`, and updated the period-level detailed view label in `app/ui/timeline.py` to `Clarity: strong`, `Clarity: moderate`, and `Clarity: general direction`.

---

## 7. Tighten concise mode

**Problem:** Even concise mode shows: story card + 2 signals + action cards + takeaway + focus pills. That's still a lot.

**File:** `app/ui/timeline.py`, `render_period_timeline()`, the `mode == "concise"` path.

**New concise layout per period:**
1. Pill row (date, tone, main focus) — keep as-is
2. Story card — **remove** the "Plain-language read" kicker line and the "What this usually feels like" meta line. Just show headline + concise_text.
3. Action cards (lean into / go slower with) — keep
4. **Remove** signal grid in concise mode (signals are already implied by the headline and action cards)
5. **Remove** takeaway card in concise mode (it often just restates the headline)
6. Focus pills — keep

This cuts each concise period from ~5 visual blocks to 3.

**Codex did:** Simplified concise mode in `app/ui/timeline.py` so it now shows the pill row, a simplified story card, the action cards, and focus pills. The concise view no longer shows the signal grid, takeaway card, or story-card helper/meta text.

---

## 8. Highlight the current period

**Problem:** If reading the current year, users can't tell which period they're in right now.

**File:** `app/ui/timeline.py`, `render_period_timeline()`

**Logic:** Compare `date.today()` against each period's `start_date` / `end_date`. If today falls inside:
- Auto-expand that period (pass `expanded=True`)
- Add a "Now" pill to its pill row: `<span class='yearlens-pill yearlens-pill-now'>Now</span>`

**CSS:**
```css
.yearlens-pill-now {
    background: var(--yl-accent);
    color: #111827;
    font-weight: 700;
}
```

Only apply when `target_year == current_year` (or more precisely, when `date.today()` falls within the year window).

**Codex did:** Added automatic current-period detection in `app/ui/timeline.py`, auto-expands the active window when today falls inside it, and adds a `Now` pill styled in `app/ui/styles.py`.

---

## 9. Hide debug payload from non-dev users

**Problem:** "Debug payload" expander is visible to all users.

**File:** `app/main.py`, lines 137-138

**Fix:** Gate behind a query param so you can append `?debug=1` to the URL without redeploying:

```python
if st.query_params.get("debug"):
    with st.expander("Debug payload", expanded=False):
        st.json(report)
```

**Codex did:** Gated the debug payload behind `?debug=1` in `app/main.py`, so regular users no longer see developer-facing output by default.

---

## 10. Make the year overview more visual

**Problem:** The three-column overview (Themes / Lean Into / Pace Carefully) is all text. The theme list is particularly flat.

**File:** `app/ui/report.py`, `render_year_overview()`

**Enhancement A — Domain emphasis mini-bar:** Below the "Your Year At A Glance" card and above the three columns, add a horizontal row of the top 3 domains with small inline progress indicators showing how dominant they are across the year.

Pull domain scores from the overview's `top_themes` (which already contain domain emojis + labels). For the actual scores, compute an aggregate in `narrative_engine.py`'s `build_year_overview`:

```python
# In build_year_overview, add to the returned dict:
"domain_totals": {
    domain: round(sum(p["domains"][domain] for p in periods) / len(periods), 1)
    for domain in DOMAINS
}
```

Render as small horizontal bars (same style as per-period domain scores but compact, in a single row of 3-4).

**Enhancement B — Tone summary as visual chips instead of pills:** The `tone_summary` pills currently show text like "🌪 Unstable" and "⚠️ Stress". Replace with small colored chips using the `TONE_COLORS` map — a colored dot + label, making the year's tone mix scannable at a glance.

**Codex did:** Added `domain_totals` to `build_year_overview()` in `app/core/narrative_engine.py`, rendered the top domain emphasis row as compact mini-bars in `app/ui/report.py`, switched the tone summary to colored chips using `TONE_COLORS`, and reformatted the overview date lists into cleaner human-readable ranges.

---

## Implementation order (recommended)

| Priority | Enhancement | Impact | Effort |
|----------|------------|--------|--------|
| 1        | #7 Tighten concise mode | Medium — reduces cognitive load | Low |
| 2        | #9 Hide debug payload | Medium — removes dev artifact | Trivial |
| 3        | #8 Highlight current period | Medium — answers "what about right now?" | Low |
| 4        | #6 Reframe confidence label | Low-Medium — removes one moment of doubt | Trivial |
| 5        | #4 Visual timeline bar | High — strongest visual upgrade | Medium |
| 6        | #5 Color-code period headers | Medium — visual scanning | Low-Medium |
| 7        | #10 Visual year overview | Medium — polish | Medium |

---

## Files touched

| File | Enhancements |
|------|-------------|
| `app/core/config.py` | #4, #5 |
| `app/core/narrative_engine.py` | #10 |
| `app/main.py` | #9 |
| `app/ui/timeline.py` | #5, #7, #8 |
| `app/ui/report.py` | #4, #6, #10 |
| `app/ui/styles.py` | #4, #5, #8 |
