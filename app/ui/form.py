from datetime import date, time

import streamlit as st

from app.i18n import t


def render_input_form() -> dict | None:
    with st.form("yearlens-input"):
        current_year = date.today().year
        year_options = list(range(current_year - 5, current_year + 11))
        date_year_col, name_col = st.columns([1, 1])
        with date_year_col:
            birth_date = st.date_input(str(t("form_birth_date")), value=date(1990, 1, 1))
        with name_col:
            target_year = int(
                st.selectbox(
                    str(t("form_year_to_read")),
                    options=year_options,
                    index=year_options.index(current_year),
                )
            )

        st.markdown(f"**{t('form_birth_time')}**")
        time_col_1, time_col_2 = st.columns(2)
        with time_col_1:
            birth_hour = int(st.selectbox(str(t("form_hour")), options=list(range(24)), index=12, help=str(t("form_hour_help"))))
        with time_col_2:
            birth_minute = int(st.selectbox(str(t("form_minute")), options=list(range(60)), index=0))
        birth_time = time(birth_hour, birth_minute)
        st.caption(str(t("form_birth_time_caption")))

        birth_location = st.text_input(str(t("form_birth_location")), value="Singapore")
        cycle_options = {
            str(t("form_birthday_cycle")): "birthday",
            str(t("form_calendar_year")): "calendar",
        }
        selected_cycle = st.selectbox(str(t("form_reading_cycle")), list(cycle_options), index=0)
        year_anchor = cycle_options[selected_cycle]
        if birth_date.month == 1 and birth_date.day == 1:
            st.caption(str(t("form_cycle_same", year=str(target_year))))
        else:
            st.caption(str(t("form_cycle_explain")))

        with st.expander(str(t("form_advanced_title"))):
            zodiac = st.selectbox(str(t("form_zodiac")), ["sidereal"], index=0)
            ayanamsa = st.selectbox(str(t("form_ayanamsa")), ["lahiri"], index=0)
            house_system = st.selectbox(str(t("form_house_system")), ["whole_sign"], index=0)
            node_type = st.selectbox(str(t("form_node_type")), ["true", "mean"], index=0)
            birth_latitude = st.text_input(str(t("form_lat_override")), value="", placeholder="e.g. 1.3521")
            birth_longitude = st.text_input(str(t("form_lon_override")), value="", placeholder="e.g. 103.8198")
            timezone_id = st.text_input(str(t("form_tz_override")), value="", placeholder="e.g. Asia/Singapore")
            name = st.text_input(str(t("form_display_name")), value="", placeholder="Optional")
            st.caption(str(t("form_advanced_caption")))

        submitted = st.form_submit_button(str(t("form_submit")), use_container_width=True)

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
