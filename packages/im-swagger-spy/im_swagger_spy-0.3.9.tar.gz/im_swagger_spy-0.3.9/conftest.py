import pytest
import requests
import logging

from im_swagger_spy import http_spy
from im_swagger_spy.syncdb import HttpMethodModel, UsedHttpMethodModel, ReportInfo


logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def clear_db(request: pytest.FixtureRequest):
    logger.info(f'Cleaning database before test "{request.node.name}"')

    for table in [HttpMethodModel, UsedHttpMethodModel, ReportInfo]:
        table.delete().execute()

    yield None


@pytest.fixture(scope='session', autouse=True)
def clear_db_after_all_tests():

    yield

    logger.info('Cleaning database after all tests')

    for table in [HttpMethodModel, UsedHttpMethodModel, ReportInfo]:
        table.delete().execute()


@pytest.fixture(scope='session')
def session():

    session = requests.Session()

    yield session


@pytest.fixture(scope='session')
def swagger(session):
    spy = http_spy.SwaggerHttpSpy(
        service_name='vk_teams.botapi',
        targets=['https://petstore.swagger.io/v2/swagger.json'],
        api_prefix='/bot/v1',
        report_path='.'
    )

    spy.load_schema()

    yield spy
