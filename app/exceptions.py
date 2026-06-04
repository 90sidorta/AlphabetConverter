from typing import List, Optional, Union

from pydantic import BaseModel


class AlphabetException(Exception):
    def __init__(
        self,
        status_code: Optional[int] = 500,
        message: Optional[str] = "Internal Server Error",
        location: Optional[str] = None,
        path: Optional[List[Union[str, int]]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.location = location
        self.path = path


class AlphabetBulkException(Exception):
    def __init__(
        self,
        status_code: Optional[int] = 500,
        errors: Optional[List[AlphabetException]] = None,
    ):
        self.status_code = status_code
        self.errors = errors


class AlphabetError(BaseModel):
    message: str
    location: str
    path: Optional[List[Union[str, int]]] = None


class AlphabetBulkError(BaseModel):
    errors: List[AlphabetError]
