<div align="center">

# FastAPITemplate

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python\&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql\&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-8.8-DC382D?logo=redis\&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker\&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[🇷🇺 Russian](docs/README_ru.md) | [🇬🇧 English](#)

</div>

---

## About

FastAPITemplate is a lightweight FastAPI application template featuring JWT authentication out of the box.

---

## Tech Stack

* **Python:** 3.14
* **Libraries & Frameworks:** `FastAPI/Uvicorn`, `SQLAlchemy/Alembic`, `Adaptix`, `Dishka`
* **Development & Testing:** `pytest`, `pyrefly`, `ruff`
* **Infrastructure:** `Redis 8`, `PostgreSQL 18`, `Docker/Docker Compose`

---

## Installation

Rename `config_example.yaml` to `config.yaml` and fill in the required values.

### Using Docker

```bash
make build && make up
```

### Running Locally

```bash
uv sync
uvicorn src.app.main.rest --factory
```
