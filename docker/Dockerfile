# Dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv
COPY pyproject.toml .
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e .

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

COPY docker/entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
