#!/usr/bin/env bash
# Wait until PostgreSQL accepts connections.
set -euo pipefail

HOST="${AIMA_DB_HOST:-localhost}"
PORT="${AIMA_DB_PORT:-5432}"
USER="${AIMA_DB_USER:-aima}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-30}"

echo "Waiting for PostgreSQL at ${HOST}:${PORT}..."

for i in $(seq 1 "${MAX_ATTEMPTS}"); do
  if pg_isready -h "${HOST}" -p "${PORT}" -U "${USER}" >/dev/null 2>&1; then
    echo "PostgreSQL is ready."
    exit 0
  fi
  # Fallback without pg_isready: TCP probe
  if (echo >/dev/tcp/"${HOST}"/"${PORT}") >/dev/null 2>&1; then
    echo "PostgreSQL port is open (attempt ${i})."
    sleep 1
    echo "Assuming ready."
    exit 0
  fi
  echo "  attempt ${i}/${MAX_ATTEMPTS}..."
  sleep 1
done

echo "PostgreSQL did not become ready in time." >&2
exit 1
