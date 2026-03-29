import streamlit as st

from app.core.config import DOMAIN_EMOJIS, DOMAIN_LABELS, TONE_UI


def _render_pill_row(items: list[str]) -> None:
    pills = "".join(f"<span class='yearlens-pill'>{item}</span>" for item in items)
    st.markdown(f"<div class='yearlens-pill-row'>{pills}</div>", unsafe_allow_html=True)


def _render_list(items: list[str]) -> None:
    bullet_list = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(f"<ul class='yearlens-list'>{bullet_list}</ul>", unsafe_allow_html=True)


def _render_section(title: str, items: list[str]) -> None:
    if not items:
        return
    st.markdown(f"<div class='yearlens-section-title'>{title}</div>", unsafe_allow_html=True)
    _render_list(items)


def _render_domain_scores(period: dict) -> None:
    for domain in period["top_domains"]:
        score = period["domains"][domain]
        label_col, value_col = st.columns([6, 1])
        with label_col:
            st.markdown(
                f"<div class='yearlens-score-label'>{DOMAIN_EMOJIS[domain]} {DOMAIN_LABELS[domain]}</div>",
                unsafe_allow_html=True,
            )
        with value_col:
            st.markdown(f"<div class='yearlens-score-value'>{score}/10</div>", unsafe_allow_html=True)
        st.progress(score / 10)


def _render_explanation_blocks(period: dict) -> None:
    for block in period["explanation_blocks"]:
        st.markdown(
            f"""
            <div class="yearlens-explainer">
                <div class="yearlens-explainer-title">{block['title']}</div>
                <div class="yearlens-explainer-summary">{block['summary']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _render_list(block["items"])


def render_period_timeline(periods: list[dict], mode: str) -> None:
    st.subheader("Period Timeline")
    st.caption("Start with the plain-English summary. Open detailed mode when you want to see how the signs, houses, and transit events were translated.")

    for index, period in enumerate(periods):
        tone_meta = TONE_UI[period["tone"]]
        header = f"{period['start_date']} to {period['end_date']} · {period['headline']}"
        with st.expander(header, expanded=(mode == "concise" and index == 0)):
            primary_domain = period["top_domains"][0]
            _render_pill_row(
                [
                    f"{tone_meta['emoji']} {tone_meta['label']}",
                    f"Confidence {period['confidence']:.0%} · {period['confidence_breakdown']['label']}",
                    f"{DOMAIN_EMOJIS[primary_domain]} {DOMAIN_LABELS[primary_domain]}",
                ]
            )

            st.markdown(f"<div class='yearlens-period-headline'>{period['headline']}</div>", unsafe_allow_html=True)
            st.write(period["concise_text"] if mode == "concise" else period["detailed_text"])
            _render_section("In This Window", [signal["detail_text"] for signal in period["surfaced_signals"][:4]] or period["period_guidance"])
            _render_section("Use This Window For", [f"✅ {item}" for item in period["use_for"]])
            _render_section("Be More Careful With", [f"⚠️ {item}" for item in period["careful_with"]])

            st.markdown("<div class='yearlens-section-title'>Domain Scores</div>", unsafe_allow_html=True)
            _render_domain_scores(period)

            _render_section("Advice", [f"💡 {advice}" for advice in period["advice"]])

            if mode == "detailed":
                _render_section(
                    "Confidence Breakdown",
                    [
                        f"Event strength: {period['confidence_breakdown']['event_strength']:.0%}",
                        f"Signal agreement: {period['confidence_breakdown']['signal_agreement']:.0%}",
                        f"Data quality: {period['confidence_breakdown']['data_quality']:.0%}",
                    ],
                )
                st.markdown("<div class='yearlens-section-title'>How This Was Read</div>", unsafe_allow_html=True)
                _render_explanation_blocks(period)
