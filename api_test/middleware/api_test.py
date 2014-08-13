from django.http import HttpResponse
from django.test import TransactionTestCase
from django.conf import settings
import json

class StubTestCase(TransactionTestCase):
    """
    This class doesn't do anything; just gives access to
    bound TransactionTestCase methods
    """
    def __init__(self, *args, **kwargs):
        return

class ApiTestMiddleware(object):
    def process_request(self, request):
        """
        process a request by doing the following:

        * if path equals settings.REMOTE_TEST_RESET_URL, reset the server and prepare for a new test by calling the following methods:
            * self.tearDown(request) - if it exists
            * TransactionTestCase._post_teardown
            * TransactionTestCase._pre_setup
            * self.setUp(request) - if it exists
        """
        # import ipdb
        # ipdb.set_trace()
        reset_url = getattr(settings, 'REMOTE_TEST_RESET_URL', '/_reset')
        if request.path == reset_url:
            testcase = StubTestCase()
            try:
                td = self.tearDown(request)
            except AttributeError:
                pass
            testcase._post_teardown()
            testcase._pre_setup()
            try:
                su = self.setUp(request)
            except AttributeError:
                pass
            out = {'status': 'new test started', 'setUp': su, 'tearDown': td}
            return HttpResponse(json.dumps(out))
        else:
            return None