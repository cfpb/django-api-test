from .settings import *

REMOTE_TEST_RESET_URL = '/_new_test'

MIDDLEWARE_CLASSES = (
    'api_test.middleware.api_test.ApiTestMiddleware',  # must be first
) + MIDDLEWARE_CLASSES

INSTALLED_APPS += (
    'api_test',
)