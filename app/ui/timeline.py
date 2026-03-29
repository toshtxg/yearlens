from __future__ import annotations

from datetime import date
from html import escape

import streamlit as st

from app.core.config import DOMAIN_EMOJIS, DOMAIN_LABELS, TONE_UI


def _render_pill_row(items: list[str]) -> None:
    pills = "".join(f"<span class='yearlens-pill'>{escape(item)}</span>" for item in items)
    st.markdown(f"<div class='yearlens-pill-row'>{pills}</div>", unsafe_allow_html=True)


def _render_list(items: list[str], list_class: str = "yearlens-list") -> None:
    bullet_list = "".join(f"<li>{escape(item)}</li>" for item in items)
    st.markdown(f"<ul class='{list_class}'>{bullet_list}</ul>", unsafe_allow_html=True)


def _render_signal_grid(signals: list[dict]) -> None:
    if not signals:
        return

    st.markdown("<div class='yearlens-section-title'>What stands out here</div>", unsafe_allow_html=True)
    trimmed_signals = signals[:3]
    for row_start in range(0, len(trimmed_signals), 2):
        row_signals = trimmed_signals[row_start:row_start + 2]
        columns = st.columns(len(row_signals), gap="small")
        for column, signal in zip(columns, row_signals):
            with column:
                st.markdown(
                    (
                        "<div class='yearlens-signal-card'>"
                        f"<div class='yearlens-signal-title'>{signal['emoji']} {escape(signal['short_text'])}</div>"
                        f"<div class='yearlens-signal-body'>{escape(signal['detail_text'])}</div>"
                        "</div>"
                    ),
                    unsafe_allow_html=True,
                )


def _render_action_cards(period: dict) -> None:
    left_col, right_col = st.columns(2, gap="small")
    with left_col:
        st.markdown("<div class='yearlens-section-title'>Lean into</div>", unsafe_allow_html=True)
        items = "".join(f"<li>{escape(f'✅ {item}')}</li>" for item in period["use_for"][:2])
        st.markdown(
            f"<div class='yearlens-action-card yearlens-action-card-up'><ul class='yearlens-compact-list'>{items}</ul></div>",
            unsafe_allow_html=True,
        )
    with right_col:
        st.markdown("<div class='yearlens-section-title'>Go slower with</div>", unsafe_allow_html=True)
        items = "".join(f"<li>{escape(f'⚠️ {item}')}</li>" for item in period["careful_with"][:2])
        st.markdown(
            f"<div class='yearlens-action-card yearlens-action-card-warn'><ul class='yearlens-compact-list'>{items}</ul></div>",
            unsafe_allow_html=True,
        )


def _render_domain_scores(period: dict) -> None:
    st.markdown("<div class='yearlens-section-title'>Main Focus Areas</div>", unsafe_allow_html=True)

    cards = []
    for domain in period["top_domains"]:
        score = period["domains"][domain]
        width = max(12, min(100, score * 10))
        cards.append(
            (
                "<div class='yearlens-score-card'>"
                f"<div class='yearlens-score-card-head'><span>{DOMAIN_EMOJIS[domain]} {escape(DOMAIN_LABELS[domain])}</span><span>{score}/10</span></div>"
                f"<div class='yearlens-score-meter'><span style='width:{width}%'></span></div>"
                "</div>"
            )
        )
    st.markdown(f"<div class='yearlens-score-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)


def _render_takeaway_card(advice: list[str]) -> None:
    if not advice:
        return
    lead = advice[0]
    follow_up = advice[1] if len(advice) > 1 else ""
    follow_up_html = f"<div class='yearlens-takeaway-sub'>{escape(follow_up)}</div>" if follow_up else ""
    st.markdown(
        (
            "<div class='yearlens-section-title'>A simple takeaway</div>"
            f"<div class='yearlens-takeaway-card'><div class='yearlens-takeaway-lead'>💡 {escape(lead)}</div>"
            f"{follow_up_html}</div>"
        ),
        unsafe_allow_html=True,
    )


def _render_explanation_blocks(period: dict) -> None:
    confidence = period["confidence_breakdown"]
    _render_pill_row(
        [
            f"Event strength {confidence['event_strength']:.0%}",
            f"Signal agreement {confidence['signal_agreement']:.0%}",
            f"Data quality {confidence['data_quality']:.0%}",
        ]
    )

    for block in period["explanation_blocks"]:
        st.markdown(
            (
                "<div class='yearlens-explainer'>"
                f"<div class='yearlens-explainer-title'>{escape(block['title'])}</div>"
                f"<div class='yearlens-explainer-summary'>{escape(block['summary'])}</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )
        _render_list(block["items"], "yearlens-compact-list")


def _clarity_label(confidence: float) -> str:
    if confidence >= 0.8:
        return "Clarity: stronger"
    if confidence >= 0.68:
        return "Clarity: moderate"
    return "Clarity: subtle"


def render_period_timeline(periods: list[dict], mode: str) -> None:
    st.caption("Read each period like a weather shift: start with the summary, then use the focus areas and cautions to decide how to move through it.")

    for index, period in enumerate(periods):
        tone_meta = TONE_UI[period["tone"]]
        primary_domain = period["top_domains"][0]
        header = f"{tone_meta['emoji']} {_pretty_date(period['start_date'])} to {_pretty_date(period['end_date'])} · {period['headline']}"

        with st.expander(header, expanded=(mode == "concise" and index == 0)):
            _render_pill_row(
                [
                    tone_meta["label"],
                    f"Main focus: {DOMAIN_LABELS[primary_domain]}",
                    _clarity_label(period["confidence"]),
                ]
            )

            st.markdown(
                (
                    "<div class='yearlens-story-card'>"
                    "<div class='yearlens-story-kicker'>Plain-language read</div>"
                    f"<div class='yearlens-period-headline'>{escape(period['headline'])}</div>"
                    f"<div class='yearlens-story-copy'>{escape(period['concise_text'] if mode == 'concise' else period['detailed_text'])}</div>"
                    f"<div class='yearlens-story-meta'>What this usually feels like: {escape(tone_meta['description'])}.</div>"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

            _render_signal_grid(period["surfaced_signals"])
            _render_action_cards(period)
            _render_domain_scores(period)
            _render_takeaway_card(period["advice"])

            if mode == "detailed":
                with st.expander("Why this period was read this way", expanded=False):
                    _render_explanation_blocks(period)


def _pretty_date(value: str) -> str:
    return date.fromisoformat(value).strftime("%b %d")
