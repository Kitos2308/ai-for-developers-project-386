#!/bin/sh
set -e

echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "!!! VITE_API_URL = ${VITE_API_URL:-<not set>}"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

# Replace __API_URL__ placeholder in built JS files with the runtime VITE_API_URL value.
# At build time (no .env), import.meta.env.VITE_API_URL resolves to undefined,
# so the fallback '__API_URL__' remains as a string literal in the output.
# At container start we swap it for the real URL from the environment.
API_URL="${VITE_API_URL:-}"
if [ -n "$API_URL" ]; then
    echo "Injecting API_URL: $API_URL"
    find /project/frontend/build -name '*.js' -exec sed -i "s|__API_URL__|${API_URL}|g" {} +
fi

echo "Starting frontend..."
exec make start
