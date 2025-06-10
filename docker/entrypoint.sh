#!/bin/sh
set -e

# Apply database migrations
alembic upgrade head

# Run the application
exec uvicorn app.presentation.api:app --host 0.0.0.0 --port 8000