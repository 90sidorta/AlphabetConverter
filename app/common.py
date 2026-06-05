import enum
from typing import Optional

from pydantic import BaseModel


class SortOrder(enum.Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


class Pagination(BaseModel):
    total_records: int
    limit: Optional[int] = None
    offset: Optional[int] = None
