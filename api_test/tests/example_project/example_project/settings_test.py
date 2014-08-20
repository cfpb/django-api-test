from .settings import *

MIDDLEWARE_CLASSES = (
    'api_test.middleware.api_test.ApiTestMiddleware',  # must be first
) + MIDDLEWARE_CLASSES

INSTALLED_APPS += (
    'api_test',
)