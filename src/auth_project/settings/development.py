import os

from .base import *  # noqa: F403

DEBUG = True

# Override ALLOWED_HOSTS for development
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]  # noqa: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "dev_db"),
        "USER": os.environ.get("POSTGRES_USER", "dev_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "dev_password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
