from typing import List, Optional
from uuid import UUID

from app.avestan.exceptions import InvalidAvestanDirection
from app.db.models.alphabet import WrittingDirection
from app.limits import LIMITS
from pydantic import BaseModel, ConfigDict, Field, field_validator
from starlette import status


class AvestanToLatinWord(BaseModel):
    transliterated: str

    model_config = ConfigDict(from_attributes=True)


class TransliterateAvestanToLatin(BaseModel):
    word: str = Field(..., min_length=LIMITS.word_min_length, max_length=LIMITS.word_max_length)
    direction: WrittingDirection = WrittingDirection.RTL
    alphabet_id: UUID
    transliteration_system_id: UUID

    @field_validator("direction")
    def ensure_valid_direction(cls, v):
        if v not in [WrittingDirection.RTL, WrittingDirection.LTR]:
            raise InvalidAvestanDirection(direction=v)
        return v

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
