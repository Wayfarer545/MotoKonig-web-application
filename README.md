# MotoKönig

## About

**MotoKönig** is a social network for motorcyclists in the Kaliningrad region. The app brings riders together on an interactive map, lets them share routes and events, and provides a marketplace for bikes, parts, and services. The codebase follows **DDD** and **Clean Architecture** principles.

> *Python 3.12 · Package manager — **uv** · Linter/formatter — **ruff***

---

[//]: # (## Repositories)

[//]: # ()
[//]: # (| Repository           | Purpose                                                                      |)

[//]: # (| -------------------- | ---------------------------------------------------------------------------- |)

[//]: # (| **motokonig-app**    | Main repository: FastAPI backend, OpenAPI docs, and web‑ui + docs submodules |)

[//]: # (| **motokonig-doc**    | Interactive project documentation served directly from the web interface     |)

[//]: # (| **motokonig-web-ui** | Nuxt 3 frontend, Caddy reverse‑proxy configuration, and static assets        |)

---

## Tech Stack

* ⚡ **FastAPI** + **Dishka** — asynchronous web server and DI container
* 🗄️ **Advanced‑Alchemy (SQLAlchemy 2)** — ORM for **PostgreSQL 16**
* 🔍 **Pydantic v2** — data validation and configuration
* ♻️ **Redis** — JWT blacklist and cache
* 💾 **MinIO** (via **aiobotocore**) — object storage for media files
* 🔑 Basic Auth + **JWT** with **RBAC**
* 🐰 **RabbitMQ** — task and event broker
* 💃 **Alembic** — database migrations
* 🎸 **UV** — dependency management
* 🐋 **Docker Compose v2** — development and production environments
* 🚢 **CI/CD** GitLab → **Amazon EC2**
* 🔒 Secure password hashing (**bcrypt**)
* ✅ Tests with **Pytest**
* 📞 **Caddy** — reverse proxy / load balancer
* 💅 **Nuxt 3** + **Tailwind CSS v4** — frontend

---

## API Versioning

All endpoints are versioned via the `X-Api-Version` header (`v1` by default).

---

## Core Features

* 🗺️ **Map** of shops, service centers, events, and POIs (Yandex Maps / OpenStreetMap)
* 🏍️ **Garage**: multiple motorcycles per user (brand, model, displacement, type, year)
* 🤝 **Friends & Moto Clubs** with roles (president + custom)
* 📅 **User events** (visible to followers) and public club events
* 🔗 Social links (VK, WhatsApp, Telegram) if the user allows
* 🛣️ **Route planning & sharing** with like/dislike
* ⭐ **Ratings** for services / shops / places
* 📰 **News feed** for the community and clubs
* 🛒 **Marketplace** for motorcycles, parts, and services

---

[//]: # (## Local Development Docs)

[//]: # ()
[//]: # (* **Backend**: [./docs/deployment.md]&#40;./docs/deployment.md&#41;)

[//]: # (* **Frontend**: [motokonig-web-ui/README.md]&#40;../motokonig-web-ui/README.md&#41;)

> Missing something? Feel free to open an Issue or submit a Pull Request! :)


