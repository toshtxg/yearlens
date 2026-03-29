from datetime import date, time

import streamlit as st


def render_input_form() -> dict | None:
    with st.form("yearlens-input"):
        current_year = date.today().year
        year_options = list(range(current_year - 5, current_year + 11))
        date_year_col, name_col = st.columns([1, 1])
        with date_year_col:
            birth_date = st.date_input("Birth date", value=date(1990, 1, 1))
        with name_col:
            target_year = int(
                st.selectbox(
                    "Year to read",
                    options=year_options,
                    index=year_options.index(current_year),
                )
            )

        st.markdown("**Birth time**")
        time_col_1, time_col_2 = st.columns(2)
        with time_col_1:
            birth_hour = int(st.selectbox("Hour", options=list(range(24)), index=12, help="24-hour format."))
        with time_col_2:
            birth_minute = int(st.selectbox("Minute", options=list(range(60)), index=0))
        birth_time = time(birth_hour, birth_minute)
        st.caption("Use the most exact birth time you know. It helps the reading land more precisely.")

        birth_location = st.text_input("Birth location", value="Singapore")
        cycle_options = {
            "Birthday cycle": "birthday",
            "Calendar year": "calendar",
        }
        selected_cycle = st.selectbox("Reading cycle", list(cycle_options), index=0)
        year_anchor = cycle_options[selected_cycle]
        if birth_date.month == 1 and birth_date.day == 1:
            st.caption(f"Your birthday is January 1, so birthday cycle and calendar year produce the same {target_year} window.")
        else:
            st.caption(
                "Birthday cycle follows your personal year from birthday to birthday. "
                "Calendar year follows January through December."
            )

        with st.expander("Location overrides and advanced options"):
            zodiac = st.selectbox("Zodiac", ["sidereal"], index=0)
            ayanamsa = st.selectbox("Ayanamsa", ["lahiri"], index=0)
            house_system = st.selectbox("House system", ["whole_sign"], index=0)
            node_type = st.selectbox("Node type", ["true", "mean"], index=0)
            birth_latitude = st.text_input("Latitude override", value="", placeholder="e.g. 1.3521")
            birth_longitude = st.text_input("Longitude override", value="", placeholder="e.g. 103.8198")
            timezone_id = st.text_input("Timezone override", value="", placeholder="e.g. Asia/Singapore")
            name = st.text_input("Display name", value="", placeholder="Optional")
            st.caption("Manual coordinates and timezone let you bypass place-name lookup for more repeatable results and better privacy.")

        submitted = st.form_submit_button("Generate Reading", use_container_width=True)

    if not submitted:
        return None

    return {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_location": birth_location,
        "birth_latitude": birth_latitude or None,
        "birth_longitude": birth_longitude or None,
        "timezone_id": timezone_id or None,
        "target_year": target_year,
        "name": name or None,
        "year_anchor": year_anchor,
        "preferences": {
            "zodiac": zodiac,
            "ayanamsa": ayanamsa,
            "house_system": house_system,
            "node_type": node_type,
        },
    }
