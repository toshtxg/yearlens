import json
import sys
from html import escape
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
from app.i18n import get_lang, t
from app.providers.template_narrative import TemplateNarrativeProvider
from app.ui.form import render_input_form
from app.ui.report import render_report_actions, render_year_overview, render_year_timeline_bar
from app.ui.styles import inject_global_styles
from app.ui.timeline import render_period_timeline


def generate_report(user_input: UserInput, lang: str = "en") -> dict:
    window_start, window_end = get_year_window(user_input)
    natal_chart = build_natal_chart(user_input)
    change_points = build_year_change_points(user_input, natal_chart, window_start, window_end)
    periods = build_periods(window_start, window_end, change_points)
    structured_periods = build_period_meanings(periods, natal_chart, lang)
    provider = TemplateNarrativeProvider()
    period_payload = attach_narratives(structured_periods, provider, lang)

    return {
        "year_overview": build_year_overview(period_payload, lang),
        "periods": period_payload,
        "lang": lang,
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

    # Language toggle in sidebar
    lang_options = {"English": "en", "中文": "zh"}
    selected_lang = st.sidebar.selectbox(
        "🌐 Language / 语言",
        list(lang_options),
        index=list(lang_options.values()).index(st.session_state.get("lang", "en")),
    )
    new_lang = lang_options[selected_lang]
    if new_lang != st.session_state.get("lang", "en"):
        st.session_state["lang"] = new_lang
        st.session_state.pop("yearlens_report", None)
        st.rerun()
    st.session_state["lang"] = new_lang

    lang = get_lang()

    st.markdown(
        f"""
        <div class="yearlens-hero-shell">
            <div class="yearlens-eyebrow">{escape(str(t("hero_eyebrow")))}</div>
            <div class="yearlens-hero">
                <h1>{escape(str(t("hero_title")))}</h1>
                <p>{escape(str(t("hero_tagline")))}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    howto_items = t("howto_items")
    items_html = "".join(f"<li>{escape(item)}</li>" for item in howto_items)
    with st.expander(str(t("howto_title")), expanded=False):
        st.markdown(
            f"""
            <div class="yearlens-note-card">
                <div class="yearlens-note-title">{escape(str(t("howto_section_title")))}</div>
                <ul class="yearlens-note-list">
                    {items_html}
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
            st.error(str(t("error_validation")))
            st.code(json.dumps(exc.errors(), indent=2))
        else:
            try:
                st.session_state["yearlens_report"] = generate_report(user_input, lang)
            except ValueError as exc:
                st.error(str(exc))
                st.info(str(t("error_location_hint")))
            except Exception as exc:
                st.error(str(t("error_report", error=str(exc))))

    report = st.session_state.get("yearlens_report")
    if not report:
        st.markdown(
            f"""
            <div class="yearlens-placeholder-card">
                <div class="yearlens-placeholder-title">{escape(str(t("placeholder_title")))}</div>
                <div class="yearlens-placeholder-copy">{escape(str(t("placeholder_copy")))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    render_year_overview(report["year_overview"], report["metadata"])
    render_year_timeline_bar(report["periods"])

    st.markdown(
        f"<div class='yearlens-section-heading yearlens-section-heading-compact'>{escape(str(t('read_the_year')))}</div>",
        unsafe_allow_html=True,
    )
    mode = st.segmented_control(
        "Reading mode",
        options=[str(t("mode_concise")), str(t("mode_detailed"))],
        default=str(t("mode_concise")),
        selection_mode="single",
        width="content",
        label_visibility="collapsed",
    )
    mode_key = "detailed" if mode == str(t("mode_detailed")) else "concise"
    render_period_timeline(report["periods"], mode=mode_key)
    render_report_actions(report)

    if st.query_params.get("debug"):
        with st.expander("Debug payload", expanded=False):
            st.json(report)


if __name__ == "__main__":
    main()
