from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from zoneinfo import ZoneInfo

from lunar_python import Solar

from app.core.config import ELEMENT_ORDER, ELEMENT_UI
from app.core.input_schema import UserInput
from app.core.location_service import resolve_location_context

GAN_ELEMENT_MAP = {
    "甲": "wood",
    "乙": "wood",
    "丙": "fire",
    "丁": "fire",
    "戊": "earth",
    "己": "earth",
    "庚": "metal",
    "辛": "metal",
    "壬": "water",
    "癸": "water",
}

ZHI_ELEMENT_MAP = {
    "子": "water",
    "丑": "earth",
    "寅": "wood",
    "卯": "wood",
    "辰": "earth",
    "巳": "fire",
    "午": "fire",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
    "戌": "earth",
    "亥": "water",
}

PILLAR_SPECS = (
    ("year", "Year", "getYearGan", "getYearZhi"),
    ("month", "Month", "getMonthGan", "getMonthZhi"),
    ("day", "Day", "getDayGan", "getDayZhi"),
    ("hour", "Hour", "getTimeGan", "getTimeZhi"),
)


def build_bazi_profile(user_input: UserInput) -> dict:
    location = resolve_location_context(user_input)
    local_birth = datetime.combine(
        user_input.birth_date,
        user_input.birth_time,
        tzinfo=ZoneInfo(location.timezone_id),
    )
    solar = Solar.fromYmdHms(
        local_birth.year,
        local_birth.month,
        local_birth.day,
        local_birth.hour,
        local_birth.minute,
        local_birth.second,
    )
    eight_char = solar.getLunar().getEightChar()

    element_counts = {element: 0 for element in ELEMENT_ORDER}
    pillars = []
    for key, label, gan_method_name, zhi_method_name in PILLAR_SPECS:
        stem = str(getattr(eight_char, gan_method_name)())
        branch = str(getattr(eight_char, zhi_method_name)())
        stem_element = GAN_ELEMENT_MAP[stem]
        branch_element = ZHI_ELEMENT_MAP[branch]
        element_counts[stem_element] += 1
        element_counts[branch_element] += 1
        pillars.append(
            {
                "key": key,
                "label": label,
                "stem": stem,
                "branch": branch,
                "characters": f"{stem}{branch}",
                "stem_element": stem_element,
                "branch_element": branch_element,
            }
        )

    total_slots = len(PILLAR_SPECS) * 2
    element_percentages = {
        element: round((element_counts[element] / total_slots) * 100, 1)
        for element in ELEMENT_ORDER
    }
    weakest_elements = _weakest_elements(element_counts)

    return {
        "basis": {
            "local_birth_datetime": local_birth.isoformat(),
            "timezone_id": location.timezone_id,
            "resolved_location": location.resolved_name,
            "calculation": "standard_bazi_exact_pillars",
        },
        "pillars": pillars,
        "element_counts": element_counts,
        "element_percentages": element_percentages,
        "elements": _element_rows(element_counts, element_percentages),
        "weakest_elements": weakest_elements,
        "recommendations": _build_recommendations(weakest_elements),
    }


def _element_rows(element_counts: dict[str, int], element_percentages: dict[str, float]) -> list[dict]:
    rows = []
    for element in ELEMENT_ORDER:
        ui = ELEMENT_UI[element]
        count = element_counts[element]
        rows.append(
            {
                "key": element,
                "label": ui["label"],
                "hanzi": ui["hanzi"],
                "full_label": ui["full_label"],
                "emoji": ui["emoji"],
                "meaning": ui["meaning"],
                "accent": ui["accent"],
                "count": count,
                "percentage": element_percentages[element],
                "state": _element_state(count),
                "state_label": _element_state_label(count),
            }
        )
    return rows


def _element_state(count: int) -> str:
    if count <= 1:
        return "low"
    if count >= 3:
        return "strong"
    return "present"


def _element_state_label(count: int) -> str:
    if count <= 1:
        return "Low"
    if count >= 3:
        return "Strong"
    return "Present"


def _weakest_elements(element_counts: dict[str, int]) -> list[str]:
    lowest = min(element_counts.values())
    return [element for element in ELEMENT_ORDER if element_counts[element] == lowest]


def _build_recommendations(weakest_elements: Iterable[str]) -> dict:
    elements = list(weakest_elements)
    disclaimer = (
        "This is a simple balance heuristic based on the lighter visible elements in the four pillars. "
        "It is not a full favorable-element prescription."
    )

    if len(elements) >= 3:
        return {
            "mode": "skip",
            "elements": elements,
            "title": "No single balancing cue surfaced",
            "copy": "Three or more elements tie at the low end, so this section stops at the decomposition instead of forcing one remedy.",
            "disclaimer": disclaimer,
            "items": [],
        }

    items = []
    for element in elements:
        ui = ELEMENT_UI[element]
        items.append(
            {
                "key": element,
                "label": ui["label"],
                "hanzi": ui["hanzi"],
                "full_label": ui["full_label"],
                "emoji": ui["emoji"],
                "colors": list(ui["colors"]),
                "examples": list(ui["examples"]),
                "accent": ui["accent"],
            }
        )

    if len(items) == 1:
        return {
            "mode": "single",
            "elements": elements,
            "title": f"Invite a little more {items[0]['full_label']}",
            "copy": "A common balancing approach is to gently bring in a little more of the lightest element through color and everyday surroundings.",
            "disclaimer": disclaimer,
            "items": items,
        }

    return {
        "mode": "pair",
        "elements": elements,
        "title": "Lighter elements",
        "copy": "Two elements tie for the lightest share, so the guidance stays broad rather than forcing one winner.",
        "disclaimer": disclaimer,
        "items": items,
    }
