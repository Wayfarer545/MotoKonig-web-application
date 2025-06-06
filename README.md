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
* 🚢 **CI/CD** GitLab → **Amazon EC2**
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

---

## Core Features (Roadmap) 🚀

* 🗺️ **Map** of shops, service centers, events, and POIs
* 🏍️ **Garage**: multiple motorcycles per user
* 🤝 **Friends & Moto Clubs** with custom roles
* 📅 **Events** (public/private)
* 🔗 Social links integration
* 🛣️ **Route planning & sharing**
* ⭐ **Ratings** for services/shops/places
* 📰 **News feed**
* 🛒 **Marketplace**

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
  docker-compose up -d postgres redis
```
5. Run migrations:
```bash
  alembic upgrade head
```
6. Start the server:
```bash
  uv run app.main:app
```

The API will be available at http://localhost:8000
___

### API Documentation
Once the server is running, you can access:
___
Swagger UI: http://localhost:8000/openapi
OpenAPI JSON: http://localhost:8000/openapi.json
___

### Testing  
Run tests with coverage:
```bash
  pytest tests/ -v --cov=app --cov-report=html
```

### Logging
The project uses **structlog** with Loguru to produce JSON logs. Contextual
information like request ID and authenticated user ID is automatically bound via
middleware and helper functions.

Example usage:

```python
import structlog

log = structlog.get_logger()

log.info("user_login", user_id=user.id)
```

### Deployment
The project includes GitLab CI/CD configuration for automated deployment to AWS EC2.  
See .gitlab-ci.yml for pipeline details.

### Project Structure  
The project follows Domain-Driven Design and Clean Architecture:

<pre>
app/  
├── domain/          # Business logic and entities  
├── application/     # Use cases and controllers  
├── infrastructure/  # External services implementation  
├── adapters/        # Interface adapters  
├── presentation/    # API layer  
└── config/          # Configuration
</pre>

See structure.md for detailed structure.

### License  
This project is licensed under the MIT License - see the LICENSE file for details.