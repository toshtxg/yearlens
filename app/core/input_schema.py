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
    birth_latitude: float | None = None
    birth_longitude: float | None = None
    timezone_id: str | None = None
    target_year: int = Field(ge=1900, le=2100)
    name: str | None = None
    year_anchor: Literal["birthday", "calendar"] = "calendar"
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

    @field_validator("timezone_id")
    @classmethod
    def normalize_timezone_id(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @field_validator("birth_latitude")
    @classmethod
    def validate_latitude(cls, value: float | None) -> float | None:
        if value is None:
            return None
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return value

    @field_validator("birth_longitude")
    @classmethod
    def validate_longitude(cls, value: float | None) -> float | None:
        if value is None:
            return None
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return value
