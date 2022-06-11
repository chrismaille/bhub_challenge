# Exported variables for subshells, and their default values
export PYTHONPATH 	:= $(PWD)

# Loading .env if exists. This file can override the variables above.
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

#############################
# DOCKER COMMANDS           #
#############################

.PHONY: format
# Format code inside docker
format:
	@echo "Running Black..."
	@black .

.PHONY: test
# Run Tests inside docker.
test:
	@echo "Running Tests..."
	@pytest --ignore=migrations

.PHONY: coverage
# Run Tests with Coverage inside Docker.
coverage:
	@echo "Running Tests with Coverage..."
	@pytest --cov=. --ignore=migrations

.PHONY: bandit
# Run Bandit inside Docker.
bandit:
	@echo "Running Bandit..."
	@bandit -r .

.PHONY: pylint
# Run Pylint inside Docker.
pylint:
	@echo "Running PyLint..."
	@pylint core datasource_serasa

.PHONY: black
# Run Black inside Docker.
black:
	@echo "Running Black..."
	@black --check .

.PHONY: precommit
# Run Pre-Commit inside Docker.
pre-commit:
	@echo "Running Pre-Commit..."
	@pre-commit install -f
	@pre-commit run --all

.PHONY: lint
# Run Bandit, Lint, Unit Tests and Coverage inside docker.
lint: pre-commit coverage
	@echo "Finish Lint"

.PHONY: update
# Update application dependencies
update:
	@poetry update --lock
	@echo "Update complete. Please rebuild DevContainer."

.PHONY: coverage_and_report
# Prepare and Send Coverage Report inside Docker
coverage_and_report: coverage
	@coverage xml

.PHONY: migrate
# Run database migration
migrate:
	@python manage.py migrate

.PHONY: migrations
# Create database migrations
migrations:
	@python manage.py makemigrations

.PHONY: config_project
# Automate first install
config_project:
	@echo "Configuring project..."
	@cp env.example .env
	@docker-compose build
	@echo ">>> Opening VSCode..."
	@code .
