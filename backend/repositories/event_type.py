import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.event_type import EventType


class EventTypeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_all(self) -> list[EventType]:
        result = await self.session.execute(select(EventType).order_by(EventType.title))
        return list(result.scalars().all())

    async def get_by_id(self, event_type_id: uuid.UUID) -> EventType | None:
        return await self.session.get(EventType, event_type_id)

    async def create(self, event_type: EventType) -> EventType:
        self.session.add(event_type)
        await self.session.flush()
        return event_type

    async def update(self, event_type: EventType, data: dict) -> EventType:
        for key, value in data.items():
            if value is not None:
                setattr(event_type, key, value)
        await self.session.flush()
        return event_type

    async def delete(self, event_type: EventType) -> None:
        await self.session.delete(event_type)
        await self.session.flush()

    async def has_bookings(self, event_type_id: uuid.UUID) -> bool:
        from models.booking import Booking
        result = await self.session.execute(
            select(Booking.id).where(Booking.event_type_id == event_type_id).limit(1)
        )
        return result.scalar_one_or_none() is not None