from datetime import date, time

from app.core.bazi_engine import _build_recommendations, _weakest_elements, build_bazi_profile
from app.core.input_schema import UserInput


def test_build_bazi_profile_returns_expected_exact_pillars_and_counts() -> None:
    user_input = UserInput(
        birth_date=date(1990, 1, 1),
        birth_time=time(12, 0),
        birth_location="Singapore",
        birth_latitude=1.3521,
        birth_longitude=103.8198,
        timezone_id="Asia/Singapore",
        target_year=2026,
    )

    profile = build_bazi_profile(user_input)

    assert [pillar["characters"] for pillar in profile["pillars"]] == ["己巳", "丙子", "丙寅", "甲午"]
    assert profile["element_counts"] == {
        "metal": 0,
        "wood": 2,
        "water": 1,
        "fire": 4,
        "earth": 1,
    }
    assert profile["weakest_elements"] == ["metal"]
    assert profile["recommendations"]["mode"] == "single"
    assert profile["recommendations"]["items"][0]["full_label"] == "Metal (金)"


def test_build_bazi_profile_uses_local_birth_time_not_utc() -> None:
    user_input = UserInput(
        birth_date=date(1990, 1, 1),
        birth_time=time(0, 30),
        birth_location="Singapore",
        birth_latitude=1.3521,
        birth_longitude=103.8198,
        timezone_id="Asia/Singapore",
        target_year=2026,
    )

    profile = build_bazi_profile(user_input)

    assert [pillar["characters"] for pillar in profile["pillars"]] == ["己巳", "丙子", "丙寅", "戊子"]
    assert profile["basis"]["local_birth_datetime"].endswith("+08:00")


def test_build_bazi_profile_respects_li_chun_boundary() -> None:
    before_li_chun = UserInput(
        birth_date=date(2024, 2, 4),
        birth_time=time(16, 27),
        birth_location="Singapore",
        birth_latitude=1.3521,
        birth_longitude=103.8198,
        timezone_id="Asia/Singapore",
        target_year=2026,
    )
    after_li_chun = before_li_chun.model_copy(update={"birth_time": time(16, 28)})

    before_profile = build_bazi_profile(before_li_chun)
    after_profile = build_bazi_profile(after_li_chun)

    assert [pillar["characters"] for pillar in before_profile["pillars"][:2]] == ["癸卯", "乙丑"]
    assert [pillar["characters"] for pillar in after_profile["pillars"][:2]] == ["甲辰", "丙寅"]


def test_weakest_elements_returns_ordered_tie() -> None:
    weakest = _weakest_elements(
        {
            "metal": 0,
            "wood": 1,
            "water": 0,
            "fire": 3,
            "earth": 4,
        }
    )

    assert weakest == ["metal", "water"]


def test_build_recommendations_supports_pair_and_skip_modes() -> None:
    pair = _build_recommendations(["metal", "water"])
    skip = _build_recommendations(["metal", "wood", "water"])

    assert pair["mode"] == "pair"
    assert [item["full_label"] for item in pair["items"]] == ["Metal (金)", "Water (水)"]
    assert skip["mode"] == "skip"
    assert skip["items"] == []
