from datetime import date, time

from app.core.astro_engine import build_natal_chart, build_year_change_points, get_year_window
from app.core.input_schema import UserInput


def test_build_natal_chart_uses_real_engine_with_manual_location() -> None:
    user_input = UserInput(
        birth_date=date(1990, 1, 1),
        birth_time=time(12, 0),
        birth_location="Singapore",
        birth_latitude=1.3521,
        birth_longitude=103.8198,
        timezone_id="Asia/Singapore",
        target_year=2026,
    )

    natal_chart = build_natal_chart(user_input)

    assert natal_chart["engine_mode"] == "swisseph"
    assert natal_chart["ascendant"]["sign"]
    assert len(natal_chart["placements"]) == 9


def test_build_year_change_points_returns_real_events() -> None:
    user_input = UserInput(
        birth_date=date(1990, 1, 1),
        birth_time=time(12, 0),
        birth_location="Singapore",
        birth_latitude=1.3521,
        birth_longitude=103.8198,
        timezone_id="Asia/Singapore",
        target_year=2026,
    )

    natal_chart = build_natal_chart(user_input)
    window_start, window_end = get_year_window(user_input)
    change_points = build_year_change_points(user_input, natal_chart, window_start, window_end)

    assert change_points
    assert any(point.event_type in {"ingress", "station", "eclipse"} for point in change_points)


def test_get_year_window_anchor_regression_cases() -> None:
    january_birth = UserInput(
        birth_date=date(1990, 1, 1),
        birth_time=time(12, 0),
        birth_location="Singapore",
        birth_latitude=1.3521,
        birth_longitude=103.8198,
        timezone_id="Asia/Singapore",
        target_year=2026,
    )
    july_birth = UserInput(
        birth_date=date(1990, 7, 10),
        birth_time=time(12, 0),
        birth_location="Singapore",
        birth_latitude=1.3521,
        birth_longitude=103.8198,
        timezone_id="Asia/Singapore",
        target_year=2026,
    )

    january_window = get_year_window(january_birth)
    january_calendar = get_year_window(january_birth.model_copy(update={"year_anchor": "calendar"}))
    july_window = get_year_window(july_birth)
    july_calendar = get_year_window(july_birth.model_copy(update={"year_anchor": "calendar"}))

    assert january_window == january_calendar
    assert july_window != july_calendar
