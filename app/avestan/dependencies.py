from fastapi import Depends

from app.avestan.service import AvestanService
from app.db.session import get_async_session


async def get_avestan_service(session = Depends(get_async_session)):
    yield AvestanService(db_session=session)
