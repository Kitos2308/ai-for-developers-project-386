import uuid

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_booking_use_case, get_db
from schemas.booking import BookingResponse, UpdateBookingRequest
from use_cases.booking import BookingUseCase

router = APIRouter()


@router.get("", response_model=list[BookingResponse])
async def list_bookings(
    db: AsyncSession = Depends(get_db),
):
    use_case = get_booking_use_case(db)
    result = await use_case.list_all()
    await db.commit()
    return result


@router.patch("/{id}", response_model=BookingResponse)
async def update_booking(
    id: uuid.UUID,
    body: UpdateBookingRequest,
    db: AsyncSession = Depends(get_db),
):
    use_case = get_booking_use_case(db)
    result = await use_case.update(
        booking_id=id,
        guest_name=body.guest_name,
        guest_email=body.guest_email,
        notes=body.notes,
    )
    await db.commit()
    return result


@router.delete("/{id}", status_code=204)
async def delete_booking(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    use_case = get_booking_use_case(db)
    await use_case.delete(id)
    await db.commit()
    return Response(status_code=204)