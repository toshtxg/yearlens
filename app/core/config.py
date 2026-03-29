from dataclasses import dataclass

APP_TITLE = "YearLens"

DOMAIN_LABELS = {
    "career_work": "Career / Work",
    "money_finance": "Money / Finance",
    "relationships": "Relationships",
    "health_emotional": "Health / Emotional",
    "travel_overseas": "Travel / Overseas",
    "study_growth": "Study / Growth",
}

DOMAINS = list(DOMAIN_LABELS)

DOMAIN_EMOJIS = {
    "career_work": "💼",
    "money_finance": "💰",
    "relationships": "❤️",
    "health_emotional": "🧠",
    "travel_overseas": "✈️",
    "study_growth": "📚",
}

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

PLANET_SEQUENCE = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
]

PLANET_MEANINGS = {
    "Sun": ["identity", "visibility", "authority"],
    "Moon": ["emotions", "habits", "sensitivity"],
    "Mars": ["drive", "conflict", "urgency"],
    "Mercury": ["communication", "trade", "learning"],
    "Jupiter": ["growth", "wisdom", "support"],
    "Venus": ["relationships", "pleasure", "value"],
    "Saturn": ["discipline", "delay", "pressure"],
    "Rahu": ["ambition", "instability", "obsession"],
    "Ketu": ["release", "detachment", "uncertainty"],
}

HOUSE_MEANINGS = {
    1: ["self", "vitality", "identity"],
    2: ["money", "speech", "family resources"],
    3: ["effort", "communication", "skills"],
    4: ["home", "foundations", "inner life"],
    5: ["creativity", "expression", "romance"],
    6: ["work", "stress", "discipline"],
    7: ["partnerships", "agreements", "mirroring"],
    8: ["shared resources", "change", "depth"],
    9: ["travel", "beliefs", "higher learning"],
    10: ["career", "status", "responsibility"],
    11: ["networks", "gains", "social circles"],
    12: ["retreat", "rest", "hidden processes"],
}

HOUSE_DOMAIN_MAP = {
    1: ["health_emotional", "study_growth"],
    2: ["money_finance"],
    3: ["study_growth"],
    4: ["health_emotional"],
    5: ["relationships", "study_growth"],
    6: ["career_work", "health_emotional"],
    7: ["relationships"],
    8: ["money_finance", "health_emotional"],
    9: ["travel_overseas", "study_growth"],
    10: ["career_work"],
    11: ["career_work", "money_finance", "relationships"],
    12: ["travel_overseas", "health_emotional"],
}

TONE_BY_PLANET = {
    "Sun": "constructive",
    "Moon": "mixed",
    "Mars": "stressful",
    "Mercury": "active",
    "Jupiter": "expansive",
    "Venus": "supportive",
    "Saturn": "serious",
    "Rahu": "volatile",
    "Ketu": "reflective",
}

ADVICE_BY_TONE = {
    "constructive": ["Take visible action on priorities.", "Use momentum deliberately."],
    "mixed": ["Watch changing moods before making decisions.", "Give yourself processing time."],
    "stressful": ["Keep a low profile.", "Avoid unnecessary conflict."],
    "active": ["Communicate clearly and in writing.", "Double-check details."],
    "expansive": ["Invest in growth with discipline.", "Say yes to strategic openings."],
    "supportive": ["Lean into collaboration.", "Stabilize what is already working."],
    "serious": ["Work methodically.", "Prefer patience over force."],
    "volatile": ["Avoid overcommitting.", "Review motives before taking big swings."],
    "reflective": ["Simplify where possible.", "Leave room for rest and reset."],
}

TONE_UI = {
    "constructive": {"label": "Productive", "emoji": "✅", "description": "steady forward movement"},
    "mixed": {"label": "Mixed", "emoji": "⚖️", "description": "some wins, some friction"},
    "stressful": {"label": "Stress", "emoji": "⚠️", "description": "higher pressure than usual"},
    "active": {"label": "Busy", "emoji": "🏃", "description": "fast-moving and detail-heavy"},
    "expansive": {"label": "Growth", "emoji": "🌱", "description": "more openings and expansion"},
    "supportive": {"label": "Supportive", "emoji": "🤝", "description": "helpful and cooperative"},
    "serious": {"label": "Heavy", "emoji": "🪨", "description": "responsibility and discipline"},
    "volatile": {"label": "Unstable", "emoji": "🌪️", "description": "sudden shifts or unpredictability"},
    "reflective": {"label": "Slow Down", "emoji": "🛋️", "description": "review, rest, and reset"},
}

SIGNAL_UI = {
    "decision_timing": {"label": "Decision Timing", "emoji": "🧭"},
    "backstabbers": {"label": "Politics / Backstabbers", "emoji": "🕵️"},
    "relationships": {"label": "Relationships", "emoji": "❤️"},
    "money": {"label": "Money", "emoji": "💰"},
    "health": {"label": "Health", "emoji": "🩺"},
}


@dataclass(frozen=True)
class SegmentConfig:
    merge_within_days: int = 4
    min_segment_days: int = 10
    max_segment_days: int = 60
    target_segment_count: int = 10


DEFAULT_SEGMENT_CONFIG = SegmentConfig()
