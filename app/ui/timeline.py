import streamlit as st

from app.core.config import DOMAIN_EMOJIS, DOMAIN_LABELS, TONE_UI


def render_period_timeline(periods: list[dict], mode: str) -> None:
    st.subheader("Period Timeline")

    for period in periods:
        tone_meta = TONE_UI[period["tone"]]
        header = f"{tone_meta['emoji']} {period['start_date']} to {period['end_date']} · {tone_meta['label']}"
        with st.expander(header, expanded=(mode == "detailed")):
            metrics = st.columns(3)
            metrics[0].metric("Tone", f"{tone_meta['emoji']} {tone_meta['label']}")
            metrics[1].metric("Confidence", f"{period['confidence']:.0%}")
            primary_domain = period["top_domains"][0]
            metrics[2].metric("Primary focus", f"{DOMAIN_EMOJIS[primary_domain]} {DOMAIN_LABELS[primary_domain]}")
            st.caption(period["driver_summary"])
            st.caption(f"What this usually feels like: {tone_meta['description']}.")

            st.write(period["concise_text"] if mode == "concise" else period["detailed_text"])

            st.markdown("**Domain scores**")
            for domain in period["top_domains"]:
                st.write(f"- {DOMAIN_EMOJIS[domain]} {DOMAIN_LABELS[domain]}: {period['domains'][domain]}/10")

            st.markdown("**Advice**")
            for advice in period["advice"]:
                st.write(f"- 💡 {advice}")

            if mode == "detailed":
                st.markdown("**Drivers**")
                for driver in period["drivers"]:
                    st.write(
                        f"- 🪐 {driver['planet']} {driver['event_type']} in {driver['sign'] or 'current sign'} / house {driver['house']}: {driver['combined_effect']}"
                    )
