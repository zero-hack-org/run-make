# flake8: noqa

from .base import *

DEBUG = True

# DataBase for test

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "USER": "test-user",
        "PASSWORD": "test-pass",
    }
}
