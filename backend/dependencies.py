from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from clients.database import async_session
from repositories.booking import BookingRepository
from repositories.event_type import EventTypeRepository
from use_cases.booking import BookingUseCase
from use_cases.event_type import EventTypeUseCase


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


def get_event_type_use_case(session: AsyncSession) -> EventTypeUseCase:
    repo = EventTypeRepository(session)
    return EventTypeUseCase(repo)


def get_booking_use_case(session: AsyncSession) -> BookingUseCase:
    booking_repo = BookingRepository(session)
    event_type_repo = EventTypeRepository(session)
    return BookingUseCase(booking_repo, event_type_repo)