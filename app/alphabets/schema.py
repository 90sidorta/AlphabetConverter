import enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.common import Pagination, SortOrder
from app.limits import LIMITS
from app.db.models.alphabet import WrittingDirection, WrittingSystem


class AlphabetSortBy(enum.Enum):
    """Enum for sorting alphabets."""
    NAME = "name"
    DATE_CREATED = "date_created"


class CreateAlphabet(BaseModel):
    name: str = Field(..., min_length=LIMITS.alphabet_name_min, max_length=LIMITS.alphabet_name_max)
    script_family_id: UUID = Field(...)
    writing_system: WrittingSystem = WrittingSystem.ALPHABET
    writing_direction: WrittingDirection = WrittingDirection.LTR

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class ReadAlphabet(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class ListAlphabet(BaseModel):
    data: List[ReadAlphabet]
    pagination: Pagination
    sort_order: SortOrder
    sort_by: AlphabetSortBy
    name: Optional[str] = None
    writting_system: Optional[WrittingSystem] = None
    writting_direction: Optional[WrittingDirection] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateAlphabet(BaseModel):
    name: Optional[str] = Field(None, min_length=LIMITS.alphabet_name_min, max_length=LIMITS.alphabet_name_max)
    script_family_id: Optional[UUID] = Field(None)
    writting_system: Optional[WrittingSystem] = Field(None)
    writting_direction: Optional[WrittingDirection] = Field(None)

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class DeleteAlphabet(BaseModel):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
