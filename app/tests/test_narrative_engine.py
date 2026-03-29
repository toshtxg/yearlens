from app.core.narrative_engine import attach_narratives
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
