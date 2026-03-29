import json

import streamlit as st


def render_year_overview(overview: dict) -> None:
    st.subheader("Year Overview")

    summary_col, confidence_col = st.columns([4, 1])
    with summary_col:
        st.write(overview["summary"])
    with confidence_col:
        st.metric("Confidence", f"{overview['confidence']:.0%}")

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
    st.download_button(
        "Download report JSON",
        data=json.dumps(report, indent=2),
        file_name="yearlens-report.json",
        mime="application/json",
    )

