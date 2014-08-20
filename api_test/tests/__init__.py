try:
    import unittest2 as unittest  # import unittest2 for 2.6
except ImportError:
    import unittest

import subprocess
from collections import namedtuple
import requests
import os
import json
import time
import signal

DIR = os.path.dirname(os.path.realpath(__file__))
MANAGE_PATH = os.path.join(DIR, 'example_project', 'manage.py')

HOST = 'http://localhost'

Std = namedtuple('std', ['out', 'err'])

def server_start(settings='example_project.settings_test', *args, **kwargs):
    """
    Start a test server in its own subprocess with the passed args, kwargs;
    yield the process; shut down the subprocess. kwargs are converted from
        {'a': 'b'} to --a b
    """
    args = list(args)
    kwargs['settings'] = settings
    for k, v in kwargs.items():
        args += ['--%s' % k, v]
    p = subprocess.Popen([MANAGE_PATH, 'api_test_server'] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    return p

def server_stop(p):
    """
    stop the server in subprocess p, return a namedtuple of (out, err,)
    ensuring they are strings.
    """
    p.send_signal(signal.SIGINT)
    out = p.communicate()
    return Std(*[str(item) for item in out])

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.url = HOST + ':8001/users/'
        self.reset_url = HOST + ':8001/_reset'

    def tearDown(self):
        self.p.send_signal(signal.SIGINT)

    def test_reset_url_resets_database(self):
        self.p = server_start()
        requests.post(self.url, data=json.dumps({'username': 'user1'}))

        actual = requests.get(self.url)
        self.assertEqual(actual.json(), [{'username': 'user1'}])

        requests.get(self.reset_url)

        actual = requests.get(self.url)
        self.assertEqual(actual.json(), [])

    def test_custom_reset_url_works(self):

        self.p = server_start(settings='example_project.settings_custom_reset')
        reset_url = HOST + ':8001/_new_test'

        actual = requests.get(reset_url)
        self.assertIn('new test started', actual.text)

    def test_setUp_run_when_specified(self):
        self.p = server_start(settings='example_project.settings_custom_middleware')

        resp = requests.get(self.reset_url).text

        self.assertIn('setup', resp)

    def test_tearDown_run_when_specified(self):
        self.p = server_start(settings='example_project.settings_custom_middleware')

        resp = requests.get(self.reset_url).text

        self.assertIn('teardown', resp)


if __name__ == '__main__':
    unittest.main()
