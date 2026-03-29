from __future__ import annotations

import json

import streamlit as st
import streamlit.components.v1 as components

THEME_OPTIONS = ["system", "light", "dark"]


def get_theme_preference() -> str:
    if "yearlens_theme_preference" not in st.session_state:
        query_value = st.query_params.get("theme", "system")
        st.session_state["yearlens_theme_preference"] = _coerce_theme(query_value)
    return _coerce_theme(st.session_state["yearlens_theme_preference"])


def render_theme_toggle() -> str:
    preference = get_theme_preference()
    selected = st.segmented_control(
        "Theme",
        options=THEME_OPTIONS,
        default=preference,
        format_func=lambda option: option.capitalize(),
        key="yearlens_theme_preference",
        width="stretch",
    )
    preference = _coerce_theme(selected)

    if st.query_params.get("theme") != preference:
        st.query_params["theme"] = preference

    return preference


def inject_theme_controller(theme_preference: str) -> None:
    preference = json.dumps(_coerce_theme(theme_preference))
    components.html(
        f"""
        <script>
        const preference = {preference};
        const parentWindow = window.parent;
        const parentDocument = parentWindow.document;
        const root = parentDocument.documentElement;
        const media = parentWindow.matchMedia("(prefers-color-scheme: dark)");

        function applyTheme() {{
            const resolved = preference === "system" ? (media.matches ? "dark" : "light") : preference;
            root.dataset.yearlensThemePreference = preference;
            root.dataset.yearlensTheme = resolved;
            root.style.colorScheme = resolved;
        }}

        if (parentWindow.__yearlensThemeMediaHandler) {{
            media.removeEventListener("change", parentWindow.__yearlensThemeMediaHandler);
        }}

        const handler = () => {{
            if (preference === "system") {{
                applyTheme();
            }}
        }};

        parentWindow.__yearlensThemeMediaHandler = handler;
        media.addEventListener("change", handler);
        applyTheme();
        </script>
        """,
        height=0,
        width=0,
    )


def _coerce_theme(value: str | None) -> str:
    normalized = (value or "system").strip().lower()
    if normalized not in THEME_OPTIONS:
        return "system"
    return normalized
