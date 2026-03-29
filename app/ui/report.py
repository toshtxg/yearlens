from __future__ import annotations

from html import escape

import streamlit as st


def _render_pill_row(items: list[str]) -> None:
    pills = "".join(f"<span class='yearlens-pill'>{escape(item)}</span>" for item in items)
    st.markdown(f"<div class='yearlens-pill-row'>{pills}</div>", unsafe_allow_html=True)


def _render_list_card(title: str, items: list[str], card_class: str = "") -> None:
    list_items = "".join(f"<li>{escape(item)}</li>" for item in items)
    classes = "yearlens-mini-card"
    if card_class:
        classes += f" {card_class}"
    st.markdown(
        f"<div class='{classes}'><div class='yearlens-mini-card-title'>{escape(title)}</div><ul class='yearlens-mini-list'>{list_items}</ul></div>",
        unsafe_allow_html=True,
    )


def _year_signal_label(confidence: float) -> str:
    if confidence >= 0.8:
        return "Clearer overall signal"
    if confidence >= 0.68:
        return "Mixed but usable signal"
    return "Gentler, lower-contrast signal"


def render_year_overview(overview: dict, metadata: dict) -> None:
    anchor_label = "Birthday cycle" if metadata["year_anchor"] == "birthday" else "Calendar year"
    window_text = f"{metadata['window_start']} to {metadata['window_end']}"

    st.markdown(
        f"""
        <div class="yearlens-overview-shell">
            <div class="yearlens-eyebrow">Your Year At A Glance</div>
            <div class="yearlens-overview-title">{escape(overview["summary"])}</div>
            <div class="yearlens-overview-meta">
                <span>{escape(window_text)}</span>
                <span>{escape(anchor_label)}</span>
                <span>{escape(_year_signal_label(overview["confidence"]))}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if metadata["year_anchor"] == "birthday" and metadata["input_snapshot"]["birth_date"].endswith("-01-01"):
        st.caption("Birthday and calendar anchors are identical here because the birth date is January 1.")

    _render_pill_row(overview.get("tone_summary", []))

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        _render_list_card("Themes That Keep Returning", overview["top_themes"], "yearlens-mini-card-theme")
    with col2:
        _render_list_card("Windows To Lean Into", overview["top_opportunity_periods"], "yearlens-mini-card-up")
    with col3:
        _render_list_card("Windows To Pace Carefully", overview["top_caution_periods"], "yearlens-mini-card-warn")


def render_report_actions(report: dict) -> None:
    metadata = report["metadata"]
    natal_chart = metadata["natal_chart"]

    notes = [
        "Use this as reflective guidance, not certainty or guaranteed prediction.",
        "The report stays in the current session and is not written to a database or report file by default.",
        "Do not use it as the sole basis for medical, legal, financial, or relationship decisions.",
    ]

    if "manual_coordinates" not in natal_chart["location"]["source"]:
        notes.append("If you entered a place name, that location text was sent to the geocoder to resolve coordinates.")

    with st.expander("Notes on interpretation and privacy", expanded=False):
        st.markdown("\n".join(f"- {note}" for note in notes))
        st.caption("If you want the technical details, the Debug payload stays available below.")
