import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
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
            color: #1f2937;
        }

        .yearlens-hero p {
            margin: 0;
            font-size: 1rem;
            line-height: 1.55;
            color: #6b7280;
            max-width: 44rem;
        }

        div[data-testid="stForm"] {
            padding: 0.8rem 0.9rem 0.9rem 0.9rem;
        }

        div[data-testid="stForm"] label,
        div[data-testid="stExpander"] label {
            font-size: 0.96rem;
        }

        div[data-testid="stCaptionContainer"] {
            margin-top: -0.15rem;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-testid="stDateInput"] > div,
        div[data-testid="stNumberInput"] > div {
            min-height: 2.85rem;
        }

        div[data-baseweb="input"] input,
        div[data-baseweb="select"] *,
        div[data-testid="stDateInput"] input,
        div[data-testid="stNumberInput"] input {
            font-size: 0.98rem;
        }

        div[data-testid="stNumberInput"] button {
            min-width: 2rem;
            min-height: 2rem;
        }

        div[data-testid="stFormSubmitButton"] button {
            min-height: 2.9rem;
            font-size: 1rem;
        }

        .yearlens-card {
            border: 1px solid rgba(120, 113, 108, 0.22);
            border-radius: 16px;
            background: rgba(255, 252, 245, 0.88);
            padding: 0.8rem 0.9rem;
            margin-bottom: 0.7rem;
        }

        .yearlens-kicker {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #7c6f64;
            margin-bottom: 0.25rem;
        }

        .yearlens-value {
            font-size: 1.05rem;
            font-weight: 600;
            color: #1f2937;
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
            background: #efe7d4;
            color: #3f3a33;
            font-size: 0.92rem;
            line-height: 1.2;
            border: 1px solid rgba(120, 113, 108, 0.16);
        }

        .yearlens-section-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: #1f2937;
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
        }

        .yearlens-period-headline {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1f2937;
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

        .yearlens-score-list {
            display: grid;
            gap: 0.5rem;
            margin: 0.18rem 0 0.35rem 0;
        }

        .yearlens-score-row {
            display: grid;
            gap: 0.18rem;
        }

        .yearlens-score-meta {
            display: flex;
            justify-content: space-between;
            gap: 0.6rem;
            font-size: 0.92rem;
            color: #374151;
        }

        .yearlens-score-bar {
            width: 100%;
            height: 0.46rem;
            border-radius: 999px;
            background: rgba(191, 167, 108, 0.18);
            overflow: hidden;
        }

        .yearlens-score-bar span {
            display: block;
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #b68b3a 0%, #d7b162 100%);
        }

        .yearlens-explainer {
            border: 1px solid rgba(120, 113, 108, 0.16);
            border-radius: 12px;
            background: rgba(255, 252, 245, 0.78);
            padding: 0.65rem 0.75rem;
            margin: 0.2rem 0 0.15rem 0;
        }

        .yearlens-explainer-title {
            font-size: 0.93rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 0.18rem;
        }

        .yearlens-explainer-summary {
            font-size: 0.94rem;
            line-height: 1.45;
            color: #4b5563;
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
