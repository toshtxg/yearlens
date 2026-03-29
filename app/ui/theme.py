from __future__ import annotations

import json

import streamlit as st

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
    st.html(
        f"""
        <div style="display:none"></div>
        <script>
        const preference = {preference};
        const root = document.documentElement;
        const media = window.matchMedia("(prefers-color-scheme: dark)");

        function applyTheme() {{
            const resolved = preference === "system" ? (media.matches ? "dark" : "light") : preference;
            root.dataset.yearlensThemePreference = preference;
            root.dataset.yearlensTheme = resolved;
            root.style.colorScheme = resolved;
            if (document.body) {{
                document.body.dataset.yearlensTheme = resolved;
                document.body.style.colorScheme = resolved;
            }}
        }}

        if (window.__yearlensThemeMediaHandler) {{
            media.removeEventListener("change", window.__yearlensThemeMediaHandler);
        }}

        const handler = () => {{
            if (preference === "system") {{
                applyTheme();
            }}
        }};

        window.__yearlensThemeMediaHandler = handler;
        media.addEventListener("change", handler);
        applyTheme();
        </script>
        """,
        width="content",
        unsafe_allow_javascript=True,
    )


def _coerce_theme(value: str | None) -> str:
    normalized = (value or "system").strip().lower()
    if normalized not in THEME_OPTIONS:
        return "system"
    return normalized
