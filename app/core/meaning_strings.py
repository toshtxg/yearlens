"""Bilingual strings for the meaning engine.

Each dict maps lang → state → (short_text, detail_text) tuple.
"""

DECISION_SIGNAL = {
    "en": {
        "mixed": ("Decision timing is mixed", "If something matters, give it a second pass before locking it in."),
        "caution": ("Use extra care with big decisions", "This window looks more emotionally charged or less clear for irreversible choices, promises, or rushed commitments."),
        "good": ("A steadier window for key decisions", "This window looks cleaner for important choices, agreements, and forward movement than the rougher periods around it."),
    },
    "zh": {
        "mixed": ("决策时机尚不明朗", "如果事关重大，在做最终决定前多斟酌一下。"),
        "caution": ("重大决定需要格外慎重", "这段时期情绪波动可能较大，不太适合做不可逆的选择、承诺或仓促的决定。"),
        "good": ("适合做重要决定的稳定窗口", "相比前后的动荡时期，这段窗口更适合做重要选择、签订协议和向前推进。"),
    },
}

POLITICS_SIGNAL = {
    "en": {
        "low": ("People dynamics look manageable", "People issues do not look like the main pressure point here."),
        "high": ("Watch people and politics more closely", "This window can bring more mixed motives, hidden agendas, social friction, or office politics than usual."),
        "medium": ("Keep boundaries clear with people", "Read the room carefully, avoid oversharing, and make sure expectations are explicit."),
    },
    "zh": {
        "low": ("人际动态较平稳", "人际关系不是这段时期的主要压力来源。"),
        "high": ("注意人际关系和办公室政治", "这段时期可能出现更多动机不明、隐藏议程、社交摩擦或办公室政治。"),
        "medium": ("在人际交往中保持清晰的边界", "仔细观察氛围，避免过度分享，确保期望明确。"),
    },
}

RELATIONSHIP_SIGNAL = {
    "en": {
        "low": ("Relationships look manageable", "Relationships are not the sharpest caution area in this window."),
        "high": ("Handle relationships with extra care", "Trust, closeness, expectations, or emotional reactions may feel more delicate than usual."),
        "medium": ("Use a softer touch in relationships", "This is a good time to clarify tone, expectations, and what each person is actually asking for."),
    },
    "zh": {
        "low": ("感情关系较平稳", "感情关系不是这段时期最需要注意的领域。"),
        "high": ("感情关系需要格外小心", "信任、亲密关系、期望或情绪反应可能比平时更加敏感。"),
        "medium": ("对感情关系轻柔以待", "这是一个适合澄清语气、期望以及彼此真正需求的时期。"),
    },
}

MONEY_SIGNAL = {
    "en": {
        "low": ("Money pressure looks manageable", "Finances are not the sharpest caution area in this window."),
        "high": ("Keep money decisions measured", "Use extra care with spending, borrowing, shared finances, debt, or rushed financial commitments."),
        "medium": ("Double-check financial choices", "Review numbers, payment timing, and the real cost before agreeing to anything."),
    },
    "zh": {
        "low": ("财务压力较小", "财务方面不是这段时期最需要注意的领域。"),
        "high": ("财务决策需要谨慎", "在消费、借贷、共同财务、债务或仓促的财务承诺方面需要格外小心。"),
        "medium": ("仔细核查财务选择", "在签署任何协议之前，核实数字、付款时间和实际成本。"),
    },
}

HEALTH_SIGNAL = {
    "en": {
        "low": ("Health pressure looks manageable", "Health is not the main caution area in this window."),
        "high": ("Mind energy, stress, and health", "Protect sleep, energy, stress levels, and follow through on early warning signs instead of pushing through them."),
        "medium": ("Take better care of your routine", "Routine, pacing, hydration, rest, and nervous-system load matter more than usual here."),
    },
    "zh": {
        "low": ("健康压力较小", "健康不是这段时期的主要关注领域。"),
        "high": ("关注精力、压力和健康", "保护睡眠、精力、压力水平，认真对待早期预警信号，不要硬撑。"),
        "medium": ("更好地照顾日常作息", "日常节奏、休息、补水和神经系统负荷比平时更重要。"),
    },
}

TRAVEL_SIGNAL = {
    "en": {
        "low": ("Travel themes stay in the background", "Travel, movement, or distance are not central here."),
        "high": ("Travel or movement becomes more important", "Movement, distance, paperwork, or a wider horizon may matter more than usual in this period."),
        "caution": ("Plan travel and movement carefully", "Travel or movement may be meaningful here, but build in margin for timing, logistics, and fatigue."),
    },
    "zh": {
        "low": ("旅行主题处于背景", "旅行、出行或远行不是这段时期的重点。"),
        "high": ("旅行或出行变得更重要", "出行、距离、文件手续或更广阔的视野在这段时期可能比平时更重要。"),
        "caution": ("谨慎规划旅行和出行", "旅行或出行在这段时期可能很有意义，但要为时间、后勤和疲劳留出余量。"),
    },
}

WORK_SIGNAL = {
    "en": {
        "low": ("Work pressure looks manageable", "Work is present but not the sharpest pressure point here."),
        "high": ("Expect more work pressure or responsibility", "This period can demand more discipline, accountability, deadlines, or selective prioritization."),
        "medium": ("Work deserves steady attention", "Work matters here, but it responds better to structure and consistency than to rushing."),
    },
    "zh": {
        "low": ("工作压力可控", "工作虽然存在，但不是这段时期最大的压力点。"),
        "high": ("预期更大的工作压力或责任", "这段时期可能要求更多的纪律性、责任心、截止日期或有选择地设定优先级。"),
        "medium": ("工作需要持续关注", "工作在这段时期很重要，但比起急于求成，结构化和持续性会更有效。"),
    },
}

USE_FOR = {
    "en": {
        "good_decisions": "making clearer decisions and moving important plans forward",
        "career_work": "steady work progress and visible responsibilities",
        "money_finance": "measured financial planning and sorting practical priorities",
        "relationships": "honest conversations and strengthening key ties",
        "health_emotional": "resetting routines and listening to what your body or mood is telling you",
        "travel_overseas": "travel planning, learning, and looking at the bigger picture",
        "study_growth": "study, strategy, personal growth, and long-range planning",
        "support_fallback": "using the steadier tone of this period to move one or two priorities forward",
        "caution_fallback": "slower review, cleanup, and making fewer but better-timed moves",
    },
    "zh": {
        "good_decisions": "做出更清晰的决定并推进重要计划",
        "career_work": "稳步推进工作和可见的职责",
        "money_finance": "有计划的财务规划和处理实际优先事项",
        "relationships": "真诚的对话和加强重要关系",
        "health_emotional": "重置日常节奏，倾听身体和情绪的信号",
        "travel_overseas": "旅行规划、学习和放眼更大的格局",
        "study_growth": "学习、规划、个人成长和长远打算",
        "support_fallback": "利用这段较稳定的基调推进一两个优先事项",
        "caution_fallback": "放慢节奏，复盘整理，做更少但时机更好的动作",
    },
}

CAREFUL_WITH = {
    "en": {
        "decision_timing": "rushed decisions, big promises, and irreversible commitments",
        "politics": "oversharing, office politics, or trusting unclear motives too quickly",
        "relationships": "sensitive conversations, assumptions, and emotional overreactions",
        "money": "risky spending, debt, or vague money agreements",
        "health": "pushing through fatigue, stress, or ignored warning signs",
        "travel": "tight travel timing, paperwork, or overpacked schedules",
        "work": "taking on too much responsibility without enough margin",
        "caution_fallback": "overloading your schedule or reacting too quickly",
        "money_fallback": "treating financial choices as small when they deserve a closer look",
    },
    "zh": {
        "decision_timing": "仓促的决定、重大承诺和不可逆的选择",
        "politics": "过度分享、办公室政治或过快信任动机不明的人",
        "relationships": "敏感的对话、臆断和情绪过度反应",
        "money": "冒险消费、债务或模糊的财务协议",
        "health": "硬撑疲劳、压力或忽视的预警信号",
        "travel": "紧凑的旅行安排、文件手续或过满的日程",
        "work": "承担过多责任而没有留够余量",
        "caution_fallback": "日程过满或反应过于迅速",
        "money_fallback": "把需要仔细审视的财务选择当作小事",
    },
}

ADVICE_EXTRA = {
    "en": {
        "delay_decisions": "Delay major decisions if the choice can wait.",
        "tight_plans": "Keep plans tighter and confirm who really needs to know what.",
        "money_write": "Write numbers down and avoid vague financial promises.",
        "protect_sleep": "Protect sleep, routine, and recovery before performance slips.",
        "say_awkward": "Say the awkward thing clearly instead of letting assumptions grow.",
        "choose_few": "Choose the few responsibilities that actually move work forward.",
    },
    "zh": {
        "delay_decisions": "如果可以等，就推迟重大决定。",
        "tight_plans": "收紧计划，确认谁真正需要知道什么。",
        "money_write": "把数字写下来，避免模糊的财务承诺。",
        "protect_sleep": "在表现下滑之前，先保护好睡眠、作息和恢复。",
        "say_awkward": "把尴尬的话说清楚，而不是让假设滋长。",
        "choose_few": "选择真正能推动工作的少数责任。",
    },
}

DRIVER_SUMMARY = {
    "en": {
        "eclipse": "{eclipse_name} themes put extra weight on {house_meaning} matters in {sign} style.",
        "retrograde": "{planet} retrograde slows things down and makes house {house} themes harder to ignore.",
        "station": "{planet} stations and makes house {house} themes louder for a while.",
        "ingress": "{planet} shifts into {sign}, so house {house} topics start taking more of your attention.",
        "fallback": "No single transit dominates this stretch, so the reading leans on the background pattern.",
    },
    "zh": {
        "eclipse": "{eclipse_name}主题为{sign}风格的{house_meaning}事务增添了额外重量。",
        "retrograde": "{planet}逆行减缓了节奏，使第{house}宫的主题更难忽视。",
        "station": "{planet}停滞，使第{house}宫的主题暂时更加突出。",
        "ingress": "{planet}进入{sign}，因此第{house}宫的话题开始占据更多注意力。",
        "fallback": "没有单一行星运行主导这段时期，解读依赖于背景星盘模式。",
    },
}

EVENT_TEXT = {
    "en": {
        "retrograde": "A retrograde station slows a planet down and often makes review, delay, and repetition more obvious.",
        "direct": "A direct station tends to unstick a theme that was stalled, slow, or under review.",
    },
    "zh": {
        "retrograde": "逆行停滞减缓了行星速度，往往使回顾、延迟和重复变得更加明显。",
        "direct": "顺行停滞倾向于让之前停滞、缓慢或处于审视中的主题重新启动。",
    },
}

COMBINED_EFFECT = {
    "en": {
        "eclipse": "{planet} themes feel louder and more exposed here. {sign_clause} {house_clause}",
        "retrograde": "{planet} themes slow down for review here. {sign_clause} {house_clause}",
        "station": "{planet} themes become more noticeable here. {sign_clause} {house_clause}",
        "ingress": "{planet} starts working through a new area here. {sign_clause} {house_clause}",
        "fallback": "This is a quieter stretch. {sign_clause} {house_clause}",
    },
    "zh": {
        "eclipse": "{planet}的主题在这里更加响亮和外显。{sign_clause} {house_clause}",
        "retrograde": "{planet}的主题在这里放慢节奏以供审视。{sign_clause} {house_clause}",
        "station": "{planet}的主题在这里变得更加显著。{sign_clause} {house_clause}",
        "ingress": "{planet}开始在一个新的领域运作。{sign_clause} {house_clause}",
        "fallback": "这是一段较为平静的时期。{sign_clause} {house_clause}",
    },
}

ECLIPSE_NAMES = {
    "en": {"solar": "Solar eclipse", "lunar": "Lunar eclipse"},
    "zh": {"solar": "日食", "lunar": "月食"},
}

EVENT_LABELS = {
    "en": {"eclipse": "", "station": "station", "ingress": "sign change", "fallback": "background pattern"},
    "zh": {"eclipse": "", "station": "停滞", "ingress": "换座", "fallback": "背景模式"},
}

DRIVER_TITLE = {
    "en": {
        "fallback": "{planet} background pattern",
        "eclipse": "{event_label} in {sign} / House {house}",
        "other": "{planet} {event_label} in {sign} / House {house}",
    },
    "zh": {
        "fallback": "{planet} 背景模式",
        "eclipse": "{event_label}在{sign} / 第{house}宫",
        "other": "{planet} {event_label}在{sign} / 第{house}宫",
    },
}

FALLBACK_SIGN_TEXT = {
    "en": "The sign adds its own style to how this period expresses itself.",
    "zh": "星座为这段时期增添了独特的表达风格。",
}

FALLBACK_SUMMARY = {
    "en": "No single transit dominates this stretch, so the reading leans on the quieter background pattern.",
    "zh": "没有单一行星运行主导这段时期，因此解读依赖于较为安静的背景模式。",
}

YEAR_OVERVIEW = {
    "en": {
        "steady": "A year with some steadier windows for progress, as long as you use the sharper periods more carefully.",
        "demanding": "A more demanding year that rewards pacing, clearer boundaries, and better timing.",
        "mixed": "A mixed year with alternating stretches of pressure, reset, and usable momentum.",
        "theme_template": "{emoji} {domain} comes up repeatedly across the year.",
        "no_caution": "No strong caution windows were surfaced from the current ruleset.",
        "no_opportunity": "No unusually supportive windows were surfaced from the current ruleset.",
    },
    "zh": {
        "steady": "这一年有一些较为稳定的窗口适合推进，只要在较激烈的时期更加谨慎。",
        "demanding": "这是较为考验的一年，需要把握节奏、明确边界和更好的时机选择。",
        "mixed": "这是交替出现压力、调整和可用势头的混合之年。",
        "theme_template": "{emoji} {domain}在全年反复出现。",
        "no_caution": "当前规则未显示出明显的高压窗口。",
        "no_opportunity": "当前规则未显示出特别顺利的窗口。",
    },
}
