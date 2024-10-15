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
COPY . /app

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Запускаем сервер
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "auth_project.wsgi:application"]

