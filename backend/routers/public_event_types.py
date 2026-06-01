import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_booking_use_case, get_db, get_event_type_use_case
from schemas.event_type import EventTypeResponse
from schemas.slot import CalendarDaySlotsResponse, SlotResponse
from use_cases.booking import BookingUseCase
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


@router.get("/{eventTypeId}/slots", response_model=list[SlotResponse])
async def get_slots(
    eventTypeId: uuid.UUID,
    date: str,
    db: AsyncSession = Depends(get_db),
):
    use_case = get_booking_use_case(db)
    slots = await use_case.get_slots(eventTypeId, date)
    await db.commit()
    return slots


@router.get("/{eventTypeId}/calendar", response_model=list[CalendarDaySlotsResponse])
async def get_calendar(
    eventTypeId: uuid.UUID,
    month: int,
    year: int,
    db: AsyncSession = Depends(get_db),
):
    use_case = get_booking_use_case(db)
    result = await use_case.get_calendar(eventTypeId, month, year)
    await db.commit()
    return result