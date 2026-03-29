from datetime import date

from app.core.meaning_engine import build_period_meanings
from app.core.period_engine import PeriodWindow


def test_build_period_meanings_returns_expected_shape() -> None:
    natal_chart = {
        "placements": [
            {"planet": "Mars", "sign": "Aries", "house": 6},
            {"planet": "Jupiter", "sign": "Taurus", "house": 10},
        ]
    }
    periods = [
        PeriodWindow(id="p1", start_date=date(2026, 1, 1), end_date=date(2026, 1, 31), drivers=[]),
    ]

    payload = build_period_meanings(periods, natal_chart)

    assert payload[0]["id"] == "p1"
    assert "career_work" in payload[0]["domains"]
    assert payload[0]["advice"]
    assert "signals" in payload[0]
    assert "decision_timing" in payload[0]["signals"]
    assert payload[0]["period_guidance"]
