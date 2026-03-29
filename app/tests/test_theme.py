from app.ui.theme import _coerce_theme


def test_coerce_theme_falls_back_to_system() -> None:
    assert _coerce_theme(None) == "system"
    assert _coerce_theme("LIGHT") == "light"
    assert _coerce_theme("dark") == "dark"
    assert _coerce_theme("sepia") == "system"
