import streamlit as st


def _render_pill_row(items: list[str]) -> None:
    pills = "".join(f"<span class='yearlens-pill'>{item}</span>" for item in items)
    st.markdown(f"<div class='yearlens-pill-row'>{pills}</div>", unsafe_allow_html=True)


def _render_list(title: str, items: list[str]) -> None:
    st.markdown(f"<div class='yearlens-section-title'>{title}</div>", unsafe_allow_html=True)
    bullet_list = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(f"<ul class='yearlens-list'>{bullet_list}</ul>", unsafe_allow_html=True)


def render_year_overview(overview: dict, metadata: dict) -> None:
    st.subheader("Year Overview")

    natal_chart = metadata["natal_chart"]
    anchor_label = "Birthday cycle" if metadata["year_anchor"] == "birthday" else "Calendar year"
    window_text = f"{metadata['window_start']} to {metadata['window_end']}"
    certainty_label, certainty_note = _certainty_note(natal_chart)
    backend_label, backend_note = _backend_note(natal_chart)
    location_label = _location_label(natal_chart)

    st.markdown(
        f"""
        <div class="yearlens-card">
            <div class="yearlens-trust-grid">
                <div class="yearlens-trust-item">
                    <div class="yearlens-kicker">Reading Window</div>
                    <div class="yearlens-value">{window_text}</div>
                </div>
                <div class="yearlens-trust-item">
                    <div class="yearlens-kicker">Anchor</div>
                    <div class="yearlens-value">{anchor_label}</div>
                </div>
                <div class="yearlens-trust-item">
                    <div class="yearlens-kicker">Birth Data Certainty</div>
                    <div class="yearlens-value">{certainty_label}</div>
                </div>
                <div class="yearlens-trust-item">
                    <div class="yearlens-kicker">Astro Backend</div>
                    <div class="yearlens-value">{backend_label}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if metadata["year_anchor"] == "birthday" and metadata["input_snapshot"]["birth_date"].endswith("-01-01"):
        st.info("Birthday anchor and calendar anchor are identical here because the birth date is January 1.")

    _render_pill_row(
        [
            f"Confidence {overview['confidence']:.0%}",
            certainty_label,
            backend_label,
            location_label,
            *overview.get("tone_summary", []),
        ]
    )

    st.write(overview["summary"])
    _render_list("Top Themes", overview["top_themes"])
    _render_list("Top Caution Periods", overview["top_caution_periods"])
    _render_list("Top Opportunity Periods", overview["top_opportunity_periods"])
    _render_list("Trust Notes", [certainty_note, backend_note])


def render_report_actions(report: dict) -> None:
    metadata = report["metadata"]
    natal_chart = metadata["natal_chart"]
    data_notes = [
        "This build keeps the generated report in the current session and does not write it to a database or report file by default.",
    ]

    if "manual_coordinates" in natal_chart["location"]["source"]:
        data_notes.append("Manual coordinates were used, so the app did not need to geocode the place name.")
    else:
        data_notes.append(
            "Because a place name was used, that location text was sent to the geocoder to resolve coordinates. Use manual coordinates and timezone if you want to avoid that."
        )

    note_items = "".join(f"<li>{item}</li>" for item in data_notes)
    st.markdown(
        f"""
        <div class="yearlens-card">
            <div class="yearlens-section-title">Before You Read</div>
            <ul class="yearlens-list">{note_items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Tip: if the year anchor looks unchanged, check the reading window dates above. January 1 birthdays produce the same birthday and calendar window.")


def _certainty_note(natal_chart: dict) -> tuple[str, str]:
    source = natal_chart["location"]["source"]
    backend = natal_chart["ephemeris_backend"]

    if "manual_coordinates" in source and "manual_timezone" in source and backend == "swisseph_files":
        return "Stronger input certainty", "Manual coordinates/timezone and Swiss ephemeris files give the cleanest baseline in the current build."
    if "manual_coordinates" in source:
        return "Good input certainty", "Manual coordinates improve location certainty, even if the backend still falls back to Moshier."
    if backend == "moshier_fallback":
        return "Some extra assumptions", "Geocoded location plus Moshier fallback means this reading is still usable, but not the cleanest possible setup."
    return "Normal input certainty", "The app resolved the location automatically. Manual coordinates/timezone can improve repeatability."


def _backend_note(natal_chart: dict) -> tuple[str, str]:
    if natal_chart["ephemeris_backend"] == "swisseph_files":
        return "Swiss files", "Swiss ephemeris files were available for this reading."
    return "Moshier fallback", "The reading used the Moshier fallback backend, so treat timing and confidence with a bit more caution."


def _location_label(natal_chart: dict) -> str:
    source = natal_chart["location"]["source"]
    if "manual_coordinates" in source and "manual_timezone" in source:
        return "Manual location + timezone"
    if "manual_coordinates" in source:
        return "Manual location"
    return "Geocoded location"
