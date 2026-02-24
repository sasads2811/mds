export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up upgrade-head test

build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans --volumes

test:
	docker compose build tests && docker compose run --rm tests

logs:
	docker compose logs --tail=25 api

migration:
	alembic revision --autogenerate -m '${m}'

upgrade-head:
	@echo "Waiting 5 seconds before running Alembic..."
	@sleep 5
	alembic upgrade head



