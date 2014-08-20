from setuptools import setup

setup(
    name='django-api-test',
    version='0.1.0',
    author='David Greisen (CFPB)',
    author_email='david.greisen@cfpb.gov',
    packages=['api_test', 'api_test.tests'],
    url='http://pypi.python.org/pypi/django-api-test/',
    license='LICENSE',
    description='Test server to easily test an API with any test framework',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.4.0",
    ],
    test_requires=[
        "requests >= 2.3.0",
    ],
    test_suite="api_test.tests",
)
