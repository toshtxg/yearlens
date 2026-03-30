from datetime import date, time

from app.core.input_schema import UserInput
from app.core.trend_engine import build_multi_year_domain_trends


def test_build_multi_year_domain_trends_returns_requested_years(monkeypatch) -> None:
    user_input = UserInput(
        birth_date=date(1990, 1, 1),
        birth_time=time(12, 0),
        birth_location="Singapore",
        target_year=2026,
    )

    monkeypatch.setattr("app.core.trend_engine.build_natal_chart", lambda _: {"engine_mode": "stub"})
    monkeypatch.setattr("app.core.trend_engine.get_year_window", lambda current_input: (date(current_input.target_year, 1, 1), date(current_input.target_year, 12, 31)))
    monkeypatch.setattr("app.core.trend_engine.build_year_change_points", lambda *args, **kwargs: [])
    monkeypatch.setattr("app.core.trend_engine.build_periods", lambda *args, **kwargs: [object()])
    monkeypatch.setattr(
        "app.core.trend_engine.build_period_meanings",
        lambda *args, **kwargs: [
            {
                "start_date": "2026-01-01",
                "end_date": "2026-03-01",
                "headline": "Peak relationships window",
                "tone": "supportive",
                "domains": {
                    "career_work": 3,
                    "money_finance": 4,
                    "relationships": 7,
                    "health_emotional": 5,
                    "travel_overseas": 2,
                    "study_growth": 6,
                },
                "confidence": 0.8,
            }
        ],
    )
    monkeypatch.setattr("app.core.trend_engine.attach_narratives", lambda periods, provider: periods)
    monkeypatch.setattr(
        "app.core.trend_engine.build_year_overview",
        lambda periods: {
            "domain_totals": {
                "career_work": 3.0,
                "money_finance": 4.0,
                "relationships": 7.0,
                "health_emotional": 5.0,
                "travel_overseas": 2.0,
                "study_growth": 6.0,
            }
        },
    )

    trend_rows = build_multi_year_domain_trends(user_input, years_to_show=3)

    assert [row["target_year"] for row in trend_rows] == [2026, 2027, 2028]
    assert trend_rows[0]["domain_totals"]["relationships"] == 7.0
    assert trend_rows[0]["peak_windows"]["relationships"]["headline"] == "Peak relationships window"
