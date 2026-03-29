from datetime import date, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReadingPreferences(BaseModel):
    zodiac: Literal["sidereal"] = "sidereal"
    ayanamsa: str = "lahiri"
    house_system: Literal["whole_sign"] = "whole_sign"
    node_type: Literal["true", "mean"] = "true"


class UserInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    birth_date: date
    birth_time: time
    birth_location: str = Field(min_length=2)
    target_year: int = Field(ge=1900, le=2100)
    name: str | None = None
    year_anchor: Literal["birthday", "calendar"] = "birthday"
    preferences: ReadingPreferences = Field(default_factory=ReadingPreferences)

    @field_validator("birth_location")
    @classmethod
    def validate_location(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Birth location is required.")
        return value

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

