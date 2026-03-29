from app.core.narrative_engine import attach_narratives, build_year_overview
from app.providers.template_narrative import TemplateNarrativeProvider


def test_template_narrative_provider_adds_structured_copy() -> None:
    period = {
        "id": "p1",
        "tone": "volatile",
        "top_domains": ["money_finance", "health_emotional", "career_work"],
        "use_for": ["reviewing priorities", "moving cautiously with financial planning"],
        "careful_with": ["rushed decisions", "unclear money agreements"],
        "surfaced_signals": [
            {
                "key": "money",
                "level": "high",
                "label": "Money",
                "emoji": "💰",
                "short_text": "Keep money decisions measured",
                "detail_text": "Use extra care with spending or borrowing.",
            }
        ],
        "dominant_drivers": [
            {
                "summary": "A lunar eclipse puts extra weight on shared resource matters in a Leo style.",
            }
        ],
    }

    payload = attach_narratives([period], TemplateNarrativeProvider())[0]

    assert payload["headline"]
    assert payload["concise_text"].startswith("This")
    assert "backstabber" not in payload["detailed_text"].lower()
    assert "rushed decisions" in payload["detailed_text"].lower()


def test_build_year_overview_returns_visual_summary_data() -> None:
    periods = [
        {
            "tone": "stressful",
            "headline": "Use extra care before locking in major choices",
            "start_date": "2026-01-01",
            "end_date": "2026-01-31",
            "confidence": 0.74,
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
            "tone": "supportive",
            "headline": "A steadier window for clearer decisions",
            "start_date": "2026-02-01",
            "end_date": "2026-02-28",
            "confidence": 0.82,
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

    overview = build_year_overview(periods)

    assert overview["tone_summary"][0]["tone"] in {"stressful", "supportive"}
    assert overview["domain_totals"]["career_work"] == 6.5
    assert overview["top_caution_periods"]
    assert overview["summary"].startswith("This year brings more focus to")
