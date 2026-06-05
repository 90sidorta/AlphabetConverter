from app.avestan.schema import WordTransliterated, TransliterateWord
from fastapi import APIRouter, Depends
from starlette import status

from app.errors import RouteErrorHandler
from app.exceptions import AlphabetBulkError
from app.avestan.dependencies import get_avestan_service
from app.avestan.service import AvestanService

avestan_router = APIRouter(route_class=RouteErrorHandler)


@avestan_router.post(
    "/avestan_to_latin",
    status_code=status.HTTP_200_OK,
    response_model=WordTransliterated,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": AlphabetBulkError},
        status.HTTP_404_NOT_FOUND: {"model": AlphabetBulkError},
    },
    summary="Transliterate from Avestan script to Latin",
)
async def avestan_to_latin(
    req: TransliterateWord,
    avestan_service: AvestanService = Depends(get_avestan_service),
) -> WordTransliterated:
    result = await avestan_service.transliterate_avestan_to_latin(
        word=req.word,
        direction=req.direction,
        alphabet_id=req.alphabet_id,
        transliteration_system_id=req.transliteration_system_id,
    )
    return WordTransliterated(transliterated=result)


@avestan_router.post(
    "/latin_to_avestan",
    status_code=status.HTTP_200_OK,
    response_model=WordTransliterated,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": AlphabetBulkError},
        status.HTTP_404_NOT_FOUND: {"model": AlphabetBulkError},
    },
    summary="Transliterate from Latin script to Avestan",
)
async def latin_to_avestan(
    req: TransliterateWord,
    avestan_service: AvestanService = Depends(get_avestan_service),
) -> WordTransliterated:
    result = await avestan_service.transliterate_latin_to_avestan(
        word=req.word,
        direction=req.direction,
        alphabet_id=req.alphabet_id,
        transliteration_system_id=req.transliteration_system_id,
    )
    return WordTransliterated(transliterated=result)
