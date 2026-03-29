import streamlit as st

from app.core.config import DOMAIN_EMOJIS, DOMAIN_LABELS, TONE_UI


def _render_pill_row(items: list[str]) -> None:
    pills = "".join(f"<span class='yearlens-pill'>{item}</span>" for item in items)
    st.markdown(f"<div class='yearlens-pill-row'>{pills}</div>", unsafe_allow_html=True)


def _render_list(items: list[str]) -> None:
    bullet_list = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(f"<ul class='yearlens-list'>{bullet_list}</ul>", unsafe_allow_html=True)


def render_period_timeline(periods: list[dict], mode: str) -> None:
    st.subheader("Period Timeline")

    for period in periods:
        tone_meta = TONE_UI[period["tone"]]
        header = f"{tone_meta['emoji']} {period['start_date']} to {period['end_date']} · {tone_meta['label']}"
        with st.expander(header, expanded=(mode == "detailed")):
            primary_domain = period["top_domains"][0]
            _render_pill_row(
                [
                    f"{tone_meta['emoji']} {tone_meta['label']}",
                    f"Confidence {period['confidence']:.0%}",
                    f"{DOMAIN_EMOJIS[primary_domain]} {DOMAIN_LABELS[primary_domain]}",
                ]
            )
            st.caption(period["driver_summary"])
            st.caption(f"What this usually feels like: {tone_meta['description']}.")

            st.write(period["concise_text"] if mode == "concise" else period["detailed_text"])

            st.markdown("**In This Window**")
            _render_list(period["period_guidance"])

            st.markdown("**Domain Scores**")
            _render_list(
                [f"{DOMAIN_EMOJIS[domain]} {DOMAIN_LABELS[domain]}: {period['domains'][domain]}/10" for domain in period["top_domains"]]
            )

            st.markdown("**Advice**")
            _render_list([f"💡 {advice}" for advice in period["advice"]])

            if mode == "detailed":
                st.markdown("**Drivers**")
                _render_list(
                    [
                        f"🪐 {driver['planet']} {driver['event_type']} in {driver['sign'] or 'current sign'} / house {driver['house']}: {driver['combined_effect']}"
                        for driver in period["drivers"]
                    ]
                )
