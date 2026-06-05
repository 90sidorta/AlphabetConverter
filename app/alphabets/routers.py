from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.db.models.alphabet import WrittingDirection, WrittingSystem
from app.common import Pagination, SortOrder
from app.alphabets.service import AlphabetService
from app.alphabets.schema import (
    CreateAlphabet,
    ListAlphabet,
    ReadAlphabet,
    AlphabetSortBy,
    UpdateAlphabet,
)
from app.errors import RouteErrorHandler
from app.exceptions import AlphabetBulkError
from app.alphabets.dependencies import get_alphabet_service

alphabets_router = APIRouter(route_class=RouteErrorHandler)


@alphabets_router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ReadAlphabet,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": AlphabetBulkError},
        status.HTTP_404_NOT_FOUND: {"model": AlphabetBulkError},
        status.HTTP_409_CONFLICT: {"model": AlphabetBulkError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError},
    },
    summary="Create Alphabet",
)
async def create_alphabet(
    req: CreateAlphabet,
    alphabet_service: AlphabetService = Depends(get_alphabet_service),
) -> ReadAlphabet:
    result = await alphabet_service.create(
        script_family_id=req.script_family_id,
        name=req.name,
        writing_system=req.writing_system,
        writing_direction=req.writing_direction,
    )
    return ReadAlphabet(id=result.id, name=result.name)


@alphabets_router.get(
    "{alphabet_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReadAlphabet,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": AlphabetBulkError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError},
    },
    summary="Read Alphabet",
)
async def read_alphabet(
    alphabet_id: UUID,
    alphabet_service: AlphabetService = Depends(get_alphabet_service),
) -> ReadAlphabet:
    result = await alphabet_service.read(alphabet_id=alphabet_id)
    return ReadAlphabet(id=result.id, name=result.name)


@alphabets_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ListAlphabet,
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError}},
    summary="List Alphabets",
)
async def list_alphabet(
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    sort_by: AlphabetSortBy = AlphabetSortBy.NAME,
    sort_order: SortOrder = SortOrder.ASCENDING,
    name: Optional[str] = None,
    writing_system: Optional[WrittingSystem] = None,
    writing_direction: Optional[WrittingDirection] = None,
    alphabet_service: AlphabetService = Depends(get_alphabet_service),
) -> ListAlphabet:
    alphabets, total = await alphabet_service.read_list(
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
        name=name,
        writing_system=writing_system,
        writing_direction=writing_direction,
    )
    return ListAlphabet(
        data=[ReadAlphabet(**alphabet.__dict__) for alphabet in alphabets],
        pagination=Pagination(total_records=total, limit=limit, offset=offset),
        sort_by=sort_by,
        sort_order=sort_order,
        name=name,
        writing_system=writing_system,
        writing_direction=writing_direction,
    )


@alphabets_router.patch(
    "{alphabet_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReadAlphabet,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": AlphabetBulkError},
        status.HTTP_409_CONFLICT: {"model": AlphabetBulkError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError},
    },
    summary="Update Alphabet",
)
async def update_alphabet(
    alphabet_id: UUID,
    req: UpdateAlphabet,
    alphabet_service: AlphabetService = Depends(get_alphabet_service),
) -> ReadAlphabet:
    result = await alphabet_service.update(
        alphabet_id=alphabet_id,
        script_family_id=req.script_family_id,
        name=req.name,
        writing_system=req.writing_system,
        writing_direction=req.writing_direction,
    )
    return ReadAlphabet(id=result.id, name=result.name)


@alphabets_router.delete(
    "{alphabet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": AlphabetBulkError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError},
    },
    summary="Delete Alphabet",
)
async def delete_alphabet(
    alphabet_id: UUID,
    alphabet_service: AlphabetService = Depends(get_alphabet_service),
) -> None:
    await alphabet_service.delete(alphabet_id=alphabet_id)
    return None
