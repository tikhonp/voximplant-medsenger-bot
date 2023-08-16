from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'voximplant.ai.medsenger.ru',
]

DOMAIN = 'https://voximplant.ai.medsenger.ru'

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

MEDSENGER_API_CLIENT = AgentApiClient(MEDSENGER_APP_KEY, MEDSENGER_MAIN_HOST, MEDSENGER_AGENT_ID, DEBUG, not DEBUG)
