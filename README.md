# MotoKönig

**MotoKönig** is a social network for motorcyclists in the Kaliningrad region. The app brings riders together on an interactive map, lets them share routes and events, and provides a marketplace for bikes, parts, and services. The codebase follows **DDD** and **Clean Architecture** principles.

> *Python 3.12 · Package manager — **uv** · Linter/formatter — **ruff***

---

## Tech Stack

* ⚡ **FastAPI** + **Dishka** — asynchronous web server and DI container
* 🗄️ **Advanced‑Alchemy (SQLAlchemy 2)** — ORM for **PostgreSQL 16**
* 🔍 **Pydantic v2** — data validation and configuration
* ♻️ **Redis** — JWT blacklist, cache, and PIN storage
* 💾 **MinIO** (via **aiobotocore**) — object storage for media files
* 🔑 JWT Authentication with **RBAC** + PIN auth for mobile
* 🐰 **RabbitMQ** — task and event broker
* 💃 **Alembic** — database migrations
* 🎸 **UV** — dependency management
* 🐋 **Docker Compose v2** — development and production environments
* 🔒 Secure password hashing (**bcrypt**)
* ✅ Tests with **Pytest**
* 📞 **Caddy** — reverse proxy / load balancer
* 💅 **Nuxt 3** + **Tailwind CSS v4** — frontend

---

## API Versioning

All endpoints are versioned via the `X-Api-Version` header (`v1` by default).

---

## Current Features ✅

### Authentication & Authorization
- User registration (first user becomes admin)
- JWT authentication with refresh tokens
- Role-based access control (Admin, Operator, User)
- PIN authentication for mobile apps
- Token blacklisting
- Device management

### User Management
- Full CRUD operations
- Profile updates
- User deactivation
- Password management

### Extended User Profiles
- Detailed profiles: bio, location, phone, date of birth
- Riding experience tracking
- 4-level privacy system (public, friends, clubs, private)
- Separate privacy settings for phone and location
- Social links: VK, Telegram, WhatsApp, Instagram, Facebook, YouTube
- URL validation for each social platform
- Social link visibility management

### Garage System
- Full motorcycle CRUD operations
- Detailed specifications: brand, model, year, engine volume
- Engine types: Inline 2/3/4, V-Twin, V4, Single, Boxer, Electric
- Motorcycle types: Sport, Naked, Touring, Cruiser, Adventure, etc.
- Power, mileage, color, description tracking
- Advanced search and filtering system
- Multiple motorcycles per user
- Data validation (year, volume, power)

### MotoClubs System
- **Club Management**
  - Public and private clubs
  - Role hierarchy: President, Vice-President, Secretary, Treasurer, Event Organizer, Moderator, Senior Member, Member
  - Member limits and location tracking
  - Club avatars, descriptions, websites
- **Membership System**
  - Automatic president assignment on creation
  - Status management: active, suspended, banned
  - Role-based permissions
  - Promotion/demotion system
- **Invitation System**
  - Personal invitations with messages
  - Auto-expiry after 7 days
  - Duplicate and limit checking
  - Accept/decline workflow
- **Full API with Filtering**
  - Complete CRUD operations
  - Search by name, location, visibility
  - Permission checks for edit/delete
  - Pydantic validation

### Routes System 🆕
- **Route Management**
  - GPS-based route creation with waypoints
  - Route types: scenic, sport, touring, offroad, mixed
  - Difficulty levels: easy, medium, hard, extreme
  - Status workflow: draft → published → archived
  - Distance, duration, and elevation tracking
- **Social Features**
  - Route rating system (1-5 stars)
  - Comments and reviews
  - View and save counters
  - Average rating calculation
- **Advanced Search**
  - Filter by type, difficulty, distance, rating
  - Text search in names and descriptions
  - Sorting by multiple criteria
  - Pagination support

### File Storage (MinIO)
- MinIO integration via aioboto3
- File type system: avatars, motorcycle photos, documents, temp files
- Size and MIME type validation per file type
- Presigned URLs for secure upload/download
- Automatic file organization by date and owner
- Direct upload and presigned URL upload methods
- Full database integration for file tracking
- Owner access verification

---

## Core Features (Roadmap) 🚀

* 🗺️ **Map** of shops, service centers, events, and POIs
* 🤝 **Events System** - public/private motorcycle meetups
* 📍 **Points of Interest** - ratings and reviews for locations
* 🛣️ **Route Import/Export** - GPX file support
* 📰 **Social Feed** - posts, comments, reactions
* 💬 **Real-time Notifications** - WebSocket + Push
* 🛒 **Marketplace** - buy/sell bikes, parts, gear

---

## Quick Start

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- Redis
- PostgreSQL (or use Docker)

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/motokonig.git && cd motokonig
```

2. Install dependencies:
```bash
pip install uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

3. Configure environment variables:
```bash
cp .env.example .env
```
Edit .env with your settings

4. Start services:
```bash
docker-compose up -d postgres redis minio
```

5. Run migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uv run uvicorn app.presentation.api:app --reload
```

The API will be available at http://localhost:8000

### MinIO Setup
MinIO will be available at:
- **Console**: http://localhost:9001 (admin/admin123)
- **API**: http://localhost:9000

The application will automatically create required buckets on startup.

---

### API Documentation
Once the server is running, you can access:

**Swagger UI**: http://localhost:8000/openapi  
**OpenAPI JSON**: http://localhost:8000/openapi.json

### Available Endpoints

#### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - Login with Basic Auth
- `POST /auth/logout` - Logout
- `POST /auth/refresh` - Refresh tokens
- `GET /auth/me` - Current user info
- `POST /auth/setup-pin` - Setup PIN for mobile
- `POST /auth/pin-login` - Login with PIN

#### Users
- `GET /users/` - List users (Admin/Operator)
- `POST /users/` - Create user (Admin)
- `GET /users/{id}` - Get user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user (Admin)

#### Profiles
- `POST /profile/` - Create profile
- `GET /profile/my` - Get own profile
- `PUT /profile/my` - Update own profile
- `GET /profile/{id}` - Get profile by ID
- Social links management endpoints

#### Motorcycles
- `GET /motorcycle/` - Search motorcycles
- `POST /motorcycle/` - Create motorcycle
- `GET /motorcycle/my` - Get own motorcycles
- `GET /motorcycle/{id}` - Get motorcycle
- `PUT /motorcycle/{id}` - Update motorcycle
- `DELETE /motorcycle/{id}` - Delete motorcycle

#### MotoClubs
- `GET /moto-clubs/` - List clubs (with filtering)
- `POST /moto-clubs/` - Create club
- `GET /moto-clubs/{id}` - Get club details
- `PUT /moto-clubs/{id}` - Update club
- `DELETE /moto-clubs/{id}` - Delete club
- `POST /moto-clubs/{id}/join` - Join club
- `POST /moto-clubs/{id}/invite` - Invite user

#### Routes 🆕
- `GET /routes/` - List routes (with filtering)
- `POST /routes/` - Create route
- `GET /routes/{id}` - Get route details
- `PUT /routes/{id}` - Update route
- `POST /routes/{id}/publish` - Publish route
- `POST /routes/{id}/rate` - Rate route

#### Media
- `POST /media/upload` - Direct file upload
- `POST /media/upload-url` - Get presigned upload URL
- `POST /media/download-url` - Get presigned download URL
- `DELETE /media/` - Delete file

---

### Testing  
Run tests with coverage:
```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Deployment
The project includes GitLab CI/CD configuration for automated deployment to AWS EC2.  
See .gitlab-ci.yml for pipeline details.

### Project Structure  
The project follows Domain-Driven Design and Clean Architecture:

```
app/  
├── domain/          # Business logic and entities  
│   ├── entities/    # Domain entities
│   └── value_objects/ # Value objects
├── application/     # Use cases and interfaces
│   ├── dto/         # Data Transfer Objects
│   ├── interfaces/  # Repository interfaces
│   ├── use_cases/   # Business use cases
│   └── di/          # Use case providers
├── infrastructure/  # External services implementation  
│   ├── repositories/ # Repository implementations
│   ├── services/    # External services (MinIO, Redis)
│   ├── persistence/ # Database models (SQLAlchemy)
│   └── di/         # Infrastructure providers
├── presentation/    # API layer (routers, schemas)
│   ├── api/        # FastAPI controllers
│   ├── schemas/    # Pydantic schemas
│   └── middlewares/ # Middleware components
└── config/         # Configuration
```

See structure.md for detailed structure and development roadmap.

### License  
This project is licensed under the MIT License - see the LICENSE file for details.