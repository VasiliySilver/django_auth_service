.PHONY: help init install update run test lint migrate superuser clean commit bump release

# Переменные
PYTHON_VERSION := 3.12.0
PROJECT_NAME := $(shell basename $(CURDIR))
PYTHON := poetry run python
MANAGE := $(PYTHON) manage.py

# Помощь
help:
	@echo "Доступные команды:"
	@echo "  make init       - Инициализация проекта (pyenv, poetry, commitizen)"
	@echo "  make install    - Установка зависимостей с помощью Poetry"
	@echo "  make update     - Обновление зависимостей"
	@echo "  make run        - Запуск сервера разработки"
	@echo "  make test       - Запуск тестов"
	@echo "  make lint       - Проверка кода линтером"
	@echo "  make migrate    - Применение миграций"
	@echo "  make superuser  - Создание суперпользователя"
	@echo "  make clean      - Очистка файлов кэша и временных файлов"
	@echo "  make commit     - Создание коммита с помощью Commitizen"
	@echo "  make bump       - Увеличение версии проекта"
	@echo "  make release    - Создание нового релиза"

# Инициализация проекта
init:
	@echo "Инициализация проекта..."
	@if ! command -v pyenv >/dev/null 2>&1; then \
		echo "pyenv не установлен. Пожалуйста, установите pyenv перед продолжением."; \
		exit 1; \
	fi
	@echo "Установка Python $(PYTHON_VERSION) через pyenv..."
	pyenv install $(PYTHON_VERSION) -s
	@echo "Создание виртуального окружения для проекта..."
	pyenv virtualenv $(PYTHON_VERSION) $(PROJECT_NAME)
	pyenv local $(PROJECT_NAME)
	@echo "Установка poetry..."
	pip install poetry
	@echo "Инициализация poetry..."
	poetry init -n
	@echo "Добавление dev-зависимостей..."
	poetry add --dev pytest flake8 mypy commitizen
	@echo "Настройка commitizen..."
	poetry run cz init
	@echo "Инициализация завершена."

# Установка зависимостей
install:
	poetry install

# Обновление зависимостей
update:
	poetry update

# Запуск сервера разработки
run:
	$(MANAGE) runserver

# Запуск тестов
test:
	poetry run pytest

# Проверка кода линтером
lint:
	poetry run flake8 .
	poetry run mypy .

# Применение миграций
migrate:
	$(MANAGE) migrate

# Создание суперпользователя
superuser:
	$(MANAGE) createsuperuser

# Очистка файлов кэша и временных файлов
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name "*.db" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache

# Создание коммита с помощью Commitizen
commit:
	poetry run cz commit

# Увеличение версии проекта
bump:
	poetry run cz bump --changelog

# Создание нового релиза
release:
	@echo "Создание нового релиза..."
	poetry run cz bump --changelog
	git push
	git push --tags
