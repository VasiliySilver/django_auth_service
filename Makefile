.PHONY: help install update run test lint clean commit bump release docker-build docker-up docker-down

# Переменные
PYTHON_VERSION := 3.12.0
PROJECT_NAME := $(shell basename $(CURDIR))
PYTHON := poetry run python
MANAGE := $(PYTHON) manage.py

# Помощь
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies using Poetry"
	@echo "  update     - Update dependencies"
	@echo "  run        - Run the development server"
	@echo "  test       - Run tests"
	@echo "  lint       - Check code with linters"
	@echo "  clean      - Clean cache and temporary files"
	@echo "  commit     - Create a commit using Commitizen"
	@echo "  bump       - Bump the project version"
	@echo "  release    - Create a new release"
	@echo "  docker-build - Build Docker images"
	@echo "  docker-up  - Start Docker containers"
	@echo "  docker-down - Stop Docker containers"

# Установка зависимостей
install:
	poetry install

# Обновление зависимостей
update:
	poetry update

# Запуск сервера разработки
run:
	poetry run python src/manage.py runserver

# Запуск тестов
test:
	DJANGO_ENVIRONMENT=testing poetry run python src/manage.py test tests

# Проверка кода линтером
lint:
	poetry run flake8 src tests
	poetry run mypy src tests

# Очистка файлов кэша и временных файлов
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Создание коммита с помощью Commitizen
commit:
	poetry run cz commit

# Увеличение версии проекта
bump:
	poetry run cz bump

# Создание нового релиза
release:
	poetry run cz bump --changelog

# Build Docker images
docker-build:
	docker-compose -f docker/docker-compose.yml build

# Start Docker containers
docker-up:
	docker-compose -f docker/docker-compose.yml up

# Stop Docker containers
docker-down:
	docker-compose -f docker/docker-compose.yml down
