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
    "health_emotional": "🩺",
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

PLANET_EXPLANATIONS = {
    "Sun": "The Sun tends to bring attention to identity, visibility, confidence, and leadership.",
    "Moon": "The Moon tends to bring out feelings, habits, sensitivity, and what feels personal.",
    "Mars": "Mars tends to increase urgency, friction, courage, and the urge to act fast.",
    "Mercury": "Mercury tends to highlight decisions, communication, paperwork, learning, and logistics.",
    "Jupiter": "Jupiter tends to expand growth, support, perspective, teaching, and opportunity.",
    "Venus": "Venus tends to highlight relationships, ease, attraction, harmony, and values.",
    "Saturn": "Saturn tends to bring pressure, responsibility, patience, delay, and long-term structure.",
    "Rahu": "Rahu tends to intensify ambition, appetite, uncertainty, and unusual or unstable situations.",
    "Ketu": "Ketu tends to reduce attachment, bring distance, and make things feel less clear or less satisfying.",
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

HOUSE_EXPLANATIONS = {
    1: "House 1 points toward the self, health, identity, vitality, and how you carry yourself.",
    2: "House 2 points toward money, savings, speech, family resources, and what feels materially secure.",
    3: "House 3 points toward effort, communication, writing, learning by doing, and everyday courage.",
    4: "House 4 points toward home, family foundations, emotional grounding, and private life.",
    5: "House 5 points toward creativity, romance, self-expression, children, and what brings joy.",
    6: "House 6 points toward work demands, health routines, stress, service, and practical upkeep.",
    7: "House 7 points toward relationships, agreements, clients, and how other people directly affect you.",
    8: "House 8 points toward shared money, debt, trust, vulnerability, endings, and deeper inner change.",
    9: "House 9 points toward travel, beliefs, teachers, long-range perspective, and higher learning.",
    10: "House 10 points toward career, status, reputation, authority, and visible responsibilities.",
    11: "House 11 points toward networks, friends, gains, supporters, and the wider social circle.",
    12: "House 12 points toward rest, retreat, hidden pressures, closure, and what drains or releases energy.",
}

SIGN_EXPLANATIONS = {
    "Aries": "Aries adds speed, courage, impatience, independence, and direct action.",
    "Taurus": "Taurus adds steadiness, material concerns, comfort, stubbornness, and staying power.",
    "Gemini": "Gemini adds conversation, choices, variety, movement, and mental restlessness.",
    "Cancer": "Cancer adds sensitivity, protection, family concerns, memory, and emotional caution.",
    "Leo": "Leo adds visibility, pride, self-expression, confidence, creativity, and wanting to be seen clearly.",
    "Virgo": "Virgo adds analysis, precision, practical cleanup, criticism, and attention to details.",
    "Libra": "Libra adds balance, relationships, compromise, social awareness, and the need to weigh both sides.",
    "Scorpio": "Scorpio adds intensity, privacy, control, trust issues, and deeper emotional undercurrents.",
    "Sagittarius": "Sagittarius adds expansion, travel, learning, truth-telling, and broader perspective.",
    "Capricorn": "Capricorn adds duty, realism, pressure, ambition, and long-term structure.",
    "Aquarius": "Aquarius adds distance, independence, group dynamics, unconventional thinking, and unpredictability.",
    "Pisces": "Pisces adds sensitivity, blurred boundaries, intuition, imagination, and the need for rest.",
}

EVENT_TYPE_EXPLANATIONS = {
    "ingress": "An ingress shifts attention into a new sign and house, so a different part of life starts taking priority.",
    "station": "A station slows a planet down and makes its themes louder, heavier, and harder to ignore for a while.",
    "eclipse": "An eclipse acts like a spotlight or turning point, often making emotions, timing, or outcomes feel more intensified than usual.",
    "fallback": "This period has less concentrated transit pressure, so the reading leans more on the background chart pattern.",
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

PLANET_DOMAIN_BOOSTS = {
    "Sun": ["career_work", "study_growth"],
    "Moon": ["health_emotional", "relationships"],
    "Mars": ["career_work", "health_emotional"],
    "Mercury": ["career_work", "study_growth", "money_finance"],
    "Jupiter": ["study_growth", "travel_overseas", "career_work"],
    "Venus": ["relationships", "money_finance"],
    "Saturn": ["career_work", "health_emotional"],
    "Rahu": ["career_work", "money_finance", "travel_overseas"],
    "Ketu": ["health_emotional", "study_growth"],
}

EVENT_SCORE_MULTIPLIERS = {
    "ingress": 1.0,
    "station": 1.25,
    "eclipse": 1.45,
    "fallback": 0.85,
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
    "stressful": {"label": "High-pressure", "emoji": "🔥", "description": "a stretch that asks for more patience and pacing"},
    "active": {"label": "Busy", "emoji": "🏃", "description": "fast-moving and detail-heavy"},
    "expansive": {"label": "Growth", "emoji": "🌱", "description": "more openings and expansion"},
    "supportive": {"label": "Supportive", "emoji": "🤝", "description": "helpful and cooperative"},
    "serious": {"label": "Demanding", "emoji": "⛰️", "description": "a heavier stretch that rewards focus"},
    "volatile": {"label": "Shifting", "emoji": "🔀", "description": "shifting ground that rewards flexibility"},
    "reflective": {"label": "Reflective", "emoji": "🌙", "description": "a quieter stretch for rest and recalibration"},
}

TONE_COLORS = {
    "constructive": "#4ade80",
    "mixed": "#a78bfa",
    "stressful": "#f87171",
    "active": "#60a5fa",
    "expansive": "#34d399",
    "supportive": "#fbbf24",
    "serious": "#9ca3af",
    "volatile": "#fb923c",
    "reflective": "#c4b5fd",
}

SIGNAL_UI = {
    "decision_timing": {"label": "Decision Timing", "emoji": "🧭"},
    "politics": {"label": "People / Politics", "emoji": "🕵️"},
    "relationships": {"label": "Relationships", "emoji": "❤️"},
    "money": {"label": "Money", "emoji": "💰"},
    "health": {"label": "Health", "emoji": "🩺"},
    "travel": {"label": "Travel / Movement", "emoji": "✈️"},
    "work": {"label": "Work / Pressure", "emoji": "💼"},
}


@dataclass(frozen=True)
class SegmentConfig:
    merge_within_days: int = 4
    min_segment_days: int = 10
    max_segment_days: int = 60
    target_segment_count: int = 10


DEFAULT_SEGMENT_CONFIG = SegmentConfig()
