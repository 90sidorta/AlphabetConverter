from starlette import status

from app.exceptions import AlphabetException
from app.db.models.alphabet import WrittingDirection


class InvalidAlphabetCharacter(AlphabetException):
    def __init__(self, value: str, index: int, alphabet_name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"{value} is not a valid {alphabet_name} character."
        self.location = f"{index}"


class InvalidAlphabetDirection(AlphabetException):
    def __init__(self, direction: WrittingDirection):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"{direction.value} is not a valid writing direction for this alphabet."
        self.location = "direction"


class ImpossibleTransliteration(AlphabetException):
    def __init__(self, transliteration_system: str, alphabet_name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"Impossible to transliterate from {alphabet_name} with transliteration system {transliteration_system}."
        self.location = "transliteration_system_id"
