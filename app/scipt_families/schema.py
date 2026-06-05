import enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.common import Pagination, SortOrder
from app.limits import LIMITS


class ScriptFamilySortBy(enum.Enum):
    """Enum for sorting script families."""
    NAME = "name"
    DATE_CREATED = "date_created"


class CreateScriptFamily(BaseModel):
    name: str = Field(..., min_length=LIMITS.script_family_name_min, max_length=LIMITS.script_family_name_max)

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class ReadScriptFamily(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class ListScriptFamily(BaseModel):
    data: List[ReadScriptFamily]
    pagination: Pagination
    sort_order: SortOrder
    sort_by: ScriptFamilySortBy
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateScriptFamily(CreateScriptFamily):
    pass


class DeleteScriptFamily(BaseModel):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
