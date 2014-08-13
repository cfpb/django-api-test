from .settings import *

MIDDLEWARE_CLASSES = (
    'example_app.middleware.cust_test_middleware.CustomTestMiddleware',  # must be first
) + MIDDLEWARE_CLASSES

INSTALLED_APPS += (
    'api_test',
)