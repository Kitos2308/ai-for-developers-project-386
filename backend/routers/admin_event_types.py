import uuid

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_event_type_use_case
from schemas.event_type import EventTypeCreateRequest, EventTypeResponse, EventTypeUpdateRequest
from use_cases.event_type import EventTypeUseCase

router = APIRouter()


@router.get("", response_model=list[EventTypeResponse])
async def list_event_types(
    db: AsyncSession = Depends(get_db),
):
    use_case = get_event_type_use_case(db)
    result = await use_case.list_all()
    await db.commit()
    return result


@router.get("/{id}", response_model=EventTypeResponse)
async def get_event_type(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    use_case = get_event_type_use_case(db)
    result = await use_case.get_by_id(id)
    await db.commit()
    return result


@router.post("", response_model=EventTypeResponse, status_code=201)
async def create_event_type(
    body: EventTypeCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    use_case = get_event_type_use_case(db)
    result = await use_case.create(
        title=body.title,
        description=body.description,
        duration_minutes=body.duration_minutes,
    )
    await db.commit()
    return result


@router.put("/{id}", response_model=EventTypeResponse)
async def update_event_type(
    id: uuid.UUID,
    body: EventTypeUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    use_case = get_event_type_use_case(db)
    result = await use_case.update(
        event_type_id=id,
        title=body.title,
        description=body.description,
        duration_minutes=body.duration_minutes,
    )
    await db.commit()
    return result


@router.delete("/{id}", status_code=204)
async def delete_event_type(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    use_case = get_event_type_use_case(db)
    await use_case.delete(id)
    await db.commit()
    return Response(status_code=204)