from typing import List, Optional
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select, Select, Result

from app.common import SortOrder
from app.scipt_families.schema import ScriptFamilySortBy
from app.db.models.script_family import ScriptFamily
from app.scipt_families.exceptions import DuplicatedScriptFamilyName, ScriptFamilyDoesNotExist


class ScriptFamilyService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, name: str) -> str:
        """Method for creation of Script Family"""

        # Create new row
        new_sf = ScriptFamily(name=name)
        # Add to session
        self.db_session.add(new_sf)
        # Save to db
        try:
            await self.db_session.commit()
        except IntegrityError:
            raise DuplicatedScriptFamilyName(name=name)

        return await self.read(script_family_id=new_sf.id)

    async def read(self, script_family_id: UUID) -> ScriptFamily:
        """Method to read Script Family"""

        # Try to get row from the db
        sf = await self.db_session.get(ScriptFamily, script_family_id)
        # If not found, raise exception
        if not sf:
            raise ScriptFamilyDoesNotExist(script_family_id=script_family_id)

        # Return row if found
        return sf

    async def read_list(
        self,
        limit: int = 20,
        offset: int = 0,
        sort_by: ScriptFamilySortBy = ScriptFamilySortBy.NAME,
        sort_order: SortOrder = SortOrder.ASCENDING,
        name: Optional[str | None] = None,
    ) -> str:
        """Method to list Script Families"""

        # Construct base query
        q: Select = select(ScriptFamily)

        # Include name in search if provided
        if name:
            q: Select = q.where(ScriptFamily.name.ilike(f"%{name}%"))

        # Apply order and sorting
        if sort_by == ScriptFamilySortBy.NAME:
            if sort_order == SortOrder.ASCENDING:
                q: Select = q.order_by(ScriptFamily.name.asc())
            else:
                q: Select = q.order_by(ScriptFamily.name.desc())
        elif sort_by == ScriptFamilySortBy.DATE_CREATED:
            if sort_order == SortOrder.ASCENDING:
                q: Select = q.order_by(ScriptFamily.date_created.asc())
            else:
                q: Select = q.order_by(ScriptFamily.date_created.desc())

        # Query to get all Script Families and to get paginated Script Families
        q_all: Select = q
        q_paginated: Select = q.limit(limit).offset(offset)

        # Get results
        result_all: Result = await self.db_session.execute(q_all)
        result_paginated: Result = await self.db_session.execute(q_paginated)

        # Convert results to list of ScriptFamily objects
        result_all: List[ScriptFamily] = result_all.scalars().all()
        result_paginated: List[ScriptFamily] = result_paginated.scalars().all()

        return result_paginated, len(result_all)

    async def update(self, script_family_id: UUID, name: str) -> str:
        """Method to update Script Family"""

        # Check if object exists
        sf = await self.read(script_family_id=script_family_id)

        # Update object
        sf.name = name

        # Save to db
        try:
            await self.db_session.commit()
        except IntegrityError:
            raise DuplicatedScriptFamilyName(name=name)

        return await self.read(script_family_id=script_family_id)


    async def delete(self, script_family_id: UUID) -> None:
        """Method to delete Script Family"""

        # Check if object exists
        sf = await self.read(script_family_id=script_family_id)

        # Delete object
        await self.db_session.delete(sf)
