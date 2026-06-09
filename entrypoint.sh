#!/bin/sh
set -e

echo "Initializing PostgreSQL..."
PGDATA="${PGDATA:-/var/lib/postgresql/data}"

if [ ! -d "$PGDATA/base" ]; then
    mkdir -p "$PGDATA"
    chown postgres:postgres "$PGDATA"
    su - postgres -c "pg_ctl initdb -D '$PGDATA'"

    cat >> "$PGDATA/pg_hba.conf" <<EOF
local   all   all   md5
host    all   all   127.0.0.1/32   md5
EOF

    su - postgres -c "pg_ctl -D '$PGDATA' -l /tmp/pg.log -w start"
    su - postgres -c "psql -c \"ALTER USER postgres PASSWORD '${POSTGRES_PASSWORD}';\""
    su - postgres -c "createdb ${POSTGRES_DB}" 2>/dev/null || true
else
    su - postgres -c "pg_ctl -D '$PGDATA' -l /tmp/pg.log -w start"
fi

echo "Running migrations..."
cd /project/backend
alembic upgrade head

echo "Starting backend on port 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

echo "Starting frontend on port ${PORT:-3000}..."
cd /project/frontend
exec node build