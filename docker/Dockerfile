# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости
RUN pip install poetry
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем проект
COPY src /app/src
COPY tests /app/tests

# Устанавливаем переменную окружения для Python, чтобы использовать режим без буферизации вывода
ENV PYTHONUNBUFFERED 1

# Добавляем entrypoint скрипт
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Устанавливаем entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Запускаем сервер по умолчанию
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]

