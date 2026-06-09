#!/bin/sh
set -e

echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "!!! VITE_API_URL = ${VITE_API_URL:-<not set>}"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "Starting frontend..."
exec make start