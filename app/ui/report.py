from __future__ import annotations

import json
from datetime import date
from html import escape

import streamlit as st
import streamlit.components.v1 as components

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
    segment_payload = []
    tone_order: list[str] = []
    component_id = f"ylr-{periods[0]['start_date'].replace('-', '')}-{periods[-1]['end_date'].replace('-', '')}-{len(periods)}"
    for period in periods:
        tone = period["tone"]
        if tone not in tone_order:
            tone_order.append(tone)
        width = (_period_duration(period) / total_days) * 100
        size_class = _timeline_segment_size(width)
        label_html = _render_segment_label(period["start_date"], period["end_date"], size_class)
        window_text = _format_window_text(period["start_date"], period["end_date"])
        segment_payload.append(
            {
                "window": window_text,
                "tone": TONE_UI[tone]["label"],
                "headline": period["headline"],
                "description": TONE_UI[tone]["description"],
            }
        )
        segments.append(
            (
                f"<button type='button' class='ylr-segment ylr-segment--{size_class}' "
                f"data-index='{len(segment_payload) - 1}' "
                f"style='width:{width:.2f}%; background:{TONE_COLORS[tone]};' "
                f"aria-label='{escape(window_text)}. {escape(TONE_UI[tone]['label'])}. {escape(period['headline'])}'>"
                f"{label_html}"
                "</button>"
            )
        )

    legend_items = "".join(
        (
            "<span class='ylr-legend-item'>"
            f"<span class='ylr-dot' style='background:{TONE_COLORS[tone]};'></span>"
            f"{escape(TONE_UI[tone]['label'])}"
            "</span>"
        )
        for tone in tone_order
    )

    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <style>
        html, body {{
          margin: 0;
          padding: 0;
          background: transparent;
        }}
        #{component_id}.ylr-shell {{
          border: 1px solid rgba(148, 163, 184, 0.16);
          border-radius: 20px;
          padding: 0.85rem 0.9rem 0.9rem 0.9rem;
          background: rgba(18, 28, 44, 0.72);
          margin-bottom: 0.85rem;
          font-family: "Manrope", sans-serif;
          color: #eef2ff;
        }}
        #{component_id} .ylr-title {{
          font-size: 0.9rem;
          font-weight: 800;
          letter-spacing: 0.02em;
          color: #eef2ff;
          margin: 0 0 0.6rem 0;
          line-height: 1.2;
        }}
        #{component_id} .ylr-bar {{
          display: flex;
          width: 100%;
          min-height: 4rem;
          gap: 3px;
          align-items: stretch;
          background: rgba(255, 255, 255, 0.03);
          border-radius: 14px;
          overflow: hidden;
        }}
        #{component_id} .ylr-segment {{
          border: none;
          border-radius: 12px;
          min-height: 4rem;
          padding: 0.3rem 0.32rem;
          display: flex;
          align-items: center;
          justify-content: center;
          text-align: center;
          font-weight: 800;
          color: #111827;
          line-height: 1.05;
          cursor: pointer;
          transition: transform 0.15s ease, filter 0.15s ease, box-shadow 0.15s ease;
          font-family: inherit;
        }}
        #{component_id} .ylr-segment:hover,
        #{component_id} .ylr-segment:focus-visible,
        #{component_id} .ylr-segment.is-active {{
          transform: translateY(-1px);
          filter: brightness(1.02);
          box-shadow: inset 0 0 0 2px rgba(255, 255, 255, 0.22);
          outline: none;
        }}
        #{component_id} .ylr-label {{
          display: block;
          max-width: 100%;
          font-size: 0.76rem;
        }}
        #{component_id} .ylr-label-stack {{
          display: flex;
          flex-direction: column;
          gap: 0.04rem;
          align-items: center;
          font-size: 0.68rem;
        }}
        #{component_id} .ylr-segment--compact {{
          padding: 0;
        }}
        #{component_id} .ylr-segment--compact .ylr-label {{
          display: none;
        }}
        #{component_id} .ylr-detail {{
          margin-top: 0.72rem;
          border: 1px solid rgba(148, 163, 184, 0.16);
          border-radius: 16px;
          padding: 0.8rem 0.85rem;
          background: rgba(12, 18, 32, 0.9);
          min-height: 5rem;
        }}
        #{component_id} .ylr-detail-hint {{
          color: #c8d1e4;
          font-size: 0.92rem;
          line-height: 1.5;
        }}
        #{component_id} .ylr-detail-meta {{
          display: flex;
          flex-wrap: wrap;
          gap: 0.45rem;
          margin-bottom: 0.45rem;
        }}
        #{component_id} .ylr-detail-pill {{
          display: inline-flex;
          align-items: center;
          gap: 0.38rem;
          padding: 0.34rem 0.62rem;
          border-radius: 999px;
          background: rgba(42, 56, 86, 0.72);
          border: 1px solid rgba(148, 163, 184, 0.16);
          color: #eef2ff;
          font-size: 0.82rem;
          font-weight: 700;
        }}
        #{component_id} .ylr-dot {{
          width: 0.62rem;
          height: 0.62rem;
          border-radius: 999px;
          flex: 0 0 auto;
          box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.04);
        }}
        #{component_id} .ylr-detail-copy {{
          color: #eef2ff;
          font-size: 0.96rem;
          line-height: 1.45;
          font-weight: 700;
          margin-bottom: 0.16rem;
        }}
        #{component_id} .ylr-detail-sub {{
          color: #8fa0bc;
          font-size: 0.88rem;
          line-height: 1.45;
        }}
        #{component_id} .ylr-legend {{
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-top: 0.7rem;
        }}
        #{component_id} .ylr-legend-item {{
          display: inline-flex;
          align-items: center;
          gap: 0.45rem;
          padding: 0.4rem 0.7rem;
          border-radius: 999px;
          background: rgba(26, 38, 61, 0.72);
          border: 1px solid rgba(148, 163, 184, 0.14);
          color: #eef2ff;
          font-size: 0.88rem;
          font-weight: 700;
        }}
        @media (max-width: 700px) {{
          #{component_id} .ylr-bar {{
            min-height: 3.7rem;
            gap: 2px;
          }}
          #{component_id} .ylr-segment--wide .ylr-label {{
            font-size: 0.66rem;
          }}
          #{component_id} .ylr-segment--medium .ylr-label-stack {{
            font-size: 0.6rem;
          }}
          #{component_id} .ylr-segment--medium {{
            padding: 0.2rem 0.16rem;
          }}
        }}
      </style>
    </head>
    <body>
    <div id="{component_id}" class="ylr-shell">
      <div class="ylr-title">Year rhythm</div>
      <div class="ylr-bar" data-role="bar">{''.join(segments)}</div>
      <div class="ylr-detail" data-role="detail">
        <div class="ylr-detail-hint">Hover on desktop or tap on mobile to preview what each stretch is about.</div>
      </div>
      <div class="ylr-legend">{legend_items}</div>
    </div>
    <script>
      (() => {{
        const root = document.getElementById({json.dumps(component_id)});
        if (!root) return;
        const detail = root.querySelector('[data-role="detail"]');
        const segments = Array.from(root.querySelectorAll('.ylr-segment'));
        const items = {json.dumps(segment_payload)};
        let pinnedIndex = null;

        const renderPlaceholder = () => {{
          detail.innerHTML = '<div class="ylr-detail-hint">Hover on desktop or tap on mobile to preview what each stretch is about.</div>';
          segments.forEach((segment) => segment.classList.remove('is-active'));
        }};

        const renderItem = (index, persist = false) => {{
          const item = items[index];
          if (!item) return;
          if (persist) pinnedIndex = index;
          segments.forEach((segment, currentIndex) => segment.classList.toggle('is-active', currentIndex === index));
          detail.innerHTML = `
            <div class="ylr-detail-meta">
              <span class="ylr-detail-pill">${{item.window}}</span>
              <span class="ylr-detail-pill"><span class="ylr-dot" style="background:${{segments[index].style.background}};"></span>${{item.tone}}</span>
            </div>
            <div class="ylr-detail-copy">${{item.headline}}</div>
            <div class="ylr-detail-sub">${{item.description}}</div>
          `;
        }};

        segments.forEach((segment, index) => {{
          segment.addEventListener('mouseenter', () => renderItem(index));
          segment.addEventListener('focus', () => renderItem(index));
          segment.addEventListener('click', (event) => {{
            event.preventDefault();
            renderItem(index, true);
          }});
          segment.addEventListener('touchstart', () => renderItem(index, true), {{ passive: true }});
        }});

        root.querySelector('[data-role="bar"]').addEventListener('mouseleave', () => {{
          if (pinnedIndex === null) {{
            renderPlaceholder();
            return;
          }}
          renderItem(pinnedIndex, true);
        }});

        renderPlaceholder();
      }})();
    </script>
    </body>
    </html>
    """

    components.html(body, height=320, scrolling=False)


def _period_duration(period: dict) -> int:
    start = date.fromisoformat(period["start_date"])
    end = date.fromisoformat(period["end_date"])
    return (end - start).days + 1


def _timeline_segment_size(width: float) -> str:
    if width >= 13:
        return "wide"
    if width >= 8:
        return "medium"
    return "compact"


def _render_segment_label(start_value: str, end_value: str, size_class: str) -> str:
    if size_class == "compact":
        return "<span class='ylr-label'></span>"

    start = date.fromisoformat(start_value)
    end = date.fromisoformat(end_value)

    if size_class == "medium":
        return (
            "<span class='ylr-label ylr-label-stack'>"
            f"<span>{escape(start.strftime('%b'))} {start.day}</span>"
            f"<span>{escape(end.strftime('%b'))} {end.day}</span>"
            "</span>"
        )

    if start.month == end.month:
        return (
            "<span class='ylr-label'>"
            f"{escape(start.strftime('%b'))} {start.day}-{end.day}"
            "</span>"
        )

    return (
        "<span class='ylr-label ylr-label-stack'>"
        f"<span>{escape(start.strftime('%b'))} {start.day}</span>"
        f"<span>{escape(end.strftime('%b'))} {end.day}</span>"
        "</span>"
    )


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
        "For reflection and timing, not certainty or guaranteed prediction.",
        "This report stays in the current session and is not written to a database or report file by default.",
        "Do not use it as the sole basis for medical, legal, financial, or relationship decisions.",
    ]

    if "manual_coordinates" not in natal_chart["location"]["source"]:
        notes.append("If you entered a place name, that location text was sent to the geocoder to resolve coordinates.")

    notes_html = "".join(f"<li>{escape(note)}</li>" for note in notes)
    st.markdown(
        (
            "<div class='yearlens-footer-note-shell'>"
            "<div class='yearlens-footer-note-title'>A few gentle notes</div>"
            f"<ul class='yearlens-footer-note-list'>{notes_html}</ul>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )
