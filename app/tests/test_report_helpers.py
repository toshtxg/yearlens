from app.core.config import DOMAINS
from app.ui.report import _build_domain_trend_frame, _summarize_domain_extremes


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
