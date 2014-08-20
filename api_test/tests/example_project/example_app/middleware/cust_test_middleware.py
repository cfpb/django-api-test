from api_test.middleware.api_test import ApiTestMiddleware

class CustomTestMiddleware(ApiTestMiddleware):
    def setUp(self, request):
        return "setup"

    def tearDown(self, request):
        return "teardown"
