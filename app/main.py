import json

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
            "window_start": window_start.isoformat(),
            "window_end": window_end.isoformat(),
            "natal_chart": natal_chart,
            "change_points": [item.to_dict() for item in change_points],
        },
    }


def main() -> None:
    st.set_page_config(page_title="YearLens", page_icon="🔭", layout="wide")
    st.title("YearLens")
    st.caption(
        "Milestone 2 build using Swiss Ephemeris-backed calculations, whole-sign houses, "
        "and rule-based interpretations. Manual coordinates/timezone can override geocoding when needed."
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
            except Exception as exc:
                st.error(f"Report generation failed: {exc}")

    report = st.session_state.get("yearlens_report")
    if not report:
        st.info("Submit the form to generate a real YearLens report. Manual latitude/longitude/timezone overrides are available under Advanced settings.")
        return

    render_report_actions(report)
    render_year_overview(report["year_overview"])

    mode = st.radio("Reading mode", ["concise", "detailed"], horizontal=True)
    render_period_timeline(report["periods"], mode=mode)

    with st.expander("Debug payload"):
        st.json(report)


if __name__ == "__main__":
    main()
