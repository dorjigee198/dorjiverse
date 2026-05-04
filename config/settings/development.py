"""
Development settings — uses SQLite, debug on, relaxed security.
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# SQLite for local development (no PostgreSQL needed)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Print emails to the console instead of sending them
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
