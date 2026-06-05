from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.common import Pagination, SortOrder
from app.scipt_families.service import ScriptFamilyService
from app.scipt_families.schema import (
    CreateScriptFamily,
    ListScriptFamily,
    ReadScriptFamily,
    ScriptFamilySortBy,
    UpdateScriptFamily,
)
from app.errors import RouteErrorHandler
from app.exceptions import AlphabetBulkError
from app.scipt_families.dependencies import get_script_family_service

script_families_router = APIRouter(route_class=RouteErrorHandler)


@script_families_router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ReadScriptFamily,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": AlphabetBulkError},
        status.HTTP_409_CONFLICT: {"model": AlphabetBulkError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError},
    },
    summary="Create Script Family",
)
async def create_script_family(
    req: CreateScriptFamily, sf_service: ScriptFamilyService = Depends(get_script_family_service),
) -> ReadScriptFamily:
    result = await sf_service.create(name=req.name)
    return ReadScriptFamily(id=result.id, name=result.name)


@script_families_router.get(
    "{script_family_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReadScriptFamily,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": AlphabetBulkError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError},
    },
    summary="Read Script Family",
)
async def read_script_family(
    script_family_id: UUID, sf_service: ScriptFamilyService = Depends(get_script_family_service),
) -> ReadScriptFamily:
    result = await sf_service.read(script_family_id=script_family_id)
    return ReadScriptFamily(id=result.id, name=result.name)


@script_families_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ListScriptFamily,
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError}},
    summary="List Script Families",
)
async def list_script_family(
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    sort_by: ScriptFamilySortBy = ScriptFamilySortBy.NAME,
    sort_order: SortOrder = SortOrder.ASCENDING,
    name: Optional[str] = None,
    sf_service: ScriptFamilyService = Depends(get_script_family_service),
) -> ListScriptFamily:
    script_families, total = await sf_service.read_list(
        limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order, name=name,
    )
    return ListScriptFamily(
        data=[ReadScriptFamily(**sf.__dict__) for sf in script_families],
        pagination=Pagination(total_records=total, limit=limit, offset=offset),
        sort_by=sort_by,
        sort_order=sort_order,
        name=name,
    )


@script_families_router.patch(
    "{script_family_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReadScriptFamily,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": AlphabetBulkError},
        status.HTTP_409_CONFLICT: {"model": AlphabetBulkError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError},
    },
    summary="Update Script Family",
)
async def update_script_family(
    script_family_id: UUID,
    req: UpdateScriptFamily,
    sf_service: ScriptFamilyService = Depends(get_script_family_service),
) -> ReadScriptFamily:
    result = await sf_service.update(script_family_id=script_family_id, name=req.name)
    return ReadScriptFamily(id=result.id, name=result.name)


@script_families_router.delete(
    "{script_family_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": AlphabetBulkError},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": AlphabetBulkError},
    },
    summary="Delete Script Family",
)
async def delete_script_family(
    script_family_id: UUID,
    sf_service: ScriptFamilyService = Depends(get_script_family_service),
) -> None:
    await sf_service.delete(script_family_id=script_family_id)
    return None
