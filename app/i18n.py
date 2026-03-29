"""Internationalization support for YearLens."""

from __future__ import annotations

import streamlit as st

STRINGS: dict[str, dict[str, str | list[str]]] = {
    "en": {
        "hero_eyebrow": "Year Reading Companion",
        "hero_title": "YearLens",
        "hero_tagline": (
            "A calmer way to read the year ahead: clear windows, plain-language themes, "
            "and softer guidance built from your birth details without making the experience "
            "feel like a technical dashboard."
        ),
        "howto_title": "How to use YearLens",
        "howto_section_title": "Getting started",
        "howto_items": [
            "Enter your birth details and the year you want to explore.",
            "Read one period at a time — start in concise mode, switch to detailed when you want the deeper reasoning.",
            "Treat the reading like guidance for reflection and timing, not certainty.",
            "Exact birth time makes the reading more specific, especially around houses.",
            "If location lookup is shaky, manual coordinates give a cleaner fallback.",
        ],
        "placeholder_title": "Generate your reading",
        "placeholder_copy": (
            "Submit the form to build a full YearLens report. If place-name lookup is "
            "unreliable, use the manual latitude, longitude, and timezone fields under advanced options."
        ),
        "error_validation": "Input validation failed. Fix the highlighted values and try again.",
        "error_location_hint": (
            "If the location lookup is the issue, open Advanced settings and provide "
            "manual latitude, longitude, and timezone."
        ),
        "error_report": "Report generation failed: {error}",
        "read_the_year": "Read The Year",
        "mode_concise": "Concise",
        "mode_detailed": "Detailed",
        "form_birth_date": "Birth date",
        "form_year_to_read": "Year to read",
        "form_birth_time": "Birth time",
        "form_hour": "Hour",
        "form_minute": "Minute",
        "form_hour_help": "24-hour format.",
        "form_birth_time_caption": "Use the most exact birth time you know. It helps the reading land more precisely.",
        "form_birth_location": "Birth location",
        "form_reading_cycle": "Reading cycle",
        "form_birthday_cycle": "Birthday cycle",
        "form_calendar_year": "Calendar year",
        "form_cycle_same": "Your birthday is January 1, so birthday cycle and calendar year produce the same {year} window.",
        "form_cycle_explain": (
            "Birthday cycle follows your personal year from birthday to birthday. "
            "Calendar year follows January through December."
        ),
        "form_advanced_title": "Location overrides and advanced options",
        "form_zodiac": "Zodiac",
        "form_ayanamsa": "Ayanamsa",
        "form_house_system": "House system",
        "form_node_type": "Node type",
        "form_lat_override": "Latitude override",
        "form_lon_override": "Longitude override",
        "form_tz_override": "Timezone override",
        "form_display_name": "Display name",
        "form_advanced_caption": (
            "Manual coordinates and timezone let you bypass place-name lookup "
            "for more repeatable results and better privacy."
        ),
        "form_submit": "Generate Reading",
        "overview_eyebrow": "Your Year At A Glance",
        "anchor_birthday": "Birthday cycle",
        "anchor_calendar": "Calendar year",
        "overview_jan1_note": "Birthday and calendar anchors are identical here because the birth date is January 1.",
        "confidence_strong": "Strong signal clarity",
        "confidence_moderate": "Moderate signal clarity",
        "confidence_soft": "Softer signal - read as general direction",
        "themes_weight": "Themes carrying the most weight this year",
        "year_rhythm": "Year rhythm",
        "themes_returning": "Themes That Keep Returning",
        "windows_lean_into": "Windows To Lean Into",
        "windows_pace_carefully": "Windows To Pace Carefully",
        "notes_title": "Notes on interpretation and privacy",
        "notes_items": [
            "Use this as reflective guidance, not certainty or guaranteed prediction.",
            "The report stays in the current session and is not written to a database or report file by default.",
            "Do not use it as the sole basis for medical, legal, financial, or relationship decisions.",
        ],
        "notes_geocoder": "If you entered a place name, that location text was sent to the geocoder to resolve coordinates.",
        "notes_debug_hint": "If you want the technical details, the Debug payload stays available below.",
        "timeline_caption": "Read each period like a weather shift: headline first, then the focus areas and cautions underneath.",
        "pill_now": "Now",
        "main_focus": "Main focus: {domain}",
        "clarity_strong": "Clarity: strong",
        "clarity_moderate": "Clarity: moderate",
        "clarity_general": "Clarity: general direction",
        "story_kicker": "Plain-language read",
        "story_meta": "What this usually feels like: {description}.",
        "signals_title": "What stands out here",
        "lean_into": "Lean into",
        "go_slower": "Go slower with",
        "takeaway_title": "A simple takeaway",
        "focus_areas": "Main Focus Areas",
        "explanation_title": "Why this period was read this way",
        "event_strength": "Event strength {value}",
        "signal_agreement": "Signal agreement {value}",
        "data_quality": "Data quality {value}",
    },
    "zh": {
        "hero_eyebrow": "年度运势解读",
        "hero_title": "YearLens",
        "hero_tagline": "用更平和的方式解读未来一年：清晰的时间窗口、通俗易懂的主题、基于出生信息的温和指引，让体验不像技术仪表盘那样冰冷。",
        "howto_title": "使用指南",
        "howto_section_title": "入门指引",
        "howto_items": [
            "输入您的出生信息和想要查看的年份。",
            "一次阅读一个时期——先从简洁模式开始，想看深入分析时再切换到详细模式。",
            "将解读视为反思和时机的参考指引，而非确定的预言。",
            "精确的出生时间能让解读更具体，尤其是宫位相关的部分。",
            "如果地点查询不稳定，手动输入经纬度会更可靠。",
        ],
        "placeholder_title": "生成您的解读",
        "placeholder_copy": "提交表单以生成完整的 YearLens 报告。如果地名查询不可靠，请使用高级选项中的手动经纬度和时区。",
        "error_validation": "输入验证失败，请修正后重试。",
        "error_location_hint": "如果是地点查询的问题，请打开高级设置并手动输入经度、纬度和时区。",
        "error_report": "报告生成失败：{error}",
        "read_the_year": "逐期解读",
        "mode_concise": "简洁",
        "mode_detailed": "详细",
        "form_birth_date": "出生日期",
        "form_year_to_read": "查看年份",
        "form_birth_time": "出生时间",
        "form_hour": "时",
        "form_minute": "分",
        "form_hour_help": "24小时制。",
        "form_birth_time_caption": "请使用您知道的最精确的出生时间，这有助于让解读更准确。",
        "form_birth_location": "出生地点",
        "form_reading_cycle": "解读周期",
        "form_birthday_cycle": "生日周期",
        "form_calendar_year": "日历年",
        "form_cycle_same": "您的生日是1月1日，生日周期和日历年产生相同的 {year} 窗口。",
        "form_cycle_explain": "生日周期从您的生日开始计算一整年。日历年从一月到十二月。",
        "form_advanced_title": "位置覆盖和高级选项",
        "form_zodiac": "星盘体系",
        "form_ayanamsa": "岁差修正",
        "form_house_system": "宫位系统",
        "form_node_type": "交点类型",
        "form_lat_override": "纬度覆盖",
        "form_lon_override": "经度覆盖",
        "form_tz_override": "时区覆盖",
        "form_display_name": "显示名称",
        "form_advanced_caption": "手动输入经纬度和时区可以绕过地名查询，获得更稳定的结果并保护隐私。",
        "form_submit": "生成解读",
        "overview_eyebrow": "年度总览",
        "anchor_birthday": "生日周期",
        "anchor_calendar": "日历年",
        "overview_jan1_note": "由于出生日期是1月1日，生日周期和日历年完全相同。",
        "confidence_strong": "信号清晰度：强",
        "confidence_moderate": "信号清晰度：中等",
        "confidence_soft": "信号较柔和——请作为大方向参考",
        "themes_weight": "今年最突出的主题",
        "year_rhythm": "年度节奏",
        "themes_returning": "反复出现的主题",
        "windows_lean_into": "适合推进的窗口",
        "windows_pace_carefully": "需要谨慎的窗口",
        "notes_title": "解读说明与隐私",
        "notes_items": [
            "请将此作为反思性指引，而非确定的预测。",
            "报告仅保存在当前会话中，默认不会写入数据库或文件。",
            "请勿将其作为医疗、法律、财务或感情决策的唯一依据。",
        ],
        "notes_geocoder": "如果您输入了地名，该文本已发送至地理编码服务以解析坐标。",
        "notes_debug_hint": "如需技术细节，调试数据在下方可查看。",
        "timeline_caption": "将每个时期想象成天气的变化：先看标题，再看下面的重点领域和注意事项。",
        "pill_now": "当前",
        "main_focus": "主要关注：{domain}",
        "clarity_strong": "清晰度：强",
        "clarity_moderate": "清晰度：中等",
        "clarity_general": "清晰度：大方向",
        "story_kicker": "通俗解读",
        "story_meta": "这段时期通常的感受：{description}。",
        "signals_title": "本期要点",
        "lean_into": "适合投入",
        "go_slower": "需要放慢",
        "takeaway_title": "简要建议",
        "focus_areas": "主要关注领域",
        "explanation_title": "为什么这样解读",
        "event_strength": "事件强度 {value}",
        "signal_agreement": "信号一致性 {value}",
        "data_quality": "数据质量 {value}",
    },
}


def get_lang() -> str:
    try:
        return st.session_state.get("lang", "en")
    except Exception:
        return "en"


def t(key: str, **kwargs: str) -> str | list[str]:
    lang = get_lang()
    value = STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
    if kwargs and isinstance(value, str):
        return value.format(**kwargs)
    return value
