from __future__ import annotations

from app.core.astro_engine import build_natal_chart, build_year_change_points, get_year_window
from app.core.config import DOMAINS
from app.core.input_schema import UserInput
from app.core.meaning_engine import build_period_meanings
from app.core.narrative_engine import attach_narratives, build_year_overview
from app.core.period_engine import build_periods
from app.providers.template_narrative import TemplateNarrativeProvider


def build_multi_year_domain_trends(user_input: UserInput, years_to_show: int = 5) -> list[dict]:
    provider = TemplateNarrativeProvider()
    natal_chart = build_natal_chart(user_input)
    trend_rows: list[dict] = []

    for offset in range(max(1, years_to_show)):
        current_input = user_input.model_copy(update={"target_year": user_input.target_year + offset})
        window_start, window_end = get_year_window(current_input)
        change_points = build_year_change_points(current_input, natal_chart, window_start, window_end)
        periods = build_periods(window_start, window_end, change_points)
        structured_periods = build_period_meanings(periods, natal_chart)
        period_payload = attach_narratives(structured_periods, provider)
        overview = build_year_overview(period_payload)

        peak_windows = {}
        for domain in DOMAINS:
            peak_period = max(period_payload, key=lambda period: period["domains"][domain])
            peak_windows[domain] = {
                "score": peak_period["domains"][domain],
                "start_date": peak_period["start_date"],
                "end_date": peak_period["end_date"],
                "headline": peak_period["headline"],
                "tone": peak_period["tone"],
            }

        trend_rows.append(
            {
                "target_year": current_input.target_year,
                "window_start": window_start.isoformat(),
                "window_end": window_end.isoformat(),
                "domain_totals": overview["domain_totals"],
                "peak_windows": peak_windows,
            }
        )

    return trend_rows
