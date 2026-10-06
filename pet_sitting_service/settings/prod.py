import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "*"]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
   ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": int(os.environ["POSTGRES_DB_PORT"]),
        "OPTIONS": {
           "sslmode": "require",
       },
    }
}