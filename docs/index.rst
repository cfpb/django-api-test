Welcome to django-api-test's documentation!
===========================================

Contents:

.. toctree::
   :maxdepth: 2

What
----
django-api-test is a test framework for quickly testing APIs and their associated clients. It makes it possible to asyncronously test both a rich web app and its underlying api with a single set of browser tests. It is implemented by a 
single django middleware.

django-api-test creates a test server that exposes a special
endpoint to signify that a test has started/ended. You can
now use any test framework you desire in any programming
language to run your tests. 

(not implemented) django-api-test also records all api calls
for each test performed on the server. Once the recording is
made, you can test the client against the recorded api calls
without hitting the database, and you can test database
against the recorded api calls without driving a browser.


Why
---
Generally a django rich web application is composed of a 
static client and a dynamic backend accessed through an api.
Sometimes, on large projects, the frontend is built by a 
separate team on a different cadence from the backend. The
API provides the contract by which the two components talk
to each other. 

django-api-test has the following features:
 - decouple integration/system tests from code to make CI
   and remote testing easier.
 - speed up backend regression testing by testing the api
   without driving the browser
 - speed up client regression testing by testing the client
   without hitting a database
 - create a testable recording of correct API request/
   response pairs -- a set of cannonical transactions --
   that can act as a living, testable contract between client
   and server.

How
---

Installation
^^^^^^^^^^^^
Install the package:: bash

    pip install django-api-test

**DO NOT ADD TO PRODUCTION SETTINGS.PY** - anyone could reset
your database by visiting the reset url.

You almost certainly want to add the app and middleware to a custom test-only settings.py file; something like ``settings_test.py``:

.. code:: python

    from .settings import *

    MIDDLEWARE_CLASSES = (
        'api_test.middleware.api_test.ApiTestMiddleware',  # must be first
    ) + MIDDLEWARE_CLASSES

    INSTALLED_APPS += (
        'api_test',
    )

Customize the test server (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^

set REMOTE_TEST_RESET_URL
"""""""""""""""""""""""""
By default, the server will be reset when your test runner
``GET``s ``/_reset``. You can set the reset path to any
path you want by setting ``REMOTE_TEST_RESET_URL`` in your
settings.py.

Custom serverside setUp and tearDown
""""""""""""""""""""""""""""""""""""
You can set custom ``setUp`` and `tearDown`` methods by
subclassing ``ApiTestMiddleware`` and creating bound methods
of those names. They are both passed the request object:

.. code:: python

    from api_test.middleware.api_test import ApiTestMiddleware

    class CustomTestMiddleware(ApiTestMiddleware):
        def setUp(self, request):
            # do custom setup here

        def tearDown(self, request):
            # do custom teardown here

You must then replace the default ApiTestMiddleware installed
above with your custom middleware.

Integrate with your Client Testing Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Your client framework will have some hook for running a
command before a test. When a test is started, you need to
make a ``GET`` to the reset endpoint (defaults to 
``/_reset``).

Run your full-stack tests
^^^^^^^^^^^^^^^^^^^^^^^^^
First start your test server:

.. code:: bash

    python ./manage.py api_test_server --settings "path.to.settings_test"

The server is now listening on port 8001 by default. Specify 
``--addrport <port>`` to change it. The test database is not destroyed at the end of a run. Specify ``--noinput`` to
automatically destroy any test databases hanging around.

Now, run your client-side tests. It doesn't matter how or 
where you you do it as long as your tests connect to the 
test server port.

Testing
-------
run:

.. code:: bash

    python setup.py test

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

