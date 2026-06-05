from typing import List, Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select, Select, Result

from app.common import SortOrder
from app.alphabets.schema import AlphabetSortBy
from app.db.models.alphabet import Alphabet, WrittingDirection, WrittingSystem
from app.alphabets.exceptions import DuplicatedAlphabetName, AlphabetDoesNotExist
from app.scipt_families.service import ScriptFamilyService


class AlphabetService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.sf_service = ScriptFamilyService(db_session=db_session)

    async def create(
        self,
        name: str,
        script_family_id: UUID,
        writing_system: WrittingSystem = WrittingSystem.ALPHABET,
        writing_direction: WrittingDirection = WrittingDirection.LTR,
    ) -> Alphabet:
        """Method for creation of Alphabet"""

        # Check if ScriptFamily exists
        await self.sf_service.read(script_family_id=script_family_id)

        # Create new row
        new_alphabet = Alphabet(
            name=name,
            writting_system=writing_system,
            writting_direction=writing_direction,
            script_family_id=script_family_id,
        )

        # Add to session
        self.db_session.add(new_alphabet)

        # Save to db
        try:
            await self.db_session.commit()
        except IntegrityError:
            raise DuplicatedAlphabetName(name=name)

        return await self.read(alphabet_id=new_alphabet.id)

    async def read(self, alphabet_id: UUID) -> Alphabet:
        """Method to read Alphabet"""

        # Try to get row from the db
        alphabet = await self.db_session.get(Alphabet, alphabet_id)

        # If not found, raise exception
        if not alphabet:
            raise AlphabetDoesNotExist(alphabet_id=alphabet_id)

        # Return row if found
        return alphabet

    async def read_list(
        self,
        limit: int = 20,
        offset: int = 0,
        sort_by: AlphabetSortBy = AlphabetSortBy.NAME,
        sort_order: SortOrder = SortOrder.ASCENDING,
        name: Optional[str | None] = None,
        writing_system: Optional[WrittingSystem] = None,
        writing_direction: Optional[WrittingDirection] = None,
    ) -> tuple[List[Alphabet], int]:
        """Method to list Alphabets"""

        # Construct base query
        q: Select = select(Alphabet)

        # Include name in search if provided
        if name:
            q = q.where(Alphabet.name.ilike(f"%{name}%"))
        # Filter by writing_system if provided
        if writing_system:
            q = q.where(Alphabet.writing_system == writing_system)
        # Filter by writing_system if provided
        if writing_direction:
            q = q.where(Alphabet.writing_direction == writing_direction)

        # Apply order and sorting
        if sort_by == AlphabetSortBy.NAME:
            if sort_order == SortOrder.ASCENDING:
                q = q.order_by(Alphabet.name.asc())
            else:
                q = q.order_by(Alphabet.name.desc())
        elif sort_by == AlphabetSortBy.DATE_CREATED:
            if sort_order == SortOrder.ASCENDING:
                q = q.order_by(Alphabet.date_created.asc())
            else:
                q = q.order_by(Alphabet.date_created.desc())

        # Query to get all Alphabets and to get paginated Alphabets
        q_all: Select = q
        q_paginated: Select = q.limit(limit).offset(offset)

        # Get results
        result_all: Result = await self.db_session.execute(q_all)
        result_paginated: Result = await self.db_session.execute(q_paginated)

        # Convert results to list of Alphabet objects
        result_all: List[Alphabet] = result_all.scalars().all()
        result_paginated: List[Alphabet] = result_paginated.scalars().all()

        return result_paginated, len(result_all)

    async def update(
        self,
        alphabet_id: UUID,
        name: Optional[str | None] = None,
        script_family_id: Optional[UUID | None] = None,
        writing_system: Optional[WrittingSystem] = None,
        writing_direction: Optional[WrittingDirection] = None,
    ) -> Alphabet:
        """Method to update Alphabet"""

        # Check if object exists
        alphabet = await self.read(alphabet_id=alphabet_id)

        # If no updates, return the fetched object
        if not name and not writing_system and not writing_direction:
            return alphabet

        # Update object
        if script_family_id:
            alphabet.script_family_id = script_family_id
        if name:
            alphabet.name = name
        if writing_system:
            alphabet.writting_system = writing_system
        if writing_direction:
            alphabet.writting_direction = writing_direction

        # Save to db
        try:
            await self.db_session.commit()
        except IntegrityError:
            raise DuplicatedAlphabetName(name=name)

        return await self.read(alphabet_id=alphabet_id)

    async def delete(self, alphabet_id: UUID) -> None:
        """Method to delete Alphabet"""

        # Check if object exists
        alphabet = await self.read(alphabet_id=alphabet_id)

        # Delete object
        await self.db_session.delete(alphabet)
