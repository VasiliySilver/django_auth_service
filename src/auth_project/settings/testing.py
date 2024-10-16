from .base import *  # noqa: F403

# Override base settings for testing
DEBUG = True

# Add any additional testing-specific settings
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# Override ALLOWED_HOSTS for testing
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]  # noqa: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
