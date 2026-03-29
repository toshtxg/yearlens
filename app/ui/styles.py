import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

        :root {
            --yl-header-offset: 4.4rem;
            --yl-bg: #0b1120;
            --yl-bg-soft: #10192c;
            --yl-surface: rgba(16, 24, 40, 0.82);
            --yl-surface-strong: rgba(20, 31, 50, 0.96);
            --yl-surface-soft: rgba(28, 41, 66, 0.84);
            --yl-border: rgba(148, 163, 184, 0.22);
            --yl-border-strong: rgba(148, 163, 184, 0.32);
            --yl-text: #eef2ff;
            --yl-text-soft: #c8d1e4;
            --yl-text-muted: #8fa0bc;
            --yl-accent: #d7a441;
            --yl-accent-soft: #f4c96b;
            --yl-accent-cool: #7dd3fc;
            --yl-success: #4ade80;
            --yl-warning: #fbbf24;
            --yl-danger: #fb7185;
            --yl-pill-bg: rgba(52, 70, 102, 0.8);
            --yl-pill-text: #eff6ff;
            --yl-shadow: 0 30px 80px rgba(2, 6, 23, 0.42);
            --yl-input-bg: rgba(18, 29, 48, 0.9);
            --yl-input-text: #eef2ff;
            --yl-input-border: rgba(110, 130, 165, 0.24);
        }

        html, body, [data-testid="stAppViewContainer"], .stApp, [data-testid="stHeader"] {
            background:
                radial-gradient(circle at top left, rgba(125, 211, 252, 0.08), transparent 24%),
                radial-gradient(circle at top right, rgba(215, 164, 65, 0.12), transparent 28%),
                linear-gradient(180deg, #0a1020 0%, #0d1527 100%) !important;
            color: var(--yl-text) !important;
            font-family: "Manrope", sans-serif !important;
        }

        .block-container {
            max-width: 920px;
            padding-top: calc(var(--yl-header-offset) + 0.9rem);
            padding-bottom: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        [data-testid="stToolbar"] {
            background: transparent !important;
        }

        h1, h2, h3, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2 {
            font-family: "Space Grotesk", sans-serif !important;
            letter-spacing: -0.03em;
        }

        .yearlens-hero-shell {
            position: relative;
            overflow: hidden;
            border: 1px solid var(--yl-border-strong);
            border-radius: 28px;
            padding: 1.25rem 1.3rem 1.35rem 1.3rem;
            margin-bottom: 0.9rem;
            background:
                linear-gradient(145deg, rgba(21, 31, 52, 0.98) 0%, rgba(13, 19, 34, 0.94) 100%);
            box-shadow: var(--yl-shadow);
        }

        .yearlens-hero-shell::before {
            content: "";
            position: absolute;
            inset: auto -10% -45% auto;
            width: 320px;
            height: 320px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(215, 164, 65, 0.18), transparent 65%);
            pointer-events: none;
        }

        .yearlens-eyebrow {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: var(--yl-accent-soft);
            margin-bottom: 0.55rem;
            font-weight: 700;
        }

        .yearlens-hero {
            position: relative;
            z-index: 1;
        }

        .yearlens-hero h1 {
            font-size: clamp(3.1rem, 8vw, 4.8rem);
            line-height: 0.92;
            margin: 0 0 0.7rem 0;
            color: var(--yl-text);
        }

        .yearlens-hero p {
            margin: 0;
            font-size: 1.12rem;
            line-height: 1.7;
            color: var(--yl-text-soft);
            max-width: 48rem;
        }

        .yearlens-note-card,
        .yearlens-card,
        div[data-testid="stForm"] {
            border: 1px solid var(--yl-border);
            border-radius: 22px;
            background: var(--yl-surface);
            box-shadow: var(--yl-shadow);
        }

        .yearlens-note-card {
            padding: 1rem 1.05rem;
            min-height: 100%;
            margin-bottom: 0.9rem;
            background:
                linear-gradient(160deg, rgba(17, 26, 43, 0.96), rgba(11, 17, 31, 0.9)),
                radial-gradient(circle at top right, rgba(125, 211, 252, 0.08), transparent 40%);
        }

        .yearlens-note-card-muted {
            background:
                linear-gradient(160deg, rgba(17, 26, 43, 0.96), rgba(11, 17, 31, 0.9)),
                radial-gradient(circle at top right, rgba(215, 164, 65, 0.1), transparent 42%);
        }

        .yearlens-note-title {
            font-size: 1.02rem;
            font-weight: 800;
            color: var(--yl-text);
            margin-bottom: 0.4rem;
        }

        .yearlens-note-list {
            margin: 0;
            padding-left: 1.1rem;
            color: var(--yl-text-soft);
        }

        .yearlens-note-list li {
            margin: 0.22rem 0;
            line-height: 1.5;
        }

        div[data-testid="stForm"] {
            padding: 0.95rem 1rem 1rem 1rem;
            margin-top: 0.25rem;
            background: linear-gradient(160deg, rgba(18, 28, 45, 0.96), rgba(14, 22, 37, 0.92));
        }

        .yearlens-placeholder-card {
            border: 1px dashed rgba(148, 163, 184, 0.25);
            border-radius: 22px;
            padding: 1rem 1.05rem;
            margin-top: 0.45rem;
            background: rgba(15, 23, 42, 0.55);
        }

        .yearlens-placeholder-title {
            font-size: 1rem;
            font-weight: 800;
            color: var(--yl-text);
            margin-bottom: 0.25rem;
        }

        .yearlens-placeholder-copy {
            font-size: 0.97rem;
            line-height: 1.6;
            color: var(--yl-text-soft);
        }

        div[data-testid="stForm"] label,
        div[data-testid="stExpander"] label,
        div[data-testid="stRadio"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stTextInput"] label {
            font-size: 0.96rem;
            font-weight: 700;
            color: var(--yl-text) !important;
        }

        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stText"],
        div[data-testid="stCaptionContainer"] {
            color: var(--yl-text-soft) !important;
        }

        div[data-testid="stCaptionContainer"] {
            margin-top: -0.12rem;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-testid="stDateInput"] > div,
        div[data-testid="stNumberInput"] > div,
        div[data-testid="stTextInputRootElement"] > div {
            min-height: 2.95rem;
            background: var(--yl-input-bg) !important;
            border-color: var(--yl-input-border) !important;
            color: var(--yl-input-text) !important;
            border-radius: 16px !important;
        }

        div[data-baseweb="input"] input,
        div[data-baseweb="select"] *,
        div[data-testid="stDateInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextInputRootElement"] input {
            font-size: 1rem;
            color: var(--yl-input-text) !important;
            background: transparent !important;
            caret-color: var(--yl-input-text) !important;
        }

        div[data-testid="stFormSubmitButton"] button,
        div[data-testid="stButton"] button,
        div[data-testid="stLinkButton"] a {
            min-height: 3rem;
            font-size: 1rem;
            font-weight: 700;
            color: #0f172a !important;
            border: none !important;
            border-radius: 16px !important;
            background: linear-gradient(135deg, var(--yl-accent-soft), var(--yl-accent)) !important;
            box-shadow: 0 16px 30px rgba(215, 164, 65, 0.22);
        }
        div[data-testid="stFormSubmitButton"] button p,
        div[data-testid="stButton"] button p,
        div[data-testid="stLinkButton"] a p {
            color: #0f172a !important;
        }

        div[data-testid="stSegmentedControl"] button {
            background: rgba(31, 45, 73, 0.7) !important;
            border-color: var(--yl-border) !important;
            color: var(--yl-text) !important;
            border-radius: 999px !important;
        }

        div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
            background: linear-gradient(135deg, rgba(125, 211, 252, 0.25), rgba(215, 164, 65, 0.26)) !important;
            color: var(--yl-text) !important;
            border-color: rgba(215, 164, 65, 0.35) !important;
        }

        div[data-testid="stExpander"] details {
            border: 1px solid var(--yl-border);
            border-radius: 22px;
            background: linear-gradient(160deg, rgba(17, 26, 43, 0.98), rgba(12, 18, 32, 0.94));
            overflow: hidden;
            box-shadow: var(--yl-shadow);
        }

        div[data-testid="stExpander"] summary {
            padding-top: 0.15rem;
            padding-bottom: 0.15rem;
        }

        div[data-testid="stExpander"] summary p {
            color: var(--yl-text) !important;
            font-size: 0.98rem !important;
            font-weight: 700 !important;
            line-height: 1.35 !important;
        }

        div[data-testid="stExpander"] details[open] summary {
            border-bottom: 1px solid var(--yl-border);
            background: rgba(255, 255, 255, 0.02);
        }

        .yearlens-card {
            padding: 1rem 1.05rem;
            margin-bottom: 0.85rem;
        }

        .yearlens-kicker {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: var(--yl-text-muted);
            margin-bottom: 0.28rem;
            font-weight: 700;
        }

        .yearlens-value {
            font-size: 1.02rem;
            font-weight: 700;
            color: var(--yl-text);
            line-height: 1.35;
        }

        .yearlens-pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 0.2rem 0 0.7rem 0;
        }

        .yearlens-pill {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.42rem 0.78rem;
            background: var(--yl-pill-bg);
            color: var(--yl-pill-text);
            font-size: 0.92rem;
            line-height: 1.2;
            border: 1px solid rgba(148, 163, 184, 0.16);
        }

        .yearlens-pill-now {
            background: var(--yl-accent);
            color: #111827;
            font-weight: 800;
            border-color: transparent;
        }

        .yearlens-section-heading {
            font-size: 1.45rem;
            font-family: "Space Grotesk", sans-serif;
            color: var(--yl-text);
            margin: 1.1rem 0 0.2rem 0;
        }

        .yearlens-section-heading-compact {
            margin-top: 0.8rem;
            margin-bottom: 0.1rem;
        }

        .yearlens-section-title {
            font-size: 0.9rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            color: var(--yl-text);
            margin-top: 0.5rem;
            margin-bottom: 0.28rem;
            line-height: 1.2;
        }

        .yearlens-list,
        .yearlens-compact-list,
        .yearlens-mini-list {
            margin: 0;
            padding-left: 1.1rem;
        }

        .yearlens-list li,
        .yearlens-compact-list li,
        .yearlens-mini-list li {
            margin: 0.14rem 0;
            line-height: 1.45;
            color: var(--yl-text-soft);
        }

        .yearlens-overview-shell {
            border: 1px solid rgba(215, 164, 65, 0.18);
            border-radius: 24px;
            padding: 1.1rem 1.15rem 1rem 1.15rem;
            margin-bottom: 0.85rem;
            background:
                radial-gradient(circle at top right, rgba(215, 164, 65, 0.12), transparent 30%),
                linear-gradient(155deg, rgba(18, 28, 44, 0.98), rgba(13, 19, 34, 0.92));
            box-shadow: var(--yl-shadow);
        }

        .yearlens-overview-title {
            font-size: 1.36rem;
            font-family: "Space Grotesk", sans-serif;
            line-height: 1.35;
            color: var(--yl-text);
            margin-bottom: 0.65rem;
        }

        .yearlens-overview-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            color: var(--yl-text-soft);
            font-size: 0.92rem;
        }

        .yearlens-overview-meta span {
            display: inline-flex;
            align-items: center;
            padding: 0.38rem 0.7rem;
            border-radius: 999px;
            background: rgba(42, 56, 86, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.16);
        }

        .yearlens-tone-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin: 0.2rem 0 0.9rem 0;
        }

        .yearlens-tone-chip,
        .yearlens-timeline-legend-item {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.4rem 0.7rem;
            border-radius: 999px;
            background: rgba(26, 38, 61, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.14);
            color: var(--yl-text);
            font-size: 0.88rem;
            font-weight: 700;
        }

        .yearlens-tone-dot {
            width: 0.62rem;
            height: 0.62rem;
            border-radius: 999px;
            flex: 0 0 auto;
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.04);
        }

        .yearlens-domain-emphasis-shell,
        .yearlens-year-rhythm {
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 20px;
            padding: 0.85rem 0.9rem 0.9rem 0.9rem;
            background: rgba(18, 28, 44, 0.72);
            margin-bottom: 0.85rem;
        }

        .yearlens-section-title-inline {
            margin-top: 0;
            margin-bottom: 0.6rem;
        }

        .yearlens-domain-emphasis-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.6rem;
        }

        .yearlens-domain-emphasis-card {
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 16px;
            padding: 0.72rem 0.78rem;
            background: rgba(15, 23, 42, 0.55);
        }

        .yearlens-domain-emphasis-head {
            display: flex;
            justify-content: space-between;
            gap: 0.5rem;
            color: var(--yl-text);
            font-size: 0.88rem;
            font-weight: 700;
            margin-bottom: 0.38rem;
        }

        .yearlens-domain-emphasis-meter {
            width: 100%;
            height: 0.42rem;
            border-radius: 999px;
            background: rgba(58, 72, 102, 0.6);
            overflow: hidden;
        }

        .yearlens-domain-emphasis-meter span {
            display: block;
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(125, 211, 252, 0.95), rgba(215, 164, 65, 0.95));
        }

        .yearlens-timeline-bar {
            display: flex;
            width: 100%;
            height: 38px;
            border-radius: 12px;
            overflow: hidden;
            margin: 0;
            gap: 2px;
            background: rgba(255, 255, 255, 0.03);
        }

        .yearlens-timeline-segment {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.68rem;
            color: #111827;
            font-weight: 700;
            letter-spacing: 0.02em;
            cursor: default;
            transition: opacity 0.15s ease;
            border-radius: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .yearlens-timeline-segment:hover {
            opacity: 0.82;
        }

        .yearlens-timeline-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.7rem;
        }

        .yearlens-mini-card {
            height: 100%;
            border: 1px solid var(--yl-border);
            border-radius: 20px;
            padding: 0.9rem 0.9rem 0.85rem 0.9rem;
            background: linear-gradient(160deg, rgba(18, 28, 44, 0.96), rgba(13, 19, 34, 0.9));
            box-shadow: var(--yl-shadow);
        }

        .yearlens-mini-card-theme {
            border-color: rgba(125, 211, 252, 0.2);
        }

        .yearlens-mini-card-up {
            border-color: rgba(74, 222, 128, 0.22);
        }

        .yearlens-mini-card-warn {
            border-color: rgba(251, 191, 36, 0.22);
        }

        .yearlens-mini-card-title {
            font-size: 0.95rem;
            font-weight: 800;
            color: var(--yl-text);
            margin-bottom: 0.35rem;
        }

        .yearlens-mini-period-item {
            list-style: none;
            margin-left: -0.2rem;
            padding: 0.12rem 0 0.38rem 0;
        }

        .yearlens-mini-period-date {
            color: var(--yl-text-muted);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.14rem;
            font-weight: 700;
        }

        .yearlens-mini-period-copy {
            color: var(--yl-text);
            font-size: 0.95rem;
            line-height: 1.45;
            font-weight: 700;
        }

        .yearlens-period-headline {
            font-size: 1.22rem;
            font-family: "Space Grotesk", sans-serif;
            font-weight: 700;
            color: var(--yl-text);
            margin: 0 0 0.38rem 0;
            line-height: 1.2;
        }

        .yearlens-story-card {
            border: 1px solid rgba(125, 211, 252, 0.14);
            border-radius: 20px;
            padding: 0.95rem 1rem;
            background:
                radial-gradient(circle at top right, rgba(125, 211, 252, 0.08), transparent 30%),
                linear-gradient(155deg, rgba(18, 28, 44, 0.98), rgba(11, 17, 31, 0.94));
            margin-bottom: 0.7rem;
        }

        .yearlens-story-card-concise {
            margin-bottom: 0.82rem;
        }

        .yearlens-story-kicker {
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            color: var(--yl-accent-soft);
            margin-bottom: 0.35rem;
            font-weight: 800;
        }

        .yearlens-story-copy {
            color: var(--yl-text-soft);
            font-size: 1.02rem;
            line-height: 1.72;
            margin-bottom: 0.45rem;
        }

        .yearlens-story-meta {
            color: var(--yl-text-muted);
            font-size: 0.9rem;
        }

        .yearlens-signal-card {
            height: 100%;
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 18px;
            padding: 0.82rem 0.85rem;
            background: rgba(26, 38, 61, 0.72);
            margin-bottom: 0.55rem;
        }

        .yearlens-signal-title {
            color: var(--yl-text);
            font-size: 0.93rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
            line-height: 1.35;
        }

        .yearlens-signal-body {
            color: var(--yl-text-soft);
            font-size: 0.9rem;
            line-height: 1.55;
        }

        .yearlens-period-accent {
            height: 4px;
            border-radius: 999px 999px 0 0;
            margin: 0.35rem 0 -0.35rem 0;
            opacity: 0.9;
        }

        .yearlens-action-card {
            border: 1px solid var(--yl-border);
            border-radius: 18px;
            padding: 0.62rem 0.8rem 0.72rem 0.8rem;
            min-height: 100%;
            background: rgba(17, 26, 43, 0.88);
        }

        .yearlens-action-card .yearlens-compact-list {
            list-style: none;
            padding-left: 0;
        }

        .yearlens-action-card .yearlens-compact-list li {
            margin: 0.28rem 0;
            line-height: 1.5;
        }

        .yearlens-action-card-up {
            border-color: rgba(74, 222, 128, 0.2);
        }

        .yearlens-action-card-warn {
            border-color: rgba(251, 191, 36, 0.22);
        }

        .yearlens-score-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.6rem;
            margin-top: 0.2rem;
        }

        .yearlens-score-card {
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 18px;
            padding: 0.75rem 0.8rem;
            background: rgba(18, 28, 44, 0.82);
        }

        .yearlens-score-card-head {
            display: flex;
            justify-content: space-between;
            gap: 0.6rem;
            color: var(--yl-text);
            font-size: 0.92rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }

        .yearlens-score-meter {
            width: 100%;
            height: 0.48rem;
            border-radius: 999px;
            background: rgba(58, 72, 102, 0.65);
            overflow: hidden;
        }

        .yearlens-score-meter span {
            display: block;
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--yl-accent-soft), var(--yl-accent));
        }

        .yearlens-takeaway-card {
            border: 1px solid rgba(125, 211, 252, 0.16);
            border-radius: 18px;
            padding: 0.8rem 0.9rem 0.85rem 0.9rem;
            background:
                radial-gradient(circle at top right, rgba(215, 164, 65, 0.08), transparent 34%),
                rgba(18, 28, 44, 0.78);
        }

        .yearlens-takeaway-lead {
            color: var(--yl-text);
            font-size: 1rem;
            line-height: 1.55;
            font-weight: 700;
        }

        .yearlens-takeaway-sub {
            color: var(--yl-text-soft);
            font-size: 0.92rem;
            line-height: 1.55;
            margin-top: 0.35rem;
        }

        .yearlens-explainer {
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 18px;
            background: rgba(18, 28, 44, 0.78);
            padding: 0.75rem 0.8rem;
            margin: 0.2rem 0 0.12rem 0;
        }

        .yearlens-explainer-title {
            font-size: 0.92rem;
            font-weight: 800;
            color: var(--yl-text);
            margin-bottom: 0.22rem;
        }

        .yearlens-explainer-summary {
            font-size: 0.92rem;
            line-height: 1.55;
            color: var(--yl-text-soft);
        }

        @media (max-width: 900px) {
            .yearlens-domain-emphasis-grid,
            .yearlens-score-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 700px) {
            :root {
                --yl-header-offset: 3.9rem;
            }

            .block-container {
                max-width: 100%;
                padding-left: 0.82rem;
                padding-right: 0.82rem;
            }

            .yearlens-hero-shell {
                padding: 1rem 1rem 1.08rem 1rem;
                border-radius: 24px;
            }

            .yearlens-hero h1 {
                font-size: 2.6rem;
            }

            .yearlens-hero p {
                font-size: 1rem;
            }

            .yearlens-note-card,
            .yearlens-card,
            div[data-testid="stForm"],
            div[data-testid="stExpander"] details {
                border-radius: 18px;
            }

            .yearlens-score-grid {
                grid-template-columns: 1fr;
            }

            .yearlens-overview-meta {
                gap: 0.42rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
