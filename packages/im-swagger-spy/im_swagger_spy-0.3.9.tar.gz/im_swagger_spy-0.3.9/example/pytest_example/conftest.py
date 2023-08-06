import pytest
import requests


@pytest.fixture(scope='session')
def session(swagger_http_spy):

    session = requests.Session()

    swagger_http_spy.register_as_hook(session)

    yield session
