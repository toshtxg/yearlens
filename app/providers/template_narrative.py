from app.core.config import get_domain_labels, get_tone_ui

_HEADLINE_VARIANTS = {
    "en": {
        "decision_timing": [
            "Use extra care before locking in major choices",
            "Pause before signing, committing, or promising",
            "Give big decisions more room to breathe",
            "Let important choices sit a little longer",
            "Timing is noisier here — avoid rushing anything permanent",
        ],
        "politics": [
            "Read people and politics more carefully",
            "Watch for mixed signals in group dynamics",
            "Navigate social currents with more caution",
        ],
        "relationships": [
            "Handle relationship dynamics more gently",
            "Be patient with emotional undercurrents",
            "Give close relationships a lighter touch",
        ],
        "money": [
            "Keep money decisions measured",
            "Take extra care around financial commitments",
            "Avoid impulsive spending or lending",
        ],
        "health": [
            "Slow down enough to protect energy and health",
            "Your body is asking for more margin here",
            "Watch for burnout — pace yourself deliberately",
        ],
        "travel": [
            "Movement and timing matter more here",
            "Travel or relocation plans need extra planning",
            "Give logistics and travel more buffer time",
        ],
        "work": [
            "Work pressure needs cleaner prioritization",
            "Focus on fewer things and do them well",
            "Career demands are louder — choose battles carefully",
        ],
    },
    "zh": {
        "decision_timing": [
            "重大选择前请格外慎重",
            "签署、承诺或许诺之前先暂停",
            "给重要决定多一些呼吸空间",
            "让重要选择多沉淀一会儿",
            "时机较混乱——避免急于做永久性决定",
        ],
        "politics": [
            "更仔细地观察人际和政治动态",
            "留意群体中的混合信号",
            "更谨慎地处理社交关系",
        ],
        "relationships": [
            "更温柔地处理感情关系",
            "对情感暗流保持耐心",
            "给亲密关系一个更轻柔的触碰",
        ],
        "money": [
            "财务决策要有分寸",
            "财务承诺需要格外小心",
            "避免冲动消费或借贷",
        ],
        "health": [
            "放慢脚步以保护精力和健康",
            "你的身体在这段时期需要更多余量",
            "警惕倦怠——有意识地调整节奏",
        ],
        "travel": [
            "出行和时机在这段时期更加重要",
            "旅行或搬迁计划需要更多准备",
            "为出行和后勤留出更多缓冲时间",
        ],
        "work": [
            "工作压力需要更清晰的优先级",
            "专注于更少的事情并做好它们",
            "职场要求更高——谨慎选择战场",
        ],
    },
}

_GOOD_TIMING_VARIANTS = {
    "en": [
        "A steadier window for clearer decisions",
        "Momentum is with you — act with intention",
        "This stretch favors forward movement",
    ],
    "zh": [
        "适合做清晰决定的稳定窗口",
        "势头在你这边——有意识地行动",
        "这段时期有利于向前推进",
    ],
}


def _pick_variant(variants: list[str], period_id: str, signal_key: str) -> str:
    index = hash((period_id, signal_key)) % len(variants)
    return variants[index]


class TemplateNarrativeProvider:
    def generate(self, period_data: dict, lang: str = "en") -> dict:
        domain_labels = get_domain_labels(lang)
        tone_ui = get_tone_ui(lang)

        primary_domain = domain_labels[period_data["top_domains"][0]].lower()
        tone_label = tone_ui[period_data["tone"]]["label"].lower()
        primary_signal = period_data["surfaced_signals"][0] if period_data["surfaced_signals"] else None
        lead_driver = period_data["dominant_drivers"][0]
        period_id = period_data.get("id", "p0")

        return {
            "headline": _build_headline(primary_signal, primary_domain, tone_label, period_id, lang),
            "concise_text": _build_concise_text(period_data, primary_domain, tone_label, lang),
            "detailed_text": _build_detailed_text(period_data, lead_driver, primary_domain, tone_label, lang),
        }


def _build_headline(primary_signal: dict | None, primary_domain: str, tone_label: str, period_id: str, lang: str) -> str:
    headlines = _HEADLINE_VARIANTS[lang]
    good_variants = _GOOD_TIMING_VARIANTS[lang]

    if primary_signal is None:
        if lang == "zh":
            return f"{tone_label}聚焦于{primary_domain}"
        return f"{tone_label.capitalize()} focus on {primary_domain}"

    signal_key = primary_signal["key"]

    if signal_key == "decision_timing" and primary_signal["status"] == "good":
        return _pick_variant(good_variants, period_id, "decision_timing_good")

    if signal_key in headlines:
        return _pick_variant(headlines[signal_key], period_id, signal_key)

    if lang == "zh":
        return f"{tone_label}聚焦于{primary_domain}"
    return f"{tone_label.capitalize()} focus on {primary_domain}"


def _build_concise_text(period_data: dict, primary_domain: str, tone_label: str, lang: str) -> str:
    use_for = period_data["use_for"][0]
    careful_with = period_data["careful_with"][0] if period_data["careful_with"] else None

    if lang == "zh":
        summary = f"这段{tone_label}时期更侧重于{primary_domain}方面。适合用于{use_for}"
        if careful_with:
            summary += f"，同时在{careful_with}方面需要格外注意"
        return f"{summary}。"

    summary = f"This {tone_label} window puts more emphasis on {primary_domain}. It is better used for {use_for}"
    if careful_with:
        summary += f", while using extra care around {careful_with}"
    return f"{summary}."


def _build_detailed_text(period_data: dict, lead_driver: dict, primary_domain: str, tone_label: str, lang: str) -> str:
    if lang == "zh":
        use_for = "；".join(period_data["use_for"][:2])
        careful_with = "；".join(period_data["careful_with"][:2]) or "没有留够余量就过于用力"
        return (
            f"这段{tone_label}时期最明显地倾向于{primary_domain}方面。"
            f"主要驱动因素是：{lead_driver['summary']}"
            f"因此这段窗口更适合{use_for}，同时需要在{careful_with}方面更加谨慎。"
        )

    use_for = "; ".join(period_data["use_for"][:2])
    careful_with = "; ".join(period_data["careful_with"][:2]) or "pushing too hard without enough margin"
    return (
        f"This {tone_label} stretch leans most strongly toward {primary_domain}. "
        f"The main driver is this: {lead_driver['summary']} "
        f"That makes this window better for {use_for}, while asking for more care around {careful_with}."
    )
