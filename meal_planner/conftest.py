import pytest
from django.conf import settings
from django.test.utils import get_runner
from django.test import Client

def pytest_configure():
    settings.debug = False
    settings.PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
    return get_runner(settings)()


@pytest.fixture(scope='session')
def django_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        django_db_setup.setup_databases()
    yield
    with django_db_blocker.unblock():
        django_db_setup.teardown_databases()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture
def client():
    client = Client()
    return client
