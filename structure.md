# Структура проекта MotoKönig

## ✅ Выполненные задачи (Минимум готового)

### 1. Базовая архитектура и инфраструктура
- ✅ DDD + Clean Architecture структура
- ✅ FastAPI + Dishka DI container
- ✅ Advanced-Alchemy (SQLAlchemy 2) + Alembic
- ✅ Docker + Docker Compose + GitLab CI/CD
- ✅ Redis client и JWT токены с blacklist
- ✅ Базовые тесты (pytest + pytest-asyncio)

### 2. Аутентификация и пользователи
- ✅ JWT аутентификация с refresh токенами
- ✅ RBAC система (Admin, Operator, User)
- ✅ PIN-аутентификация для мобильных
- ✅ Регистрация (первый пользователь = админ)
- ✅ CRUD операции пользователей
- ✅ Middleware для проверки прав

## 🚀 Предстоящие задачи (Максимум работы)

### Фаза 1: Основные доменные сущности

#### 1.1 Motorcycle (Гараж) - ВЫСОКИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/motorcycle.py` - доменная сущность
- [ ] `app/domain/value_objects/` - Brand, Model, Year, EngineType
- [ ] `app/infrastructure/models/motorcycle_model.py` - SQLAlchemy модель
- [ ] `app/infrastructure/repositories/motorcycle_repo.py` - репозиторий
- [ ] `app/infrastructure/specifications/motorcycle_specs/` - спецификации поиска
- [ ] `app/application/use_cases/motorcycle/` - CRUD use cases
- [ ] `app/application/controllers/motorcycle_controller.py` - контроллер
- [ ] `app/presentation/schemas/motorcycle.py` - Pydantic схемы
- [ ] `app/presentation/routers/motorcycle.py` - API endpoints
- [ ] Миграция Alembic для таблицы motorcycles
- [ ] Связь Many-to-Many с User через промежуточную таблицу
- [ ] Тесты для всех слоев

#### 1.2 Profile (Расширенный профиль) - ВЫСОКИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/profile.py` - профиль пользователя
- [ ] `app/domain/value_objects/social_links.py` - VK, Telegram, WhatsApp
- [ ] Связь One-to-One с User
- [ ] Поля: bio, location, phone, social_links, avatar_url
- [ ] Настройки приватности (кто видит профиль, контакты)
- [ ] API для обновления профиля и настроек приватности

#### 1.3 MotoClub - ВЫСОКИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/moto_club.py` - сущность мотоклуба
- [ ] `app/domain/entities/club_membership.py` - членство в клубе
- [ ] `app/domain/entities/club_role.py` - роли в клубе
- [ ] Роли: President (создатель), Vice-President, Secretary, Member
- [ ] Кастомные роли с настраиваемыми правами
- [ ] Система приглашений и заявок на вступление
- [ ] Модерация контента клуба
- [ ] API для управления клубами и участниками

#### 1.4 Event - ВЫСОКИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/event.py` - события/мероприятия
- [ ] `app/domain/entities/event_participation.py` - участие в событиях
- [ ] `app/domain/value_objects/location.py` - геолокация
- [ ] Типы: публичные (от админов клубов), приватные (от пользователей)
- [ ] Поля: title, description, date_time, location, max_participants
- [ ] Регистрация на события, список участников
- [ ] Фильтры по дате, локации, типу события

### Фаза 2: Файловое хранилище и медиа

#### 2.1 MinIO интеграция - СРЕДНИЙ ПРИОРИТЕТ
- [ ] `app/infrastructure/storage/minio_client.py` - MinIO клиент
- [ ] `app/domain/ports/file_storage.py` - порт для хранилища
- [ ] `app/application/use_cases/media/` - use cases для файлов
- [ ] Buckets: avatars, motorcycles, events, posts
- [ ] Генерация presigned URLs для загрузки
- [ ] Автоматическая очистка неиспользуемых файлов

#### 2.2 Media Processing - СРЕДНИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/media_file.py` - сущность медиафайла
- [ ] `app/infrastructure/services/image_processor.py` - обработка изображений
- [ ] Ресайз и сжатие изображений (Pillow)
- [ ] Генерация превью разных размеров
- [ ] Водяные знаки для защиты контента
- [ ] Валидация форматов и размеров файлов

### Фаза 3: Геолокация и карты

#### 3.1 Points of Interest (POI) - СРЕДНИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/poi.py` - точки интереса
- [ ] `app/domain/entities/poi_rating.py` - рейтинги POI
- [ ] `app/domain/entities/poi_review.py` - отзывы о POI
- [ ] Типы POI: shop, service, attraction, gas_station, parking
- [ ] Геопоиск по радиусу
- [ ] Система модерации POI
- [ ] Рейтинги и отзывы с фото

#### 3.2 Routes - СРЕДНИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/route.py` - маршруты
- [ ] `app/domain/entities/route_point.py` - точки маршрута
- [ ] `app/domain/value_objects/gps_track.py` - GPS треки
- [ ] Импорт/экспорт GPX файлов
- [ ] Калькуляция расстояния и времени
- [ ] Шаринг маршрутов, лайки/дизлайки
- [ ] Комментарии к маршрутам

### Фаза 4: Социальные функции

#### 4.1 Friends System - НИЗКИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/friendship.py` - дружба
- [ ] `app/domain/entities/friend_request.py` - заявки в друзья
- [ ] `app/domain/entities/subscription.py` - подписки
- [ ] Статусы: pending, accepted, blocked
- [ ] Настройки приватности профиля
- [ ] Уведомления о заявках и принятии

#### 4.2 News Feed - НИЗКИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/post.py` - посты
- [ ] `app/domain/entities/comment.py` - комментарии
- [ ] `app/domain/entities/reaction.py` - реакции (лайки)
- [ ] Алгоритм формирования ленты
- [ ] Посты пользователей и клубов
- [ ] Уведомления о новых постах

### Фаза 5: Маркетплейс

#### 5.1 Marketplace - НИЗКИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/listing.py` - объявления
- [ ] `app/domain/entities/listing_category.py` - категории
- [ ] `app/domain/entities/listing_image.py` - фото объявлений
- [ ] Категории: motorcycles, parts, services, gear
- [ ] Фильтры и поиск по категориям
- [ ] Система модерации объявлений
- [ ] Избранное и сравнение

### Фаза 6: Расширенная функциональность

#### 6.1 Notifications System - СРЕДНИЙ ПРИОРИТЕТ
- [ ] `app/domain/entities/notification.py` - уведомления
- [ ] `app/infrastructure/messaging/` - RabbitMQ integration
- [ ] Push-уведомления для мобильных
- [ ] Email уведомления
- [ ] In-app уведомления
- [ ] Настройки типов уведомлений

#### 6.2 Search & Analytics - НИЗКИЙ ПРИОРИТЕТ
- [ ] Elasticsearch интеграция
- [ ] Полнотекстовый поиск
- [ ] Аналитика поведения пользователей
- [ ] Метрики использования функций
- [ ] A/B тестирование

#### 6.3 Mobile API Enhancements - СРЕДНИЙ ПРИОРИТЕТ
- [ ] Оптимизация API для мобильных
- [ ] Offline режим (синхронизация)
- [ ] Биометрическая аутентификация
- [ ] Геолокация в реальном времени
- [ ] Background sync для треков

### Фаза 7: Безопасность и производительность

#### 7.1 Advanced Security - ВЫСОКИЙ ПРИОРИТЕТ
- [ ] Rate limiting (Redis-based)
- [ ] CSRF protection
- [ ] Content Security Policy
- [ ] Аудит логирование действий
- [ ] 2FA аутентификация
- [ ] Детектирование подозрительной активности

#### 7.2 Performance & Monitoring - СРЕДНИЙ ПРИОРИТЕТ
- [ ] Redis кеширование запросов
- [ ] Database query optimization
- [ ] Background tasks (Celery/FastStream)
- [ ] Prometheus метрики
- [ ] Grafana дашборды
- [ ] Sentry для error tracking
- [ ] ELK stack для логов

### Фаза 8: DevOps и инфраструктура

#### 8.1 Production Infrastructure - СРЕДНИЙ ПРИОРИТЕТ
- [ ] Kubernetes манифесты
- [ ] Terraform для AWS инфраструктуры
- [ ] Auto-scaling настройки
- [ ] Load balancer configuration
- [ ] SSL сертификаты и домены
- [ ] Backup стратегия для данных

#### 8.2 Development Workflow - НИЗКИЙ ПРИОРИТЕТ
- [ ] Pre-commit hooks
- [ ] Automated testing в CI/CD
- [ ] Code coverage отчеты
- [ ] Dependabot для обновлений
- [ ] Staging environment
- [ ] Feature flags система

## 📱 Mobile Applications

### Android App - СРЕДНИЙ ПРИОРИТЕТ
- [ ] Kotlin/Compose нативное приложение
- [ ] PIN и биометрическая аутентификация
- [ ] Офлайн карты и навигация
- [ ] Push уведомления
- [ ] Камера для QR кодов
- [ ] GPS трекинг маршрутов

### iOS App - НИЗКИЙ ПРИОРИТЕТ
- [ ] SwiftUI нативное приложение
- [ ] Аналогичный функционал Android версии
- [ ] App Store публикация
- [ ] TestFlight бета тестирование

## 🌐 Frontend Web

### Nuxt 3 Application - СРЕДНИЙ ПРИОРИТЕТ
- [ ] Адаптивный дизайн (Tailwind CSS v4)
- [ ] PWA возможности
- [ ] SSR для SEO оптимизации
- [ ] Интерактивные карты
- [ ] Real-time чат
- [ ] Drag&drop загрузка файлов

## 📚 Documentation & Testing

- [ ] OpenAPI/Swagger автодокументация
- [ ] Postman коллекции для API
- [ ] Unit тесты (95% coverage)
- [ ] Integration тесты
- [ ] Load testing (Locust)
- [ ] E2E тесты для критических флоу
- [ ] Архитектурные диаграммы (C4 model)
- [ ] Пользовательская документация

---

**Следующие 3 задачи для немедленного выполнения:**
1. **Motorcycle entity** - основа для гаража пользователей
2. **Profile entity** - расширенные профили с социальными ссылками  
3. **MinIO integration** - хранилище для аватаров и фото мотоциклов