# Структура проекта MotoKönig

## Текущие изменения

### 1. Переместить файлы:
```bash
# Создать новую структуру
mkdir -p app/infrastructure/messaging
mkdir -p app/domain/exceptions
mkdir -p app/application/services

# Переместить broker.py
mv app/infrastructure/broker.py app/infrastructure/messaging/broker.py
```

### 2. Создать новые файлы:

#### Порты (интерфейсы):
- `app/domain/ports/token_service.py` ✅

#### Сервисы инфраструктуры:
- `app/infrastructure/services/token_service.py` ✅
- `app/infrastructure/messaging/redis_client.py` ✅

#### Use Cases для аутентификации:
- `app/application/use_cases/auth/login.py` ✅
- `app/application/use_cases/auth/logout.py` ✅
- `app/application/use_cases/auth/refresh.py` ✅

#### Контроллеры:
- `app/application/controllers/auth_controller.py` ✅

#### Презентационный слой:
- `app/presentation/schemas/auth.py` ✅
- `app/presentation/routers/auth.py` ✅
- `app/presentation/middleware/auth.py` ✅

#### Тесты:
- `tests/test_auth_endpoints.py` ✅

### 3. Обновить файлы:
- `app/infrastructure/di/container.py` - добавить новые зависимости ✅
- `app/presentation/api.py` - добавить auth роутер и lifecycle ✅
- `app/presentation/routers/user.py` - добавить проверку прав ✅
- `pyproject.toml` - добавить pyjwt и redis ✅

## Следующие шаги разработки:

### 1. Сущность Motorcycle (Гараж):
- `app/domain/entities/motorcycle.py`
- `app/infrastructure/models/motorcycle_model.py`
- CRUD use cases для мотоциклов
- Связь many-to-many с User

### 2. Сущность MotoClub:
- Роли в клубе (президент, член, etc)
- Приглашения в клуб
- События клуба

### 3. Сущность Event:
- Публичные/приватные мероприятия
- Участники
- Геолокация

### 4. MinIO интеграция:
- `app/infrastructure/storage/minio_client.py`
- Use cases для загрузки фото
- Аватарки пользователей
- Фото мотоциклов

### 5. Карта и геолокация:
- Интеграция с картами
- Точки интереса (POI)
- Маршруты

## Команды для запуска:

```bash
# Установить зависимости
uv pip install -e .

# Запустить Redis (Docker)
docker run -d -p 6379:6379 redis:alpine

# Создать миграции
alembic revision --autogenerate -m "Add auth fields"
alembic upgrade head

# Запустить приложение
python -m app.main

# Запустить тесты
pytest tests/
```