from app.db.models.alphabet import WrittingDirection
from starlette import status

from app.exceptions import AlphabetException


class InvalidAvestanCharacter(AlphabetException):
    def __init__(self, value: str, index: int):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"{value} is not a valid Avestan character."
        self.location = f"{index}"


class InvalidAvestanDirection(AlphabetException):
    def __init__(self, direction: WrittingDirection):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"{direction.value} is not a valid Avestan writing direction."
        self.location = "direction"
