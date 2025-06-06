# Структура проекта MotoKönig

## ✅ Реализованные функции (Текущий статус)

### 1. Базовая архитектура и инфраструктура
- ✅ DDD + Clean Architecture структура проекта
- ✅ FastAPI + Dishka DI container для внедрения зависимостей
- ✅ Advanced-Alchemy (SQLAlchemy 2) + Alembic для работы с БД
- ✅ Docker + Docker Compose для разработки и деплоя
- ✅ GitLab CI/CD пайплайн с автоматическим деплоем на AWS EC2
- ✅ Redis для JWT blacklist, кеширования и PIN-кодов
- ✅ Базовые тесты с pytest + pytest-asyncio

### 2. Система аутентификации и авторизации
- ✅ JWT токены с access/refresh механизмом
- ✅ RBAC (Role-Based Access Control): Admin, Operator, User
- ✅ PIN-аутентификация для мобильных приложений
- ✅ Управление устройствами и их отзыв
- ✅ Blacklist токенов через Redis
- ✅ Middleware для проверки прав доступа
- ✅ Регистрация (первый пользователь автоматически становится админом)

### 3. Управление пользователями
- ✅ Полная CRUD система для пользователей
- ✅ Безопасное хеширование паролей (bcrypt)
- ✅ Валидация данных пользователей
- ✅ Деактивация/активация аккаунтов

### 4. Расширенные профили пользователей
- ✅ Детальные профили: биография, локация, телефон, дата рождения
- ✅ Опыт вождения мотоцикла в годах
- ✅ Система приватности с 4 уровнями (публичный, друзья, клубы, приватный)
- ✅ Отдельные настройки приватности для телефона и локации
- ✅ Социальные ссылки: VK, Telegram, WhatsApp, Instagram, Facebook, YouTube
- ✅ Валидация URL для каждой социальной платформы
- ✅ Управление видимостью социальных ссылок

### 5. Система гаража мотоциклов
- ✅ Полная CRUD система для мотоциклов
- ✅ Детальные характеристики: марка, модель, год, объем двигателя
- ✅ Типы двигателей: Inline 2/3/4, V-Twin, V4, Single, Boxer, Electric
- ✅ Типы мотоциклов: Sport, Naked, Touring, Cruiser, Adventure и др.
- ✅ Мощность, пробег, цвет, описание
- ✅ Система поиска и фильтрации мотоциклов
- ✅ Множественное владение (несколько мотоциклов у пользователя)
- ✅ Валидация данных мотоциклов (год, объем, мощность)

### 6. Файловое хранилище (MinIO)
- ✅ Интеграция с MinIO через aioboto3
- ✅ Система типов файлов: аватары, фото мотоциклов, документы, временные
- ✅ Валидация размеров и MIME типов для каждого типа файла
- ✅ Presigned URLs для безопасной загрузки/скачивания
- ✅ Автоматическая организация файлов по дате и владельцу
- ✅ Прямая загрузка файлов и загрузка через presigned URLs
- ✅ Полная интеграция с базой данных для отслеживания файлов
- ✅ Проверки владельца при доступе к файлам

### 7. Система мотоклубов - НОВОЕ! 🎉
- ✅ **Создание и управление мотоклубами**
  - Публичные и приватные клубы
  - Система ролей: President, Vice-President, Secretary, Treasurer, Event Organizer, Moderator, Senior Member, Member
  - Лимиты участников
  - Локация, описание, аватар, сайт клуба
- ✅ **Членство в клубах**
  - Автоматическое назначение президента при создании
  - Система статусов: active, suspended, banned
  - Права доступа для каждой роли
  - Повышение/понижение в ролях
- ✅ **Приглашения в клубы**
  - Персональные приглашения с сообщениями
  - Автоматическое истечение через 7 дней
  - Проверки лимитов и дублирования
  - Система accept/decline
- ✅ **API и права доступа**
  - Полный CRUD для клубов
  - Фильтрация по названию, локации, публичности
  - Проверки прав на редактирование/удаление
  - Валидация данных через Pydantic

### 8. API и документация
- ✅ RESTful API с автоматической OpenAPI документацией
- ✅ Версионирование API через заголовки
- ✅ Валидация запросов/ответов через Pydantic v2
- ✅ Обработка ошибок с детальными сообщениями
- ✅ CORS настройки для фронтенда

## 🚀 Приоритетные задачи для разработки

### Фаза 1: События и мероприятия - КРИТИЧЕСКИЙ ПРИОРИТЕТ

#### 1.1 Система событий
- [ ] `app/domain/entities/event.py` - мероприятия
- [ ] `app/domain/entities/event_participation.py` - участие в событиях
- [ ] `app/domain/value_objects/location.py` - геолокация с координатами
- [ ] Типы: публичные (от админов клубов), приватные (от пользователей)
- [ ] Регистрация на события с лимитами участников
- [ ] Фотографии событий через MinIO
- [ ] Фильтры по дате, локации, типу события

### Фаза 2: Карты и геолокация - ВЫСОКИЙ ПРИОРИТЕТ

#### 2.1 Points of Interest (POI)
- [ ] `app/domain/entities/poi.py` - точки интереса
- [ ] `app/domain/entities/poi_rating.py` - рейтинговая система
- [ ] `app/domain/entities/poi_review.py` - отзывы с фотографиями
- [ ] Типы POI: магазины, сервисы, заправки, достопримечательности
- [ ] Геопоиск по радиусу (требует PostGIS)
- [ ] Система модерации POI

#### 2.2 Планирование маршрутов
- [ ] `app/domain/entities/route.py` - маршруты
- [ ] `app/domain/entities/route_point.py` - точки маршрута
- [ ] `app/domain/value_objects/gps_track.py` - GPS треки
- [ ] Импорт/экспорт GPX файлов
- [ ] Расчет расстояния и времени
- [ ] Шаринг маршрутов с лайками/дизлайками

### Фаза 3: Медиа и контент - СРЕДНИЙ ПРИОРИТЕТ

#### 3.1 Расширенная обработка медиа
- [ ] `app/infrastructure/services/image_processor.py` - обработка изображений
- [ ] Автоматический ресайз и оптимизация изображений
- [ ] Генерация превью разных размеров
- [ ] Водяные знаки для защиты контента
- [ ] Поддержка видео для демонстрации мотоциклов

#### 3.2 Социальная лента
- [ ] `app/domain/entities/post.py` - посты пользователей и клубов
- [ ] `app/domain/entities/comment.py` - комментарии к постам
- [ ] `app/domain/entities/reaction.py` - лайки, дизлайки, эмоции
- [ ] Алгоритм формирования персональной ленты
- [ ] Модерация контента

### Фаза 4: Уведомления и коммуникации - СРЕДНИЙ ПРИОРИТЕТ

#### 4.1 Система уведомлений
- [ ] `app/domain/entities/notification.py` - уведомления
- [ ] `app/infrastructure/messaging/` - интеграция с RabbitMQ
- [ ] Push-уведомления для мобильных приложений
- [ ] Email уведомления для важных событий
- [ ] WebSocket для real-time уведомлений

### Фаза 5: Маркетплейс - НИЗКИЙ ПРИОРИТЕТ

#### 5.1 Торговая площадка
- [ ] `app/domain/entities/listing.py` - объявления о продаже
- [ ] `app/domain/entities/listing_category.py` - категории товаров
- [ ] Категории: мотоциклы, запчасти, экипировка, услуги
- [ ] Система модерации объявлений
- [ ] Фотографии товаров через MinIO

## 📱 Клиентские приложения

### Android приложение - ВЫСОКИЙ ПРИОРИТЕТ
- [ ] Kotlin/Compose нативное приложение
- [ ] PIN и биометрическая аутентификация
- [ ] Офлайн карты и GPS навигация
- [ ] Push уведомления
- [ ] GPS трекинг маршрутов

### Web фронтенд - СРЕДНИЙ ПРИОРИТЕТ
- [ ] Nuxt 3 + Tailwind CSS v4
- [ ] Интерактивные карты (Yandex Maps/OpenStreetMap)
- [ ] PWA для мобильных браузеров
- [ ] Real-time функции

## 🔧 Техническая инфраструктура

### Production готовность - ВЫСОКИЙ ПРИОРИТЕТ
- [ ] Мониторинг: Prometheus + Grafana
- [ ] Отслеживание ошибок: Sentry
- [ ] Rate limiting через Redis
- [ ] Логирование с ELK stack
- [ ] Automated backup стратегия

### База данных
- [ ] PostGIS для геолокационных запросов
- [ ] Оптимизация индексов
- [ ] Connection pooling

### Безопасность
- [ ] 2FA аутентификация
- [ ] CSRF protection
- [ ] Audit logging

---

**Критический путь к MVP (4-6 недель):**
1. **События** (2 недели) - ключевая функция для встреч мотоциклистов
2. **POI система** (2 недели) - каталог важных мест
3. **Базовые карты** (1 неделя) - отображение событий и POI
4. **Android приложение** (2 недели) - основной клиент

**Текущий прогресс:** 60% готовности к MVP. Завершена базовая инфраструктура и система мотоклубов!