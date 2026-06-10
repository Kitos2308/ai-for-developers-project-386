FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

FROM python:3.12-slim AS backend-builder
ENV POETRY_VERSION=2.1.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_HOME=/opt/poetry
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /app
COPY backend/pyproject.toml backend/poetry.lock ./
RUN poetry install --no-root --only main

FROM python:3.12-slim AS runner

RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    postgresql \
    && ln -sf /usr/lib/postgresql/15/bin/* /usr/local/bin/ \
    && rm -rf /var/lib/apt/lists/*

COPY --from=node:20-slim /usr/local/bin/node /usr/local/bin/node

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PGDATA=/var/lib/postgresql/data \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=postgres \
    POSTGRES_DB=minical \
    DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/minical

COPY --from=backend-builder /app/.venv /app/.venv

WORKDIR /project
COPY --from=frontend-builder /app/build ./frontend/build
COPY --from=frontend-builder /app/.svelte-kit ./frontend/.svelte-kit
COPY --from=frontend-builder /app/node_modules ./frontend/node_modules
COPY frontend/package.json ./frontend/

COPY backend ./backend
COPY Makefile .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV PORT=3000
EXPOSE 3000

ENTRYPOINT ["./entrypoint.sh"]