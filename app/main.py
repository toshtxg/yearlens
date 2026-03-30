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
from app.ui.report import render_report_actions, render_year_overview, render_year_timeline_bar
from app.ui.styles import inject_global_styles
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
    inject_global_styles()
    st.markdown(
        """
        <div class="yearlens-hero-shell">
            <div class="yearlens-eyebrow">Year Reading Companion</div>
            <div class="yearlens-hero">
                <h1>YearLens</h1>
                <p>A calmer way to read the year ahead: clear windows, plain-language themes, and softer guidance built from your birth details without making the experience feel like a technical dashboard.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("How to use YearLens", expanded=False):
        st.markdown(
            """
            <div class="yearlens-note-card">
                <div class="yearlens-note-title">Getting started</div>
                <ul class="yearlens-note-list">
                    <li>Enter your birth details and the year you want to explore.</li>
                    <li>Read one period at a time — start in concise mode, switch to detailed when you want the deeper reasoning.</li>
                    <li>Treat the reading like guidance for reflection and timing, not certainty.</li>
                    <li>Exact birth time makes the reading more specific, especially around houses.</li>
                    <li>If location lookup is shaky, manual coordinates give a cleaner fallback.</li>
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
        st.markdown(
            """
            <div class="yearlens-placeholder-card">
                <div class="yearlens-placeholder-title">Generate your reading</div>
                <div class="yearlens-placeholder-copy">Submit the form to build a full YearLens report. If place-name lookup is unreliable, use the manual latitude, longitude, and timezone fields under advanced options.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    render_year_overview(report["year_overview"], report["metadata"])
    render_year_timeline_bar(report["periods"])

    st.markdown("<div class='yearlens-section-heading yearlens-section-heading-compact'>Read The Year</div>", unsafe_allow_html=True)
    mode = st.segmented_control(
        "Reading mode",
        options=["Concise", "Detailed"],
        default="Concise",
        selection_mode="single",
        width="content",
        label_visibility="collapsed",
    )
    render_period_timeline(report["periods"], mode=(mode or "Concise").lower())
    render_report_actions(report)

    if st.query_params.get("debug"):
        with st.expander("Debug payload", expanded=False):
            st.json(report)


if __name__ == "__main__":
    main()
