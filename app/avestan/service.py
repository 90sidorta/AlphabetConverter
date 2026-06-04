import re
from typing import Dict, List, Tuple
from uuid import UUID

from app.avestan.exceptions import InvalidAvestanCharacter
from app.db.models.transliteration_character import TransliterationCharacter
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from starlette import status

from app.db.models.alphabet import WrittingDirection
from app.db.models.character import AlphabetUnitType, Character
from app.exceptions import AlphabetBulkException


class AvestanService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def transliterate_avestan_to_latin(
        self,
        word: str,
        direction: WrittingDirection,
        alphabet_id: UUID,
        transliteration_system_id: UUID,
    ) -> str:
        """Method for transliteration of avestan characters to latin"""

        # Get Avestan alphabet with latin equivalents
        alphabet_with_trans: Tuple[str, str] = (
            await self.db_session.execute(
                select(Character.value, TransliterationCharacter.value)
                .join(TransliterationCharacter, TransliterationCharacter.character_id == Character.id)
                .where(Character.alphabet_id == alphabet_id, TransliterationCharacter.transliteration_system_id == transliteration_system_id)
        )).all()

        # Check if all characters are Avestan
        self.validate_characters(word=word, avestan_alphabet=[c for c, _ in alphabet_with_trans])

        # Flip word if it was written from Left to Right
        if direction == WrittingDirection.RTL:
            word = word[::-1]

        # Prepare transliteration dict
        transliteration_map: Dict[str, str] = {
            character_value: transliteration_value
            for character_value, transliteration_value in alphabet_with_trans
        }

        # Get avestan sequences
        sequence_indexes: List[int | None] = []
        avestan_sequences: List[str] = (
            await self.db_session.execute(
                select(Character.value)
                .where(Character.alphabet_id == alphabet_id, Character.unit_type == AlphabetUnitType.SEQUENCE)
        )).scalars().all()

        # Check if sequences occur in the provided strin
        for seq in avestan_sequences:
            sequence_indexes.extend([match.start() for match in re.finditer(re.escape(seq), word)])

        # Transliterate
        transliterated: List[str] = []
        for i, c in enumerate(word):
            to_be_added = ""

            # If index is of sequence, add transliteration for whole sequnce
            if i in sequence_indexes:
                char = f"{c}{word[i+1]}"
                to_be_added = transliteration_map[char]
            # If index - 1 is of sequence, skip, as this symbol is already accounted for
            elif i - 1 in sequence_indexes:
                pass
            # Else just add the symbol
            else:
                to_be_added = transliteration_map[c]

            # Append to final list
            transliterated.append(to_be_added)

        # Return as string
        return "".join([t for t in transliterated])

    def validate_characters(self, word: str, avestan_alphabet = List[str]) -> None:
        """Method for validating provided word"""

        # Declare list for errors
        invalid_characters: List[InvalidAvestanCharacter | None] = []

        # Check if each and every
        for i, c in enumerate(word):
            if c not in avestan_alphabet:
                invalid_characters.append(InvalidAvestanCharacter(value=c, index=i))

        if invalid_characters:
            raise AlphabetBulkException(status_code=status.HTTP_400_BAD_REQUEST, errors=invalid_characters)
