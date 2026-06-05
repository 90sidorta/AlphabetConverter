from uuid import UUID

from starlette import status

from app.exceptions import AlphabetException


class DuplicatedAlphabetName(AlphabetException):
    def __init__(self, name: str):
        self.status_code = status.HTTP_409_CONFLICT
        self.message = f"Alphabet {name} already exists."
        self.location = "name"


class AlphabetDoesNotExist(AlphabetException):
    def __init__(self, alphabet_id: UUID):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f"Alphabet {alphabet_id} does not exist."
        self.location = "alphabet_id"
