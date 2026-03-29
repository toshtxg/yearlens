from datetime import date, time

import streamlit as st


def render_input_form() -> dict | None:
    with st.form("yearlens-input"):
        date_year_col, name_col = st.columns([1, 1])
        with date_year_col:
            birth_date = st.date_input("Birth date", value=date(1990, 1, 1))
        with name_col:
            target_year = int(st.number_input("Target year", min_value=1900, max_value=2100, value=date.today().year, step=1))

        st.markdown("**Birth time**")
        time_col_1, time_col_2 = st.columns(2)
        with time_col_1:
            birth_hour = int(
                st.number_input(
                    "Hour",
                    min_value=0,
                    max_value=23,
                    value=12,
                    step=1,
                    help="24-hour format.",
                )
            )
        with time_col_2:
            birth_minute = int(
                st.number_input(
                    "Minute",
                    min_value=0,
                    max_value=59,
                    value=0,
                    step=1,
                )
            )
        birth_time = time(birth_hour, birth_minute)
        st.caption("Enter birth time as exact hour and minute when known.")

        birth_location = st.text_input("Birth location", value="Singapore")
        name = st.text_input("Display name", value="", placeholder="Optional")
        year_anchor = st.selectbox("Year anchor", ["birthday", "calendar"], index=0)
        if birth_date.month == 1 and birth_date.day == 1:
            st.caption("Your birthday is January 1, so `birthday` and `calendar` will produce the same 2026 window.")
        else:
            st.caption(
                "`birthday` uses your personal 12-month cycle starting on your birthday. "
                "`calendar` uses January 1 to December 31."
            )

        with st.expander("Advanced settings"):
            zodiac = st.selectbox("Zodiac", ["sidereal"], index=0)
            ayanamsa = st.selectbox("Ayanamsa", ["lahiri"], index=0)
            house_system = st.selectbox("House system", ["whole_sign"], index=0)
            node_type = st.selectbox("Node type", ["true", "mean"], index=0)
            birth_latitude = st.text_input("Latitude override", value="", placeholder="e.g. 1.3521")
            birth_longitude = st.text_input("Longitude override", value="", placeholder="e.g. 103.8198")
            timezone_id = st.text_input("Timezone override", value="", placeholder="e.g. Asia/Singapore")
            st.caption("Optional. Use manual coordinates/timezone to bypass geocoding when needed.")

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
