from datetime import date

from app.core.astro_engine import ChangePoint
from app.core.period_engine import build_periods


def test_build_periods_returns_contiguous_windows() -> None:
    change_points = [
        ChangePoint(date=date(2026, 2, 1), planet="Mars", event_type="ingress", summary="x"),
        ChangePoint(date=date(2026, 3, 10), planet="Jupiter", event_type="station", summary="y"),
    ]

    periods = build_periods(date(2026, 1, 1), date(2026, 4, 30), change_points)

    assert periods[0].start_date == date(2026, 1, 1)
    assert periods[-1].end_date == date(2026, 4, 30)
    assert len(periods) >= 2

