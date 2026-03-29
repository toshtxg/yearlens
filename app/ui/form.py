from datetime import date, time

import streamlit as st


def render_input_form() -> dict | None:
    with st.form("yearlens-input"):
        left, right = st.columns(2)

        with left:
            birth_date = st.date_input("Birth date", value=date(1990, 1, 1))
            birth_time = st.time_input("Birth time", value=time(12, 0))
            birth_location = st.text_input("Birth location", value="Singapore")

        with right:
            target_year = int(st.number_input("Target year", min_value=1900, max_value=2100, value=date.today().year, step=1))
            name = st.text_input("Display name", value="")
            year_anchor = st.selectbox("Year anchor", ["birthday", "calendar"], index=0)

        with st.expander("Advanced settings"):
            zodiac = st.selectbox("Zodiac", ["sidereal"], index=0)
            ayanamsa = st.selectbox("Ayanamsa", ["lahiri"], index=0)
            house_system = st.selectbox("House system", ["whole_sign"], index=0)
            node_type = st.selectbox("Node type", ["true", "mean"], index=0)

        submitted = st.form_submit_button("Generate Reading", use_container_width=True)

    if not submitted:
        return None

    return {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_location": birth_location,
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

