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

# ---------------------------------------------------------------------------
# Chinese translations
# ---------------------------------------------------------------------------

DOMAIN_LABELS_ZH = {
    "career_work": "事业/工作",
    "money_finance": "财务/金融",
    "relationships": "感情关系",
    "health_emotional": "健康/情绪",
    "travel_overseas": "旅行/海外",
    "study_growth": "学习/成长",
}

TONE_UI_ZH = {
    "constructive": {"label": "高效期", "emoji": "✅", "description": "稳步前进"},
    "mixed": {"label": "混合期", "emoji": "⚖️", "description": "有进展也有摩擦"},
    "stressful": {"label": "高压期", "emoji": "🔥", "description": "需要更多耐心和节奏调整"},
    "active": {"label": "忙碌期", "emoji": "🏃", "description": "节奏快、细节多"},
    "expansive": {"label": "成长期", "emoji": "🌱", "description": "更多开放和扩展的机会"},
    "supportive": {"label": "顺利期", "emoji": "🤝", "description": "有助力、易合作"},
    "serious": {"label": "考验期", "emoji": "⛰️", "description": "较沉重但回报专注"},
    "volatile": {"label": "变动期", "emoji": "🔀", "description": "变化多端但回报灵活性"},
    "reflective": {"label": "沉淀期", "emoji": "🌙", "description": "适合休息和重新校准"},
}

SIGNAL_UI_ZH = {
    "decision_timing": {"label": "决策时机", "emoji": "🧭"},
    "politics": {"label": "人际/政治", "emoji": "🕵️"},
    "relationships": {"label": "感情关系", "emoji": "❤️"},
    "money": {"label": "财务", "emoji": "💰"},
    "health": {"label": "健康", "emoji": "🩺"},
    "travel": {"label": "旅行/出行", "emoji": "✈️"},
    "work": {"label": "工作/压力", "emoji": "💼"},
}

PLANET_MEANINGS_ZH = {
    "Sun": ["身份", "可见度", "权威"],
    "Moon": ["情绪", "习惯", "敏感"],
    "Mars": ["驱动力", "冲突", "紧迫感"],
    "Mercury": ["沟通", "商贸", "学习"],
    "Jupiter": ["成长", "智慧", "支持"],
    "Venus": ["关系", "享受", "价值"],
    "Saturn": ["纪律", "延迟", "压力"],
    "Rahu": ["野心", "不稳定", "执念"],
    "Ketu": ["放下", "超脱", "不确定"],
}

PLANET_EXPLANATIONS_ZH = {
    "Sun": "太阳倾向于将注意力带到身份、可见度、自信和领导力方面。",
    "Moon": "月亮倾向于唤起感受、习惯、敏感以及个人化的事务。",
    "Mars": "火星倾向于增加紧迫感、摩擦、勇气和快速行动的冲动。",
    "Mercury": "水星倾向于突出决策、沟通、文件、学习和后勤方面。",
    "Jupiter": "木星倾向于扩展成长、支持、视野、教学和机会。",
    "Venus": "金星倾向于突出关系、轻松、吸引力、和谐和价值观。",
    "Saturn": "土星倾向于带来压力、责任、耐心、延迟和长期结构。",
    "Rahu": "罗睺倾向于加剧野心、欲望、不确定性以及不寻常或不稳定的情况。",
    "Ketu": "计都倾向于减少执着，带来距离感，让事情感觉不太清晰或不太令人满意。",
}

HOUSE_MEANINGS_ZH = {
    1: ["自我", "活力", "身份"],
    2: ["金钱", "言语", "家庭资源"],
    3: ["努力", "沟通", "技能"],
    4: ["家庭", "根基", "内心"],
    5: ["创造力", "表达", "浪漫"],
    6: ["工作", "压力", "纪律"],
    7: ["伴侣关系", "协议", "映射"],
    8: ["共享资源", "变化", "深度"],
    9: ["旅行", "信念", "高等教育"],
    10: ["事业", "地位", "责任"],
    11: ["人脉", "收获", "社交圈"],
    12: ["退隐", "休息", "隐藏过程"],
}

HOUSE_EXPLANATIONS_ZH = {
    1: "第一宫指向自我、健康、身份、活力以及外在呈现方式。",
    2: "第二宫指向金钱、储蓄、言语、家庭资源以及物质安全感。",
    3: "第三宫指向努力、沟通、写作、实践学习和日常勇气。",
    4: "第四宫指向家庭、家庭根基、情感基础和私人生活。",
    5: "第五宫指向创造力、浪漫、自我表达、子女以及带来快乐的事物。",
    6: "第六宫指向工作需求、健康习惯、压力、服务和日常维护。",
    7: "第七宫指向关系、协议、客户以及他人如何直接影响你。",
    8: "第八宫指向共同财务、债务、信任、脆弱、结束和更深层的内在变化。",
    9: "第九宫指向旅行、信念、导师、长远视野和高等教育。",
    10: "第十宫指向事业、地位、声誉、权威和可见的责任。",
    11: "第十一宫指向人脉、朋友、收获、支持者和更广泛的社交圈。",
    12: "第十二宫指向休息、退隐、隐藏的压力、结束以及消耗或释放能量的事物。",
}

SIGN_EXPLANATIONS_ZH = {
    "Aries": "白羊座增添速度、勇气、急躁、独立和直接行动。",
    "Taurus": "金牛座增添稳定、物质关注、舒适、固执和持久力。",
    "Gemini": "双子座增添对话、选择、多样性、活动和精神上的不安。",
    "Cancer": "巨蟹座增添敏感、保护、家庭关注、记忆和情感上的谨慎。",
    "Leo": "狮子座增添可见度、自豪、自我表达、自信、创造力和被清晰看到的渴望。",
    "Virgo": "处女座增添分析、精确、实际清理、批评和对细节的关注。",
    "Libra": "天秤座增添平衡、关系、妥协、社交意识和权衡两面的需要。",
    "Scorpio": "天蝎座增添强度、隐私、控制、信任问题和更深层的情感暗流。",
    "Sagittarius": "射手座增添扩展、旅行、学习、真言直说和更广阔的视野。",
    "Capricorn": "摩羯座增添责任、现实主义、压力、野心和长期结构。",
    "Aquarius": "水瓶座增添距离、独立、群体动态、非传统思维和不可预测性。",
    "Pisces": "双鱼座增添敏感、模糊的边界、直觉、想象力和休息的需要。",
}

EVENT_TYPE_EXPLANATIONS_ZH = {
    "ingress": "入座将注意力转移到新的星座和宫位，生活的不同部分开始成为重点。",
    "station": "停滞减缓了行星速度，使其主题在一段时间内更加响亮、沉重、难以忽视。",
    "eclipse": "食相像聚光灯或转折点，常常使情绪、时机或结果比平时更加强烈。",
    "fallback": "这段时期行星运行压力较小，解读更多依赖于背景星盘模式。",
}

ADVICE_BY_TONE_ZH = {
    "constructive": ["在优先事项上采取可见的行动。", "有目的地利用势头。"],
    "mixed": ["情绪波动时先不要做决定。", "给自己留出消化的时间。"],
    "stressful": ["保持低调。", "避免不必要的冲突。"],
    "active": ["沟通要清晰，最好书面确认。", "仔细核查细节。"],
    "expansive": ["有纪律地投资成长。", "对战略性机会说是。"],
    "supportive": ["善用合作。", "稳固已经运转良好的事务。"],
    "serious": ["有条不紊地工作。", "耐心优于蛮力。"],
    "volatile": ["避免过度承诺。", "在大动作之前审视动机。"],
    "reflective": ["尽可能简化。", "为休息和重置留出空间。"],
}


def get_domain_labels(lang: str = "en") -> dict[str, str]:
    return DOMAIN_LABELS_ZH if lang == "zh" else DOMAIN_LABELS


def get_tone_ui(lang: str = "en") -> dict:
    return TONE_UI_ZH if lang == "zh" else TONE_UI


def get_signal_ui(lang: str = "en") -> dict:
    return SIGNAL_UI_ZH if lang == "zh" else SIGNAL_UI


def get_planet_meanings(lang: str = "en") -> dict:
    return PLANET_MEANINGS_ZH if lang == "zh" else PLANET_MEANINGS


def get_planet_explanations(lang: str = "en") -> dict:
    return PLANET_EXPLANATIONS_ZH if lang == "zh" else PLANET_EXPLANATIONS


def get_house_meanings(lang: str = "en") -> dict:
    return HOUSE_MEANINGS_ZH if lang == "zh" else HOUSE_MEANINGS


def get_house_explanations(lang: str = "en") -> dict:
    return HOUSE_EXPLANATIONS_ZH if lang == "zh" else HOUSE_EXPLANATIONS


def get_sign_explanations(lang: str = "en") -> dict:
    return SIGN_EXPLANATIONS_ZH if lang == "zh" else SIGN_EXPLANATIONS


def get_event_type_explanations(lang: str = "en") -> dict:
    return EVENT_TYPE_EXPLANATIONS_ZH if lang == "zh" else EVENT_TYPE_EXPLANATIONS


def get_advice_by_tone(lang: str = "en") -> dict:
    return ADVICE_BY_TONE_ZH if lang == "zh" else ADVICE_BY_TONE
