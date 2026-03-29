import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --yl-bg: #111827;
            --yl-surface: rgba(24, 33, 49, 0.92);
            --yl-surface-strong: #1f2937;
            --yl-surface-soft: #162033;
            --yl-border: rgba(148, 163, 184, 0.28);
            --yl-border-soft: rgba(148, 163, 184, 0.18);
            --yl-text: #edf2f7;
            --yl-text-soft: #cbd5e1;
            --yl-text-muted: #94a3b8;
            --yl-pill-bg: #243247;
            --yl-pill-text: #e5edf8;
            --yl-input-bg: #162033;
            --yl-input-text: #edf2f7;
            --yl-input-border: rgba(148, 163, 184, 0.26);
            --yl-subtle-bg: rgba(20, 28, 42, 0.84);
        }

        html, body, [data-testid="stAppViewContainer"], .stApp, [data-testid="stHeader"] {
            background: var(--yl-bg) !important;
            color: var(--yl-text) !important;
        }

        [data-testid="stToolbar"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 760px;
            padding-top: 0.75rem;
            padding-bottom: 1.6rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .yearlens-hero {
            margin-bottom: 0.8rem;
        }

        .yearlens-hero h1 {
            font-size: clamp(2.4rem, 4vw, 3.4rem);
            line-height: 0.95;
            letter-spacing: -0.04em;
            margin: 0 0 0.55rem 0;
            color: var(--yl-text);
        }

        .yearlens-hero p {
            margin: 0;
            font-size: 1rem;
            line-height: 1.55;
            color: var(--yl-text-soft);
            max-width: 44rem;
        }

        div[data-testid="stForm"] {
            padding: 0.8rem 0.9rem 0.9rem 0.9rem;
            border: 1px solid var(--yl-border);
            border-radius: 16px;
            background: var(--yl-surface);
        }

        div[data-testid="stForm"] label,
        div[data-testid="stExpander"] label,
        div[data-testid="stRadio"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stTextInput"] label {
            font-size: 0.96rem;
            color: var(--yl-text) !important;
        }

        div[data-testid="stCaptionContainer"],
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stText"] {
            color: var(--yl-text) !important;
        }

        div[data-testid="stCaptionContainer"] {
            margin-top: -0.15rem;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-testid="stDateInput"] > div,
        div[data-testid="stNumberInput"] > div,
        div[data-testid="stTextInputRootElement"] > div {
            min-height: 2.85rem;
            background: var(--yl-input-bg) !important;
            border-color: var(--yl-input-border) !important;
            color: var(--yl-input-text) !important;
        }

        div[data-baseweb="input"] input,
        div[data-baseweb="select"] *,
        div[data-testid="stDateInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextInputRootElement"] input {
            font-size: 0.98rem;
            color: var(--yl-input-text) !important;
            background: transparent !important;
            caret-color: var(--yl-input-text) !important;
        }

        div[data-baseweb="input"] input::placeholder,
        div[data-testid="stTextInputRootElement"] input::placeholder {
            color: var(--yl-text-muted) !important;
        }

        div[data-testid="stNumberInput"] button {
            min-width: 2rem;
            min-height: 2rem;
            color: var(--yl-text) !important;
        }

        div[data-testid="stFormSubmitButton"] button,
        div[data-testid="stButton"] button {
            min-height: 2.9rem;
            font-size: 1rem;
            background: var(--yl-surface-strong) !important;
            color: var(--yl-text) !important;
            border: 1px solid var(--yl-border) !important;
        }

        div[data-testid="stRadio"] div[role="radiogroup"] label {
            color: var(--yl-text) !important;
        }

        details, summary, div[data-testid="stExpander"] {
            background: transparent !important;
            color: var(--yl-text) !important;
        }

        .yearlens-card {
            border: 1px solid var(--yl-border);
            border-radius: 16px;
            background: var(--yl-surface);
            padding: 0.8rem 0.9rem;
            margin-bottom: 0.7rem;
        }

        .yearlens-kicker {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--yl-text-muted);
            margin-bottom: 0.25rem;
        }

        .yearlens-value {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--yl-text);
            line-height: 1.35;
        }

        .yearlens-pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin: 0.2rem 0 0.45rem 0;
        }

        .yearlens-pill {
            display: inline-block;
            border-radius: 999px;
            padding: 0.32rem 0.7rem;
            background: var(--yl-pill-bg);
            color: var(--yl-pill-text);
            font-size: 0.92rem;
            line-height: 1.2;
            border: 1px solid var(--yl-border-soft);
        }

        .yearlens-section-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--yl-text);
            margin-top: 0.32rem;
            margin-bottom: 0.08rem;
            line-height: 1.2;
        }

        .yearlens-list {
            margin: 0 0 0.1rem 0;
            padding-left: 1.1rem;
        }

        .yearlens-list li {
            margin: 0.08rem 0;
            line-height: 1.35;
            color: var(--yl-text);
        }

        .yearlens-period-headline {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--yl-text);
            margin: 0.1rem 0 0.45rem 0;
            line-height: 1.25;
        }

        .yearlens-trust-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.7rem;
        }

        .yearlens-trust-item {
            min-width: 0;
        }

        .yearlens-score-label,
        .yearlens-score-value {
            font-size: 0.94rem;
            color: var(--yl-text-soft);
            margin: 0.12rem 0 0.12rem 0;
        }

        .yearlens-score-value {
            text-align: right;
        }

        .yearlens-explainer {
            border: 1px solid var(--yl-border-soft);
            border-radius: 12px;
            background: var(--yl-subtle-bg);
            padding: 0.65rem 0.75rem;
            margin: 0.2rem 0 0.15rem 0;
        }

        .yearlens-explainer-title {
            font-size: 0.93rem;
            font-weight: 700;
            color: var(--yl-text);
            margin-bottom: 0.18rem;
        }

        .yearlens-explainer-summary {
            font-size: 0.94rem;
            line-height: 1.45;
            color: var(--yl-text-soft);
        }

        @media (max-width: 640px) {
            .block-container {
                max-width: 100%;
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }

            .yearlens-hero h1 {
                font-size: 2.35rem;
            }

            .yearlens-hero p {
                font-size: 1rem;
            }

            .yearlens-card {
                padding: 0.8rem 0.85rem;
                border-radius: 14px;
            }

            .yearlens-value {
                font-size: 1rem;
            }

            .yearlens-trust-grid {
                grid-template-columns: 1fr;
                gap: 0.55rem;
            }

            div[data-testid="stForm"] {
                padding: 0.75rem 0.8rem 0.85rem 0.8rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
