import sentry_sdk
from medsenger_api import AgentApiClient
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # To set a uniform sample rate
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production,
    profiles_sample_rate=1.0,
)

HOST = 'https://voximplant.ai.medsenger.ru'

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS = [
    'https://voximplant.ai.medsenger.ru',
    'https://medsenger.ru',
]

ALLOWED_HOSTS = [
    'voximplant.ai.medsenger.ru',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

MEDSENGER_API_CLIENT = AgentApiClient(
    os.getenv('MEDSENGER_APP_KEY'),
    host=os.getenv('MEDSENGER_MAIN_HOST'),
    agent_id=os.getenv('MEDSENGER_AGENT_ID'),
    debug=DEBUG,
    use_grpc=not DEBUG
)
