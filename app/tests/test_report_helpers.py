from datetime import date

from app.core.config import DOMAINS
from app.ui.report import (
    _build_domain_trend_frame,
    _current_age_from_birth_date,
    _current_age_marker_layer,
    _default_long_range_metric_label,
    _default_long_range_scope_label,
    _long_range_score_label,
    _summary_trend_rows,
    _summarize_domain_extremes,
    _trend_report_key,
)


def test_build_domain_trend_frame_creates_one_row_per_period_and_domain() -> None:
    periods = [
        {
            "start_date": "2026-01-01",
            "end_date": "2026-01-31",
            "headline": "Use extra care before locking in major choices",
            "tone": "stressful",
            "domains": {
                "career_work": 8,
                "money_finance": 4,
                "relationships": 3,
                "health_emotional": 7,
                "travel_overseas": 2,
                "study_growth": 5,
            },
        },
        {
            "start_date": "2026-02-01",
            "end_date": "2026-02-28",
            "headline": "A steadier window for clearer decisions",
            "tone": "supportive",
            "domains": {
                "career_work": 5,
                "money_finance": 6,
                "relationships": 4,
                "health_emotional": 4,
                "travel_overseas": 3,
                "study_growth": 7,
            },
        },
    ]

    frame = _build_domain_trend_frame(periods)

    assert len(frame) == len(periods) * len(DOMAINS)
    assert set(frame["domain"]) == set(DOMAINS)
    assert "window" in frame.columns
    assert "score" in frame.columns


def test_summarize_domain_extremes_returns_peak_and_low_windows() -> None:
    periods = [
        {
            "start_date": "2026-01-01",
            "end_date": "2026-01-31",
            "headline": "First stretch",
            "domains": {"career_work": 3},
        },
        {
            "start_date": "2026-02-01",
            "end_date": "2026-02-28",
            "headline": "Second stretch",
            "domains": {"career_work": 8},
        },
    ]

    summary = _summarize_domain_extremes(periods, "career_work")

    assert summary["peak"]["score"] == 8
    assert summary["peak"]["headline"] == "Second stretch"
    assert summary["low"]["score"] == 3
    assert summary["low"]["headline"] == "First stretch"


def test_long_range_trend_defaults_match_expected_ui_choices() -> None:
    assert _default_long_range_scope_label() == "Life to 80"
    assert _default_long_range_metric_label() == "Average"


def test_trend_report_key_changes_with_report_identity() -> None:
    metadata_a = {
        "window_start": "2024-01-01",
        "window_end": "2024-12-31",
        "input_snapshot": {
            "birth_date": "1990-01-01",
            "birth_time": "12:00:00",
            "birth_location": "Singapore",
            "target_year": 2024,
            "year_anchor": "calendar",
        },
    }
    metadata_b = {
        "window_start": "2025-01-01",
        "window_end": "2025-12-31",
        "input_snapshot": {
            "birth_date": "1990-01-01",
            "birth_time": "12:00:00",
            "birth_location": "Singapore",
            "target_year": 2025,
            "year_anchor": "calendar",
        },
    }

    assert _trend_report_key(metadata_a) != _trend_report_key(metadata_b)


def test_long_range_score_label_uses_birth_year_for_age_zero() -> None:
    assert _long_range_score_label({"age": 0, "target_year": 1990}, "lifetime") == "Birth year"
    assert _long_range_score_label({"age": 5, "target_year": 1995}, "lifetime") == "Age 5"


def test_current_age_from_birth_date_handles_birthday_boundary() -> None:
    assert _current_age_from_birth_date("1990-03-29", today=date(2026, 3, 29)) == 36
    assert _current_age_from_birth_date("1990-03-30", today=date(2026, 3, 29)) == 35


def test_summary_trend_rows_uses_current_age_onward_for_lifetime_scope() -> None:
    trend_rows = [
        {"age": 0, "target_year": 1990},
        {"age": 20, "target_year": 2010},
        {"age": 35, "target_year": 2025},
        {"age": 36, "target_year": 2026},
        {"age": 40, "target_year": 2030},
    ]

    filtered = _summary_trend_rows(
        trend_rows,
        "lifetime",
        {"birth_date": "1990-03-29"},
        today=date(2026, 3, 29),
    )

    assert [row["age"] for row in filtered] == [36, 40]


def test_current_age_marker_layer_uses_birth_date() -> None:
    marker_layers = _current_age_marker_layer({"birth_date": "1990-03-29"})

    assert marker_layers is not None
