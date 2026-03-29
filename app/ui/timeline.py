from __future__ import annotations

from datetime import date
from html import escape

import streamlit as st

from app.core.config import DOMAIN_EMOJIS, TONE_COLORS, get_domain_labels, get_tone_ui
from app.i18n import get_lang, t


def _render_pill_row(items: list[str]) -> None:
    pills = "".join(
        f"<span class='yearlens-pill{' yearlens-pill-now' if item == str(t('pill_now')) else ''}'>{escape(item)}</span>"
        for item in items
    )
    st.markdown(f"<div class='yearlens-pill-row'>{pills}</div>", unsafe_allow_html=True)


def _render_list(items: list[str], list_class: str = "yearlens-list") -> None:
    bullet_list = "".join(f"<li>{escape(item)}</li>" for item in items)
    st.markdown(f"<ul class='{list_class}'>{bullet_list}</ul>", unsafe_allow_html=True)


def _render_signal_grid(signals: list[dict]) -> None:
    _render_signal_grid_with_limit(signals, 3)


def _render_signal_grid_with_limit(signals: list[dict], limit: int) -> None:
    if not signals:
        return

    st.markdown(f"<div class='yearlens-section-title'>{escape(str(t('signals_title')))}</div>", unsafe_allow_html=True)
    trimmed_signals = signals[:limit]
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
        st.markdown(f"<div class='yearlens-section-title'>{escape(str(t('lean_into')))}</div>", unsafe_allow_html=True)
        items = "".join(f"<li>{escape(f'✅ {item}')}</li>" for item in period["use_for"][:2])
        st.markdown(
            f"<div class='yearlens-action-card yearlens-action-card-up'><ul class='yearlens-compact-list'>{items}</ul></div>",
            unsafe_allow_html=True,
        )
    with right_col:
        st.markdown(f"<div class='yearlens-section-title'>{escape(str(t('go_slower')))}</div>", unsafe_allow_html=True)
        items = "".join(f"<li>{escape(f'⚠️ {item}')}</li>" for item in period["careful_with"][:2])
        st.markdown(
            f"<div class='yearlens-action-card yearlens-action-card-warn'><ul class='yearlens-compact-list'>{items}</ul></div>",
            unsafe_allow_html=True,
        )


def _render_domain_scores(period: dict) -> None:
    lang = get_lang()
    domain_labels = get_domain_labels(lang)
    st.markdown(f"<div class='yearlens-section-title'>{escape(str(t('focus_areas')))}</div>", unsafe_allow_html=True)

    cards = []
    for domain in period["top_domains"]:
        score = period["domains"][domain]
        width = max(12, min(100, score * 10))
        cards.append(
            (
                "<div class='yearlens-score-card'>"
                f"<div class='yearlens-score-card-head'><span>{DOMAIN_EMOJIS[domain]} {escape(domain_labels[domain])}</span><span>{score}/10</span></div>"
                f"<div class='yearlens-score-meter'><span style='width:{width}%'></span></div>"
                "</div>"
            )
        )
    st.markdown(f"<div class='yearlens-score-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)


def _render_focus_pills(period: dict) -> None:
    lang = get_lang()
    domain_labels = get_domain_labels(lang)
    items = [f"{DOMAIN_EMOJIS[domain]} {domain_labels[domain]}" for domain in period["top_domains"]]
    _render_pill_row(items)


def _render_takeaway_card(advice: list[str]) -> None:
    if not advice:
        return
    lead = advice[0]
    follow_up = advice[1] if len(advice) > 1 else ""
    follow_up_html = f"<div class='yearlens-takeaway-sub'>{escape(follow_up)}</div>" if follow_up else ""
    st.markdown(
        (
            f"<div class='yearlens-section-title'>{escape(str(t('takeaway_title')))}</div>"
            f"<div class='yearlens-takeaway-card'><div class='yearlens-takeaway-lead'>💡 {escape(lead)}</div>"
            f"{follow_up_html}</div>"
        ),
        unsafe_allow_html=True,
    )


def _render_explanation_blocks(period: dict) -> None:
    confidence = period["confidence_breakdown"]
    _render_pill_row(
        [
            str(t("event_strength", value=f"{confidence['event_strength']:.0%}")),
            str(t("signal_agreement", value=f"{confidence['signal_agreement']:.0%}")),
            str(t("data_quality", value=f"{confidence['data_quality']:.0%}")),
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
        return str(t("clarity_strong"))
    if confidence >= 0.68:
        return str(t("clarity_moderate"))
    return str(t("clarity_general"))


def render_period_timeline(periods: list[dict], mode: str) -> None:
    lang = get_lang()
    domain_labels = get_domain_labels(lang)
    tone_ui = get_tone_ui(lang)

    st.caption(str(t("timeline_caption")))
    today = date.today()
    current_period_id = next(
        (
            period["id"]
            for period in periods
            if date.fromisoformat(period["start_date"]) <= today <= date.fromisoformat(period["end_date"])
        ),
        None,
    )

    for index, period in enumerate(periods):
        tone_meta = tone_ui[period["tone"]]
        primary_domain = period["top_domains"][0]
        header = f"{tone_meta['emoji']} {_pretty_header_range(period['start_date'], period['end_date'])} · {period['headline']}"
        tone_color = TONE_COLORS[period["tone"]]
        is_current = period["id"] == current_period_id

        st.markdown(
            f"<div class='yearlens-period-accent' style='background:{tone_color};'></div>",
            unsafe_allow_html=True,
        )

        with st.expander(header, expanded=is_current or (current_period_id is None and mode == "concise" and index == 0)):
            header_pills = [
                _pretty_date_range(period["start_date"], period["end_date"]),
                tone_meta["label"],
                str(t("main_focus", domain=domain_labels[primary_domain])),
            ]
            if is_current:
                header_pills.insert(0, str(t("pill_now")))
            if mode == "detailed":
                header_pills.append(_clarity_label(period["confidence"]))
            _render_pill_row(header_pills)

            if mode == "concise":
                st.markdown(
                    (
                        "<div class='yearlens-story-card yearlens-story-card-concise'>"
                        f"<div class='yearlens-period-headline'>{escape(period['headline'])}</div>"
                        f"<div class='yearlens-story-copy'>{escape(period['concise_text'])}</div>"
                        "</div>"
                    ),
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    (
                        "<div class='yearlens-story-card'>"
                        f"<div class='yearlens-story-kicker'>{escape(str(t('story_kicker')))}</div>"
                        f"<div class='yearlens-period-headline'>{escape(period['headline'])}</div>"
                        f"<div class='yearlens-story-copy'>{escape(period['detailed_text'])}</div>"
                        f"<div class='yearlens-story-meta'>{escape(str(t('story_meta', description=tone_meta['description'])))}</div>"
                        "</div>"
                    ),
                    unsafe_allow_html=True,
                )

            if mode == "detailed":
                _render_signal_grid_with_limit(period["surfaced_signals"], 3)
            _render_action_cards(period)
            if mode == "concise":
                st.markdown(f"<div class='yearlens-section-title'>{escape(str(t('focus_areas')))}</div>", unsafe_allow_html=True)
                _render_focus_pills(period)
            else:
                _render_domain_scores(period)
                _render_takeaway_card(period["advice"])

            if mode == "detailed":
                with st.expander(str(t("explanation_title")), expanded=False):
                    _render_explanation_blocks(period)


def _pretty_date(value: str) -> str:
    return date.fromisoformat(value).strftime("%b %d")


def _pretty_date_range(start_value: str, end_value: str) -> str:
    start = date.fromisoformat(start_value)
    end = date.fromisoformat(end_value)
    if start.year == end.year:
        if start.month == end.month:
            return f"{start.strftime('%b')} {start.day} to {end.day}, {start.year}"
        return f"{start.strftime('%b')} {start.day} to {end.strftime('%b')} {end.day}, {start.year}"
    return f"{start.strftime('%b')} {start.day}, {start.year} to {end.strftime('%b')} {end.day}, {end.year}"


def _pretty_header_range(start_value: str, end_value: str) -> str:
    start = date.fromisoformat(start_value)
    end = date.fromisoformat(end_value)
    if start.year == end.year:
        if start.month == end.month:
            return f"{start.strftime('%b')} {start.day} to {end.day}"
        return f"{start.strftime('%b')} {start.day} to {end.strftime('%b')} {end.day}"
    return f"{start.strftime('%b')} {start.day}, {start.year} to {end.strftime('%b')} {end.day}, {end.year}"
