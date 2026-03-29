from datetime import date, time

import pytest
from pydantic import ValidationError

from app.core.input_schema import UserInput


def test_valid_user_input_defaults() -> None:
    model = UserInput(
        birth_date=date(1990, 1, 1),
        birth_time=time(12, 0),
        birth_location="Singapore",
        target_year=2026,
    )

    assert model.year_anchor == "birthday"
    assert model.preferences.zodiac == "sidereal"


def test_blank_location_is_rejected() -> None:
    with pytest.raises(ValidationError):
        UserInput(
            birth_date=date(1990, 1, 1),
            birth_time=time(12, 0),
            birth_location="   ",
            target_year=2026,
        )

