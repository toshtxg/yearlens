import streamlit as st

from app.core.config import DOMAIN_LABELS


def render_period_timeline(periods: list[dict], mode: str) -> None:
    st.subheader("Period Timeline")

    for period in periods:
        header = f"{period['start_date']} to {period['end_date']} · {period['tone'].title()}"
        with st.expander(header, expanded=(mode == "detailed")):
            metrics = st.columns(3)
            metrics[0].metric("Tone", period["tone"].title())
            metrics[1].metric("Confidence", f"{period['confidence']:.0%}")
            metrics[2].metric("Primary focus", DOMAIN_LABELS[period["top_domains"][0]])
            st.caption(period["driver_summary"])

            st.write(period["concise_text"] if mode == "concise" else period["detailed_text"])

            st.markdown("**Domain scores**")
            for domain in period["top_domains"]:
                st.write(f"- {DOMAIN_LABELS[domain]}: {period['domains'][domain]}/10")

            st.markdown("**Advice**")
            for advice in period["advice"]:
                st.write(f"- {advice}")

            if mode == "detailed":
                st.markdown("**Drivers**")
                for driver in period["drivers"]:
                    st.write(
                        f"- {driver['planet']} {driver['event_type']} in {driver['sign'] or 'current sign'} / house {driver['house']}: {driver['combined_effect']}"
                    )
