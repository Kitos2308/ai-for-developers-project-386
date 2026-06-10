#!/bin/sh
set -e

PGDATA="${PGDATA:-/var/lib/postgresql/data}"

echo "Initializing PostgreSQL..."
if [ ! -d "$PGDATA/base" ]; then
    mkdir -p "$PGDATA"
    chown postgres:postgres "$PGDATA"
    su -s /bin/sh postgres -c "pg_ctl initdb -D '$PGDATA'"

    cat >> "$PGDATA/pg_hba.conf" <<EOF
local   all   all   md5
host    all   all   127.0.0.1/32   md5
EOF

    su -s /bin/sh postgres -c "pg_ctl -D '$PGDATA' -l /tmp/pg.log -w start"
    su -s /bin/sh postgres -c "psql -c \"ALTER USER postgres PASSWORD '${POSTGRES_PASSWORD}';\""
    su -s /bin/sh postgres -c "createdb ${POSTGRES_DB}" 2>/dev/null || true
else
    su -s /bin/sh postgres -c "pg_ctl -D '$PGDATA' -l /tmp/pg.log -w start"
fi

echo "Running migrations..."
cd /project/backend
alembic upgrade head

echo "Starting backend on port 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

echo "Starting frontend on port ${PORT:-3000}..."
cd /project/frontend
exec node build