SHELL := /bin/bash
DOCKER_COMPOSE := docker compose -f docker-compose.yml

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start
start: ## Start all docker containers
	$(DOCKER_COMPOSE) up -d --build --force-recreate
	PIPENV_VERBOSITY=-1 pipenv install

.PHONY: server-up
server-up: ## Startup the FastAPI server.
	PIPENV_VERBOSITY=-1 pipenv run uvicorn main:create_app --factory --reload --host 0.0.0.0

.PHONY: stop
stop: ## Stop project docker containers.
	$(DOCKER_COMPOSE) down --remove-orphans