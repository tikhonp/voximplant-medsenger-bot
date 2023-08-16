from medsenger_api import AgentApiClient

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

DOMAIN = 'http://127.0.0.1:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDSENGER_API_CLIENT = AgentApiClient(MEDSENGER_APP_KEY, MEDSENGER_MAIN_HOST, MEDSENGER_AGENT_ID, DEBUG, not DEBUG)
