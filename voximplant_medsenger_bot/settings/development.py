from medsenger_api import AgentApiClient

from .base import *

DEBUG = True

HOST = 'http://127.0.0.1:8000'

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://localhost',
]

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

MEDSENGER_API_CLIENT = AgentApiClient(
    os.getenv('MEDSENGER_APP_KEY'),
    host=os.getenv('MEDSENGER_MAIN_HOST'),
    agent_id=os.getenv('MEDSENGER_AGENT_ID'),
    debug=DEBUG,
    use_grpc=not DEBUG
)

# Enable for logging SQL queries

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }
