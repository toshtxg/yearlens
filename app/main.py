import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from pydantic import ValidationError

from app.core.astro_engine import build_natal_chart, build_year_change_points, get_year_window
from app.core.input_schema import UserInput
from app.core.meaning_engine import build_period_meanings
from app.core.narrative_engine import attach_narratives, build_year_overview
from app.core.period_engine import build_periods
from app.providers.template_narrative import TemplateNarrativeProvider
from app.ui.form import render_input_form
from app.ui.report import render_report_actions, render_year_overview
from app.ui.styles import inject_global_styles
from app.ui.theme import get_theme_preference, inject_theme_controller, render_theme_toggle
from app.ui.timeline import render_period_timeline


def generate_report(user_input: UserInput) -> dict:
    window_start, window_end = get_year_window(user_input)
    natal_chart = build_natal_chart(user_input)
    change_points = build_year_change_points(user_input, natal_chart, window_start, window_end)
    periods = build_periods(window_start, window_end, change_points)
    structured_periods = build_period_meanings(periods, natal_chart)
    provider = TemplateNarrativeProvider()
    period_payload = attach_narratives(structured_periods, provider)

    return {
        "year_overview": build_year_overview(period_payload),
        "periods": period_payload,
        "metadata": {
            "engine_mode": natal_chart["engine_mode"],
            "input_snapshot": user_input.model_dump(mode="json"),
            "year_anchor": user_input.year_anchor,
            "window_start": window_start.isoformat(),
            "window_end": window_end.isoformat(),
            "natal_chart": natal_chart,
            "change_points": [item.to_dict() for item in change_points],
        },
    }


def main() -> None:
    st.set_page_config(page_title="YearLens", page_icon="🔭", layout="wide")
    theme_preference = get_theme_preference()
    inject_theme_controller(theme_preference)
    inject_global_styles()
    hero_col, theme_col = st.columns([4, 1.3], gap="small")
    with hero_col:
        st.markdown(
            """
            <div class="yearlens-hero">
                <h1>YearLens</h1>
                <p>YearLens turns your birth details into a structured year reading with clearer windows, plain-language guidance, and a softer explanation of what the astrology is actually pointing to.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with theme_col:
        st.markdown("<div class='yearlens-kicker'>Theme</div>", unsafe_allow_html=True)
        theme_preference = render_theme_toggle()
        st.caption("Default is System.")
    inject_theme_controller(theme_preference)
    st.markdown(
        """
        <div class="yearlens-card">
            <div class="yearlens-section-title">How To Use This</div>
            <ul class="yearlens-list">
                <li>Enter your birth date, exact birth hour and minute, location, and the target year.</li>
                <li>Use <strong>birthday</strong> for a personal birthday-to-birthday cycle, or <strong>calendar</strong> for January to December.</li>
                <li>Read the timeline period by period. Start with the headline and plain-English summary, then open detailed mode if you want to see how the signs, houses, and transits were translated.</li>
                <li>If geocoding is unreliable, use the manual latitude, longitude, and timezone overrides in <strong>Advanced settings</strong>.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="yearlens-card">
            <div class="yearlens-section-title">Disclaimer And Data Handling</div>
            <ul class="yearlens-list">
                <li>This app is for reflection and personal guidance, not certainty or guaranteed prediction.</li>
                <li>Do not use it as the sole basis for medical, legal, financial, or relationship decisions.</li>
                <li>This build keeps the generated report in the current session and does not write it to a database or report file by default.</li>
                <li>If you enter a place name instead of manual coordinates, that location text may be sent to the geocoder to resolve latitude and longitude before timezone lookup happens locally.</li>
                <li>Treat the output as prompts for judgment and self-awareness, especially when the app says a period looks cleaner or more sensitive.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    payload = render_input_form()

    if payload is not None:
        try:
            user_input = UserInput.model_validate(payload)
        except ValidationError as exc:
            st.error("Input validation failed. Fix the highlighted values and try again.")
            st.code(json.dumps(exc.errors(), indent=2))
        else:
            try:
                st.session_state["yearlens_report"] = generate_report(user_input)
            except ValueError as exc:
                st.error(str(exc))
                st.info("If the location lookup is the issue, open Advanced settings and provide manual latitude, longitude, and timezone.")
            except Exception as exc:
                st.error(f"Report generation failed: {exc}")

    report = st.session_state.get("yearlens_report")
    if not report:
        st.info("Submit the form to generate a real YearLens report. Manual latitude/longitude/timezone overrides are available under Advanced settings.")
        return

    render_report_actions(report)
    render_year_overview(report["year_overview"], report["metadata"])

    mode = st.radio("Reading mode", ["concise", "detailed"], horizontal=True)
    render_period_timeline(report["periods"], mode=mode)

    with st.expander("Debug payload"):
        st.json(report)


if __name__ == "__main__":
    main()
