from uuid import UUID

from starlette import status

from app.exceptions import AlphabetException


class DuplicatedScriptFamilyName(AlphabetException):
    def __init__(self, name: str):
        self.status_code = status.HTTP_409_CONFLICT
        self.message = f"Script family {name} already exists."
        self.location = "name"


class ScriptFamilyDoesNotExist(AlphabetException):
    def __init__(self, script_family_id: UUID):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f"Script family {script_family_id} does not exist."
        self.location = "script_family_id"
