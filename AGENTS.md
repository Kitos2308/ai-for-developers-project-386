AGENT.md
# Booking Call Service

Минималистичный аналог Cal.com для записи на звонки.

## Stack

### Backend
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Redis
- Pydantic v2

### Frontend
- SvelteKit
- TypeScript
- TailwindCSS

---


## Layers

```text
Frontend
↓
API Layer
↓
Service Layer
↓
Repository Layer
↓
PostgreSQL
```

