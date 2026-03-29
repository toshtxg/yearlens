from __future__ import annotations

from datetime import date
from html import escape

import streamlit as st

from app.core.config import DOMAIN_EMOJIS, TONE_COLORS, get_domain_labels, get_tone_ui
from app.i18n import get_lang, t


def _render_pill_row(items: list[str]) -> None:
    pills = "".join(f"<span class='yearlens-pill'>{escape(item)}</span>" for item in items)
    st.markdown(f"<div class='yearlens-pill-row'>{pills}</div>", unsafe_allow_html=True)


def _render_list_card(title: str, items: list[str], card_class: str = "", card_kind: str = "plain") -> None:
    if card_kind == "period":
        list_items = "".join(_render_period_item(item) for item in items)
    else:
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
        return str(t("confidence_strong"))
    if confidence >= 0.68:
        return str(t("confidence_moderate"))
    return str(t("confidence_soft"))


def _render_period_item(item: str) -> str:
    if " · " not in item or " to " not in item:
        return f"<li>{escape(item)}</li>"

    range_part, headline = item.split(" · ", 1)
    start_text, end_text = range_part.split(" to ", 1)
    try:
        start_date = date.fromisoformat(start_text)
        end_date = date.fromisoformat(end_text)
    except ValueError:
        return f"<li>{escape(item)}</li>"

    date_label = _format_date_range(start_date, end_date)
    return (
        "<li class='yearlens-mini-period-item'>"
        f"<div class='yearlens-mini-period-date'>{escape(date_label)}</div>"
        f"<div class='yearlens-mini-period-copy'>{escape(headline)}</div>"
        "</li>"
    )


def _format_date_range(start: date, end: date) -> str:
    if start.year == end.year:
        if start.month == end.month:
            return f"{start.strftime('%b')} {start.day} to {end.day}, {start.year}"
        return f"{start.strftime('%b')} {start.day} to {end.strftime('%b')} {end.day}, {start.year}"
    return f"{start.strftime('%b')} {start.day}, {start.year} to {end.strftime('%b')} {end.day}, {end.year}"


def _format_window_text(start_value: str, end_value: str) -> str:
    return _format_date_range(date.fromisoformat(start_value), date.fromisoformat(end_value))


def _render_tone_summary_chips(tone_summary: list[dict]) -> None:
    chips = []
    for item in tone_summary:
        color = TONE_COLORS[item["tone"]]
        chips.append(
            (
                "<span class='yearlens-tone-chip'>"
                f"<span class='yearlens-tone-dot' style='background:{color};'></span>"
                f"{escape(item['label'])}"
                "</span>"
            )
        )
    st.markdown(f"<div class='yearlens-tone-chip-row'>{''.join(chips)}</div>", unsafe_allow_html=True)


def _render_domain_emphasis(overview: dict) -> None:
    lang = get_lang()
    domain_labels = get_domain_labels(lang)
    top_domains = sorted(overview["domain_totals"], key=overview["domain_totals"].get, reverse=True)[:3]
    max_total = max(overview["domain_totals"][domain] for domain in top_domains) or 1

    cards = []
    for domain in top_domains:
        score = overview["domain_totals"][domain]
        width = max(18, min(100, round((score / max_total) * 100)))
        cards.append(
            (
                "<div class='yearlens-domain-emphasis-card'>"
                f"<div class='yearlens-domain-emphasis-head'><span>{DOMAIN_EMOJIS[domain]} {escape(domain_labels[domain])}</span><span>{score:.1f}</span></div>"
                f"<div class='yearlens-domain-emphasis-meter'><span style='width:{width}%'></span></div>"
                "</div>"
            )
        )

    st.markdown(
        (
            "<div class='yearlens-domain-emphasis-shell'>"
            f"<div class='yearlens-section-title yearlens-section-title-inline'>{escape(str(t('themes_weight')))}</div>"
            f"<div class='yearlens-domain-emphasis-grid'>{''.join(cards)}</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_year_timeline_bar(periods: list[dict]) -> None:
    if not periods:
        return

    lang = get_lang()
    tone_ui = get_tone_ui(lang)
    total_days = sum(_period_duration(period) for period in periods) or 1
    segments = []
    tone_order: list[str] = []
    for period in periods:
        tone = period["tone"]
        if tone not in tone_order:
            tone_order.append(tone)
        width = (_period_duration(period) / total_days) * 100
        label = _format_segment_label(period["start_date"], period["end_date"]) if width > 8 else ""
        tooltip = f"{_format_window_text(period['start_date'], period['end_date'])}: {tone_ui[tone]['label']}"
        segments.append(
            (
                f"<div class='yearlens-timeline-segment' style='width:{width:.2f}%; background:{TONE_COLORS[tone]};' title='{escape(tooltip)}'>"
                f"{escape(label)}"
                "</div>"
            )
        )

    legend_items = "".join(
        (
            "<span class='yearlens-timeline-legend-item'>"
            f"<span class='yearlens-tone-dot' style='background:{TONE_COLORS[tone]};'></span>"
            f"{escape(tone_ui[tone]['label'])}"
            "</span>"
        )
        for tone in tone_order
    )

    st.markdown(
        (
            "<div class='yearlens-year-rhythm'>"
            f"<div class='yearlens-section-title yearlens-section-title-inline'>{escape(str(t('year_rhythm')))}</div>"
            f"<div class='yearlens-timeline-bar'>{''.join(segments)}</div>"
            f"<div class='yearlens-timeline-legend'>{legend_items}</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _period_duration(period: dict) -> int:
    start = date.fromisoformat(period["start_date"])
    end = date.fromisoformat(period["end_date"])
    return (end - start).days + 1


def _format_segment_label(start_value: str, end_value: str) -> str:
    start = date.fromisoformat(start_value)
    end = date.fromisoformat(end_value)
    if start.month == end.month:
        return f"{start.strftime('%b')} {start.day}-{end.day}"
    return f"{start.strftime('%b')} {start.day}-{end.strftime('%b')} {end.day}"


def render_year_overview(overview: dict, metadata: dict) -> None:
    lang = get_lang()
    anchor_label = str(t("anchor_birthday")) if metadata["year_anchor"] == "birthday" else str(t("anchor_calendar"))
    window_text = _format_window_text(metadata["window_start"], metadata["window_end"])

    st.markdown(
        f"""
        <div class="yearlens-overview-shell">
            <div class="yearlens-eyebrow">{escape(str(t("overview_eyebrow")))}</div>
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
        st.caption(str(t("overview_jan1_note")))

    _render_tone_summary_chips(overview["tone_summary"])
    _render_domain_emphasis(overview)

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        _render_list_card(str(t("themes_returning")), overview["top_themes"], "yearlens-mini-card-theme")
    with col2:
        _render_list_card(str(t("windows_lean_into")), overview["top_opportunity_periods"], "yearlens-mini-card-up", "period")
    with col3:
        _render_list_card(str(t("windows_pace_carefully")), overview["top_caution_periods"], "yearlens-mini-card-warn", "period")


def render_report_actions(report: dict) -> None:
    metadata = report["metadata"]
    natal_chart = metadata["natal_chart"]

    notes = list(t("notes_items"))

    if "manual_coordinates" not in natal_chart["location"]["source"]:
        notes.append(str(t("notes_geocoder")))

    with st.expander(str(t("notes_title")), expanded=False):
        st.markdown("\n".join(f"- {note}" for note in notes))
        st.caption(str(t("notes_debug_hint")))
