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

            div[data-testid="stForm"] {
                padding: 0.75rem 0.8rem 0.85rem 0.8rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
