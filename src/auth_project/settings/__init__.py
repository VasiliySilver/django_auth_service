import os

environment = os.environ.get("DJANGO_ENVIRONMENT", "development")

if environment == "production":
    from .production import *  # noqa: F403
elif environment == "testing":
    from .testing import *  # noqa: F403
else:
    from auth_project.settings.development import *  # noqa: F403
