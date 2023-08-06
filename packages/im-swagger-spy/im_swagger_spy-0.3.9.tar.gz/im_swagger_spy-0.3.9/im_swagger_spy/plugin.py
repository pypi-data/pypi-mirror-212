import logging

from urllib.parse import urlparse

import pytest

from im_swagger_spy.http_spy import SwaggerHttpSpy
from im_swagger_spy.file_spy import SwaggerFileSpy
from im_swagger_spy.syncdb import HttpMethodModel, UsedHttpMethodModel, ReportInfo


logger = logging.getLogger(__name__)


def pytest_addoption(parser: pytest.Parser):
    group = parser.getgroup("reporting")

    group.addoption(
        '--swagger-report',
        action="store",
        dest="swagger_report",
        metavar="DIR",
        default='.',
        help="Generate Swagger-Spy report in the specified directory"
    )
    group.addoption(
        '--swagger-url',
        action="append",
        type=str,
        dest="swagger_urls",
        metavar="URL",
        default=[],
        help="URL/Path to swagger.json|yaml|yml file"
    )
    group.addoption(
        '--swagger-prefix',
        action="store",
        dest="swagger_prefix",
        metavar="/v1",
        default='',
        required=False,
        help="Prefix to add to complete path from documentation "
             "(in cases of several API versions)"
    )
    group.addoption(
        '--swagger-name',
        action="store",
        dest="swagger_name",
        default=None,
        help="Name of target service"
    )
    group.addoption(
        '--swagger-exclude-json',
        action="store",
        dest="swagger_exclude_json",
        metavar="PATH",
        default=None,
        help="Exclude provided paths from report"
    )


# @pytest.fixture(scope='session', autouse=True)
# def clear_base():
#
#     for table in [HttpMethodModel, UsedHttpMethodModel, ReportInfo]:
#         table.delete().execute()
#
#     yield


@pytest.fixture(scope='session')
def swagger_http_spy(pytestconfig: pytest.Config):

    logger.info(f'IM-Swagger-Spy: Url is {pytestconfig.option.swagger_urls}')
    
    if pytestconfig.option.swagger_urls:

        sw_spy = SwaggerHttpSpy(
            service_name=pytestconfig.option.swagger_name or urlparse(
                pytestconfig.option.swagger_url).netloc,
            targets=pytestconfig.option.swagger_urls,
            api_prefix=pytestconfig.option.swagger_prefix,
            report_path=pytestconfig.option.swagger_report,
            exclude_json=pytestconfig.option.swagger_exclude_json
        )
        
        sw_spy.load_schema()
    
        yield sw_spy
    
        sw_spy.report()
        
    else:
        
        yield None


@pytest.fixture(scope='session')
def swagger_file_spy(pytestconfig: pytest.Config):

    logger.info(f'IM-Swagger-Spy: Url is {pytestconfig.option.swagger_urls}')
    
    if pytestconfig.option.swagger_urls:

        sw_spy = SwaggerFileSpy(
            service_name=pytestconfig.option.swagger_name,
            targets=pytestconfig.option.swagger_urls,
            api_prefix=pytestconfig.option.swagger_prefix,
            report_path=pytestconfig.option.swagger_report,
            exclude_json=pytestconfig.option.swagger_exclude_json
        )
        
        sw_spy.load_schema()
    
        yield sw_spy
    
        sw_spy.report()
        
    else:
        
        yield None
