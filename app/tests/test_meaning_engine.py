from datetime import date

from app.core.astro_engine import ChangePoint
from app.core.meaning_engine import build_period_meanings
from app.core.period_engine import PeriodWindow


def _natal_chart() -> dict:
    return {
        "ephemeris_backend": "moshier_fallback",
        "warnings": [],
        "location": {"source": "manual_coordinates+manual_timezone"},
        "placements": [
            {"planet": "Moon", "sign": "Cancer", "house": 1},
            {"planet": "Mars", "sign": "Aries", "house": 6},
            {"planet": "Jupiter", "sign": "Taurus", "house": 10},
            {"planet": "Saturn", "sign": "Capricorn", "house": 7},
        ],
    }


def test_build_period_meanings_returns_expected_shape() -> None:
    periods = [
        PeriodWindow(id="p1", start_date=date(2026, 1, 1), end_date=date(2026, 1, 31), drivers=[]),
    ]

    payload = build_period_meanings(periods, _natal_chart())

    assert payload[0]["id"] == "p1"
    assert "career_work" in payload[0]["domains"]
    assert payload[0]["advice"]
    assert payload[0]["surfaced_signals"] is not None
    assert payload[0]["confidence_breakdown"]["overall"] == payload[0]["confidence"]
    assert payload[0]["use_for"]
    assert payload[0]["careful_with"]
    assert payload[0]["explanation_blocks"]


def test_build_period_meanings_surfaces_caution_signals_from_house_eight_eclipse() -> None:
    eclipse = ChangePoint(
        date=date(2026, 5, 12),
        planet="Moon",
        event_type="eclipse",
        summary="Lunar eclipse in Leo, highlighting house 8.",
        sign="Leo",
        house=8,
        motion=None,
        intensity=5,
    )
    periods = [
        PeriodWindow(id="p1", start_date=date(2026, 5, 12), end_date=date(2026, 5, 28), drivers=[eclipse]),
    ]

    payload = build_period_meanings(periods, _natal_chart())[0]
    surfaced_keys = {signal["key"] for signal in payload["surfaced_signals"]}

    assert payload["signals"]["decision_timing"]["status"] == "caution"
    assert "money" in surfaced_keys
    assert "health" in surfaced_keys
    assert payload["domains"]["money_finance"] >= 6


def test_build_period_meanings_suppresses_unbacked_signals() -> None:
    ingress = ChangePoint(
        date=date(2026, 10, 1),
        planet="Jupiter",
        event_type="ingress",
        summary="Jupiter enters Cancer and activates house 9.",
        sign="Cancer",
        house=9,
        motion="direct",
        intensity=3,
    )
    periods = [
        PeriodWindow(id="p2", start_date=date(2026, 10, 1), end_date=date(2026, 10, 28), drivers=[ingress]),
    ]

    payload = build_period_meanings(periods, _natal_chart())[0]
    surfaced_keys = {signal["key"] for signal in payload["surfaced_signals"]}

    assert "politics" not in surfaced_keys
    assert "money" not in surfaced_keys
    assert payload["suppressed_signals"]
