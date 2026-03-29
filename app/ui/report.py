import json

import streamlit as st


def _render_pill_row(items: list[str]) -> None:
    pills = "".join(f"<span class='yearlens-pill'>{item}</span>" for item in items)
    st.markdown(f"<div class='yearlens-pill-row'>{pills}</div>", unsafe_allow_html=True)


def _render_list(title: str, items: list[str]) -> None:
    st.markdown(f"<div class='yearlens-section-title'>{title}</div>", unsafe_allow_html=True)
    bullet_list = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(f"<ul class='yearlens-list'>{bullet_list}</ul>", unsafe_allow_html=True)


def render_year_overview(overview: dict, metadata: dict) -> None:
    st.subheader("Year Overview")

    anchor_label = "Birthday cycle" if metadata["year_anchor"] == "birthday" else "Calendar year"
    window_text = f"{metadata['window_start']} to {metadata['window_end']}"
    st.markdown(
        f"""
        <div class="yearlens-card">
            <div class="yearlens-kicker">Reading Window</div>
            <div class="yearlens-value">{window_text}</div>
            <div class="yearlens-kicker" style="margin-top:0.5rem;">Anchor</div>
            <div class="yearlens-value">{anchor_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    birth_date = metadata["input_snapshot"]["birth_date"]
    if metadata["year_anchor"] == "birthday" and birth_date.endswith("-01-01"):
        st.info("Birthday anchor and calendar anchor are identical here because the birth date is January 1.")

    _render_pill_row(
        [
            f"Confidence {overview['confidence']:.0%}",
            *overview.get("tone_summary", []),
        ]
    )

    st.write(overview["summary"])
    _render_list("Top Themes", overview["top_themes"])
    _render_list("Top Caution Periods", overview["top_caution_periods"])
    _render_list("Top Opportunity Periods", overview["top_opportunity_periods"])


def render_report_actions(report: dict) -> None:
    st.download_button(
        "Download JSON",
        data=json.dumps(report, indent=2),
        file_name="yearlens-report.json",
        mime="application/json",
        use_container_width=True,
    )
    st.caption("Tip: if the year anchor looks unchanged, check the reading window dates above. January 1 birthdays produce the same birthday and calendar window.")
