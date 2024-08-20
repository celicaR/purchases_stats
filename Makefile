default: help
SHELL := /usr/bin/env bash

# set default env variables
export pytest?=true
export parameter?=run_parameters

include .env

#.PHONY: build lint format test run run_airflow dbt_run
.PHONY: verification test build run delete

.PHONY: help
help: #\t🆘 Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: setup
setup: # 🔧 Install python packages required for local development
	@echo "Installing python packages required for local development"
	@./scripts/py_env_setup.sh

.PHONY: build
build: #\t🔨 Build the docker images.
	@echo "🔨 Building the docker images"
	docker-compose build

.PHONY: run_all
run_all: #\t🏃 Run all Docker images and containers.
	@echo "🏃 Run all Docker images and containers"
	# @./scripts/docker_run.sh
	docker-compose up

.PHONY: run
run: #\t🏃 Run the app with the given JSON data file.
	@echo "🏃 Run the app with the given JSON data file."
	docker-compose run --rm app $(json_file_path)

.PHONY: down
down: #\t🗑️ Delete all Docker containers and images.
	@echo "🗑️ Delete all Docker containers and images"
	@./scripts/down.sh

.PHONY: test
test: setup #\t🏃 Run pytests related to the app.
	@echo "🏃 Running tests for the app"
	@./scripts/pytest.sh

.PHONY: validation
validation: setup #🔄 Validate python code formatting and lint.
	@echo "🔄 Validate python code formatting and lint"
	@./scripts/code_validation.sh

# .PHONY: airflow
# airflow: #▶️ Run airflow.
# 	@echo "▶️ Run airflow"
# 	@./scripts/run_airflow.sh

# .PHONY: dbt
# dbt: #\t▶️ Run dbt.
# 	@echo "▶️ Run dbt"
# 	@./scripts/dbt_run.sh

.PHONY: start
start: verification test run #✨ Validate, test and run the app.
	@echo "✨ Validated, tested and started the app and its dependencies."

.PHONY: stop
stop: down #✨ Stop the app and clean all docker images and containers.
	@echo "✨ Stop the app and clean all docker images and containers."
