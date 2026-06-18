COMPOSE = docker compose -f ./deployment/docker-compose.yml

.PHONY: build
build:
	$(COMPOSE) build

.PHONY: up
up:
	$(COMPOSE)  up -d

.PHONY: up-build
up-build:
	$(COMPOSE)  up -d --build

.PHONY: down
down:
	$(COMPOSE) down

.PHONY: down-v
down-v:
	$(COMPOSE) down -v

.PHONY: restart
restart:
	$(COMPOSE) restart


.PHONY: migrate
migrate:
	$(COMPOSE)  run --rm migrations

.PHONY: migration
migration:
	$(COMPOSE)  run --rm migrations uv run alembic revision --autogenerate -m "$(MSG)"

.PHONY: logs
logs:
	$(COMPOSE) logs -f

.PHONY: logs-rest
logs-rest:
	$(COMPOSE) logs -f rest

.PHONY: logs-db
logs-db:
	$(COMPOSE) logs -f postgres

.PHONY: logs-redis
logs-redis:
	$(COMPOSE) logs -f redis

.PHONY: shell-rest
shell-rest:
	$(COMPOSE) exec rest sh

.PHONY: shell-db
shell-db:
	$(COMPOSE) exec postgres psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}

.PHONY: shell-redis
shell-redis:
	$(COMPOSE) exec redis redis-cli -a $${REDIS_PASSWORD}

.PHONY: ps
ps:
	$(COMPOSE) ps

.PHONY: clean
clean:
	docker container prune -f
	docker image prune -f

.PHONY: clean-all
clean-all:
	$(COMPOSE) down -v --rmi all --remove-orphans
	docker system prune -f

check:
	ruff check --fix
	ruff format
	typos
	tombi format
	tombi lint
	pyrefly check src/
	pytest -v

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
