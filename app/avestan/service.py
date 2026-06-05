import re
from typing import Dict, List, Tuple
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy import func

from app.db.models.alphabet import WrittingDirection
from app.db.models.character import AlphabetUnitType, Character
from app.exceptions import AlphabetBulkException
from app.avestan.exceptions import ImpossibleTransliteration, InvalidAlphabetCharacter
from app.db.models.transliteration_character import TransliterationCharacter


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
        """Method for transliteration of Avestan characters to Latin"""

        # Sanitze word
        word = self.sanitize(word=word)

        # Get Avestan alphabet with latin equivalents
        alphabet_with_trans: Tuple[str, str] = (
            await self.db_session.execute(
                select(Character.value, TransliterationCharacter.value)
                .join(TransliterationCharacter, TransliterationCharacter.character_id == Character.id)
                .where(Character.alphabet_id == alphabet_id, TransliterationCharacter.transliteration_system_id == transliteration_system_id)
        )).all()

        # Check if all characters are Avestan
        self.validate_characters(
            word=word,
            alphabet_characters=[c for c, _ in alphabet_with_trans],
            alphabet_name="Avestan",
            transliteration_system="X",
        )

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

        # Check if sequences occur in the provided string
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

    async def transliterate_latin_to_avestan(
        self,
        word: str,
        direction: WrittingDirection,
        alphabet_id: UUID,
        transliteration_system_id: UUID,
    ) -> str:
        """Method for transliteration of trans characters to Avestan"""

        # Sanitze word
        word = self.sanitize(word=word)

        # Get Avestan alphabet with latin equivalents
        alphabet_with_trans: Tuple[str, str] = (
            await self.db_session.execute(
                select(Character.value, TransliterationCharacter.value)
                .join(TransliterationCharacter, TransliterationCharacter.character_id == Character.id)
                .where(Character.alphabet_id == alphabet_id, TransliterationCharacter.transliteration_system_id == transliteration_system_id)
        )).all()

        # Check if all characters are trans characters
        self.validate_characters(
            word=word,
            alphabet_characters=[t for _, t in alphabet_with_trans],
            alphabet_name="Latin",
            transliteration_system="X",
        )

        # Flip word if it was written from Right to Left
        if direction == WrittingDirection.RTL:
            word = word[::-1]

        # Prepare transliteration dict
        transliteration_map: Dict[str, str] = {
            transliteration_value: character_value
            for character_value, transliteration_value in alphabet_with_trans
        }

        # Get trans sequences
        indexes_with_seq_length: Dict[int, int] = []
        trans_sequences: List[str] = (
            await self.db_session.execute(
                select(TransliterationCharacter.value)
                .where(
                    TransliterationCharacter.transliteration_system_id == transliteration_system_id,
                    func.length(TransliterationCharacter.value) > 1,
                )
        )).scalars().all()

        # Check if sequences occur in the provided string
        for seq in trans_sequences:
            seq_indexes: List[int] = [match.start() for match in re.finditer(re.escape(seq), word)]
            for seq_index in seq_indexes:
                indexes_with_seq_length[seq_index] = len(seq)

        # Transliterate
        transliterated: List[str] = []
        for i, c in enumerate(word):
            seq_start = 0
            seq_length = 0
            to_be_added = ""

            # If index is of sequence, add transliteration for whole sequnce
            if i in indexes_with_seq_length:
                seq_start = i
                seq_length = indexes_with_seq_length[i]
                char = f"{c}{word[i:i+seq_length]}"
                to_be_added = transliteration_map[char]
            # If index points to character in sequence, skip, as this symbol is already accounted for
            elif i in range(seq_start, seq_start + seq_length):
                pass
            # Else just add the symbol
            else:
                to_be_added = transliteration_map[c]

            # Append to final list
            transliterated.append(to_be_added)

        # Return as string
        return "".join([t for t in transliterated])

    def validate_characters(
        self,
        word: str,
        alphabet_characters: List[str],
        alphabet_name: str,
        transliteration_system: str,
    ) -> None:
        """Method for validating provided word"""

        if len(alphabet_characters) != len(set(alphabet_characters)):
            raise ImpossibleTransliteration(alphabet_name=alphabet_name, transliteration_system=transliteration_system)

        # Declare list for errors
        invalid_characters: List[InvalidAlphabetCharacter | None] = []

        # Check if each and every
        for i, c in enumerate(word):
            if c not in alphabet_characters:
                invalid_characters.append(InvalidAlphabetCharacter(value=c, index=i, alphabet_name=alphabet_name))

        if invalid_characters:
            raise AlphabetBulkException(status_code=status.HTTP_400_BAD_REQUEST, errors=invalid_characters)

    def sanitize(self, word: str) -> str:
        """Delete all whitespaces and special characters"""
        return ''.join(c for c in word if c.isalnum())
