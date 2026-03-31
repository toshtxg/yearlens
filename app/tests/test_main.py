from datetime import date, time

from app.main import generate_report
from app.core.input_schema import UserInput


def test_generate_report_includes_bazi_profile(monkeypatch) -> None:
    user_input = UserInput(
        birth_date=date(1990, 1, 1),
        birth_time=time(12, 0),
        birth_location="Singapore",
        target_year=2026,
    )
    fake_natal_chart = {
        "engine_mode": "stub",
        "location": {"source": "manual_coordinates"},
        "warnings": [],
    }
    fake_bazi_profile = {"pillars": [], "element_counts": {}, "recommendations": {"mode": "skip", "items": []}}

    monkeypatch.setattr("app.main.get_year_window", lambda _: (date(2026, 1, 1), date(2026, 12, 31)))
    monkeypatch.setattr("app.main.build_natal_chart", lambda _: fake_natal_chart)
    monkeypatch.setattr("app.main.build_bazi_profile", lambda _: fake_bazi_profile)
    monkeypatch.setattr("app.main.build_year_change_points", lambda *args, **kwargs: [])
    monkeypatch.setattr("app.main.build_periods", lambda *args, **kwargs: [{"id": "p1", "confidence": 0.7}])
    monkeypatch.setattr("app.main.build_period_meanings", lambda periods, natal_chart: periods)
    monkeypatch.setattr("app.main.attach_narratives", lambda periods, provider: periods)
    monkeypatch.setattr("app.main.build_year_overview", lambda periods: {"summary": "stub"})

    report = generate_report(user_input)

    assert report["metadata"]["bazi_profile"] == fake_bazi_profile
    assert report["metadata"]["natal_chart"] == fake_natal_chart
