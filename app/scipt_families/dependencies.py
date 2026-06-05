from fastapi import Depends

from app.scipt_families.service import ScriptFamilyService
from app.db.session import get_async_session


async def get_script_family_service(session = Depends(get_async_session)):
    yield ScriptFamilyService(db_session=session)
