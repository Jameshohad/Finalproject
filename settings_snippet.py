# Put this near the top of config/settings.py after BASE_DIR is defined.
# Also run: pip install python-dotenv django-redis
import os
from dotenv import load_dotenv

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = [h for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    origin for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",") if origin
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},
}
