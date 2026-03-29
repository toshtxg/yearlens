import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 860px;
            padding-top: 1rem;
            padding-bottom: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .yearlens-card {
            border: 1px solid rgba(120, 113, 108, 0.22);
            border-radius: 16px;
            background: rgba(255, 252, 245, 0.88);
            padding: 0.9rem 1rem;
            margin-bottom: 0.85rem;
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
            margin: 0.35rem 0 0.75rem 0;
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
            font-size: 0.98rem;
            font-weight: 700;
            color: #1f2937;
            margin-top: 0.75rem;
            margin-bottom: 0.35rem;
        }

        .yearlens-list {
            margin: 0.15rem 0 0.25rem 0;
            padding-left: 1.1rem;
        }

        .yearlens-list li {
            margin: 0.2rem 0;
        }

        @media (max-width: 640px) {
            .block-container {
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }

            .yearlens-card {
                padding: 0.8rem 0.85rem;
                border-radius: 14px;
            }

            .yearlens-value {
                font-size: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
