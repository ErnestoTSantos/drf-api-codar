from marked.settings.base import *

DEBUG = True
ALLOWED_HOSTS = []
LOGGING = {
    **LOGGING,
    "loggers": {"": {"level": "DEBUG", "handlers": ["console", "file"]}},
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
