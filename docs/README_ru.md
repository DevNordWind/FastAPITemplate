<div align="center">

# FastAPITemplate

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-8.8-DC382D?logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[🇷🇺 Русский](docs/README_ru.md) | [🇬🇧 Английский](#)

</div>

---

## О проекте

FastAPITemplate - лёгкий шаблон FastAPI приложения с реализованной JWT-аутентификацией

---

## Стек:

- **Python:** 3.14
- **Библиотеки и фреймворки:** `FastAPI/Uvicorn`, `SQLAlchemy/Alembic`, `Adaptix`, `Dishka`,
- **Тестирование и разработки:** `pytest`, `pyrefly`, `ruff`
- **Прочие технологии:** `Redis 8`, `PostgreSQL 18`, `Docker/Docker Compose`

---

## Установка

Переименуйте `config_example.yaml` в `config.yaml` и заполните его, запуск с использованием docker:
```bash
make build && make up
```
Локально:
```bash
uv sync
uvicorn src.app.main.rest --factory
```