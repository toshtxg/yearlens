from __future__ import annotations

from datetime import date
from html import escape

import streamlit as st

from app.core.config import DOMAIN_EMOJIS, DOMAIN_LABELS, TONE_COLORS, TONE_UI


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
    top_domains = sorted(overview["domain_totals"], key=overview["domain_totals"].get, reverse=True)[:3]
    max_total = max(overview["domain_totals"][domain] for domain in top_domains) or 1

    cards = []
    for domain in top_domains:
        score = overview["domain_totals"][domain]
        width = max(18, min(100, round((score / max_total) * 100)))
        cards.append(
            (
                "<div class='yearlens-domain-emphasis-card'>"
                f"<div class='yearlens-domain-emphasis-head'><span>{DOMAIN_EMOJIS[domain]} {escape(DOMAIN_LABELS[domain])}</span><span>{score:.1f}</span></div>"
                f"<div class='yearlens-domain-emphasis-meter'><span style='width:{width}%'></span></div>"
                "</div>"
            )
        )

    st.markdown(
        (
            "<div class='yearlens-domain-emphasis-shell'>"
            "<div class='yearlens-section-title yearlens-section-title-inline'>Themes carrying the most weight this year</div>"
            f"<div class='yearlens-domain-emphasis-grid'>{''.join(cards)}</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_year_timeline_bar(periods: list[dict]) -> None:
    if not periods:
        return

    total_days = sum(_period_duration(period) for period in periods) or 1
    segments = []
    tone_order: list[str] = []
    for period in periods:
        tone = period["tone"]
        if tone not in tone_order:
            tone_order.append(tone)
        width = (_period_duration(period) / total_days) * 100
        label = _format_segment_label(period["start_date"], period["end_date"]) if width > 8 else ""
        tooltip = f"{_format_window_text(period['start_date'], period['end_date'])}: {TONE_UI[tone]['label']}"
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
            f"{escape(TONE_UI[tone]['label'])}"
            "</span>"
        )
        for tone in tone_order
    )

    st.markdown(
        (
            "<div class='yearlens-year-rhythm'>"
            "<div class='yearlens-section-title yearlens-section-title-inline'>Year rhythm</div>"
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
    anchor_label = "Birthday cycle" if metadata["year_anchor"] == "birthday" else "Calendar year"
    window_text = _format_window_text(metadata["window_start"], metadata["window_end"])

    st.markdown(
        f"""
        <div class="yearlens-overview-shell">
            <div class="yearlens-eyebrow">Your Year At A Glance</div>
            <div class="yearlens-overview-title">{escape(overview["summary"])}</div>
            <div class="yearlens-overview-meta">
                <span>{escape(window_text)}</span>
                <span>{escape(anchor_label)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if metadata["year_anchor"] == "birthday" and metadata["input_snapshot"]["birth_date"].endswith("-01-01"):
        st.caption("Birthday and calendar anchors are identical here because the birth date is January 1.")

    _render_tone_summary_chips(overview["tone_summary"])
    _render_domain_emphasis(overview)

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        _render_list_card("Themes That Keep Returning", overview["top_themes"], "yearlens-mini-card-theme")
    with col2:
        _render_list_card("Windows To Lean Into", overview["top_opportunity_periods"], "yearlens-mini-card-up", "period")
    with col3:
        _render_list_card("Windows To Pace Carefully", overview["top_caution_periods"], "yearlens-mini-card-warn", "period")


def render_report_actions(report: dict) -> None:
    metadata = report["metadata"]
    natal_chart = metadata["natal_chart"]

    notes = [
        "Use this as reflective guidance, not certainty or guaranteed prediction.",
        "The report stays in the current session and is not written to a database or report file by default.",
        "Do not use it as the sole basis for medical, legal, financial, or relationship decisions.",
    ]

    if "manual_coordinates" not in natal_chart["location"]["source"]:
        notes.append("If you entered a place name, that location text was sent to the geocoder to resolve coordinates.")

    with st.expander("Notes on interpretation and privacy", expanded=False):
        st.markdown("\n".join(f"- {note}" for note in notes))
        st.caption("If you want the technical details, the Debug payload stays available below.")
