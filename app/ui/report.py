import json

import streamlit as st


def render_year_overview(overview: dict, metadata: dict) -> None:
    st.subheader("Year Overview")

    anchor_label = "Birthday cycle" if metadata["year_anchor"] == "birthday" else "Calendar year"
    window_text = f"{metadata['window_start']} to {metadata['window_end']}"

    info_col, confidence_col = st.columns([4, 1])
    with info_col:
        st.markdown(f"**Reading window:** {window_text}")
        st.caption(f"Anchor: {anchor_label}")
        birth_date = metadata["input_snapshot"]["birth_date"]
        if metadata["year_anchor"] == "birthday" and birth_date.endswith("-01-01"):
            st.info("Birthday anchor and calendar anchor are identical here because the birth date is January 1.")

    with confidence_col:
        st.metric("Confidence", f"{overview['confidence']:.0%}")

    summary_col, tone_col = st.columns([4, 2])
    with summary_col:
        st.write(overview["summary"])
    with tone_col:
        st.markdown("**Main vibe**")
        for item in overview.get("tone_summary", []):
            st.write(f"- {item}")

    st.markdown("**Top themes**")
    for theme in overview["top_themes"]:
        st.write(f"- {theme}")

    caution_col, opportunity_col = st.columns(2)
    with caution_col:
        st.markdown("**Top caution periods**")
        for item in overview["top_caution_periods"]:
            st.write(f"- {item}")

    with opportunity_col:
        st.markdown("**Top opportunity periods**")
        for item in overview["top_opportunity_periods"]:
            st.write(f"- {item}")


def render_report_actions(report: dict) -> None:
    left, right = st.columns([1, 4])
    with left:
        st.download_button(
            "Download JSON",
            data=json.dumps(report, indent=2),
            file_name="yearlens-report.json",
            mime="application/json",
        )
    with right:
        st.caption("Tip: if the year anchor looks unchanged, check the reading window dates above. January 1 birthdays produce the same birthday and calendar window.")
