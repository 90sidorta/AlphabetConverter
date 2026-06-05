from fastapi import Depends

from app.alphabets.service import AlphabetService
from app.db.session import get_async_session


async def get_alphabet_service(session = Depends(get_async_session)):
    yield AlphabetService(db_session=session)
