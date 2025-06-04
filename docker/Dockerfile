# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
RUN pip install uv

# Копируем файлы зависимостей
COPY pyproject.toml .

# Устанавливаем зависимости
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e .

# Копируем код приложения
COPY . .

# Активируем venv и запускаем приложение
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.presentation.api:app", "--host", "0.0.0.0", "--port", "8000"]