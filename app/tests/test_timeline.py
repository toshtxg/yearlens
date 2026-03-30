from datetime import date

from app.ui.timeline import _resolve_current_period_id


def test_resolve_current_period_id_matches_today_only_for_current_target_year() -> None:
    periods = [
        {"id": "p1", "start_date": "2026-01-01", "end_date": "2026-03-04"},
        {"id": "p2", "start_date": "2026-03-05", "end_date": "2026-04-19"},
    ]

    assert _resolve_current_period_id(periods, target_year=2026, today=date(2026, 3, 12)) == "p2"


def test_resolve_current_period_id_is_disabled_for_non_current_target_year() -> None:
    periods = [
        {"id": "p1", "start_date": "2026-01-01", "end_date": "2026-03-04"},
        {"id": "p2", "start_date": "2026-03-05", "end_date": "2026-04-19"},
    ]

    assert _resolve_current_period_id(periods, target_year=2025, today=date(2026, 3, 12)) is None
