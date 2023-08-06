import json
import pathlib
import re
import logging
from string import Formatter
from typing import Literal, Optional

import peewee
import requests
from requests.adapters import HTTPAdapter

from urllib.parse import urlparse

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

from im_swagger_spy import utils
from im_swagger_spy.syncdb import HttpMethodModel, ReportInfo, UsedHttpMethodModel

from playhouse.shortcuts import model_to_dict

logger = logging.getLogger('im-swagger-spy.base')


class SwaggerBaseSpy:
    decoder = None
    exclude_json = []

    def __init__(
            self,
            service_name: str,
            targets: list[str],
            api_prefix: str = '',
            report_path: str = '.',
            exclude_json: Optional[str] = None
    ):

        self.service = service_name

        self.API_PATH_PREFIX = api_prefix

        self.report_path = report_path

        self.target = targets

        self.swagger_urls = []
        self.base_paths = []

        self.exclude_json = exclude_json

        for target in targets:

            if target.startswith('http://') or target.startswith('https://'):
                self.swagger_urls.append(target)
            else:
                self.base_paths.append(pathlib.Path(target))

    @staticmethod
    def safe_load(file_content: str):

        return yaml.safe_load(file_content)

    def add_path(self, path: str, method_info_json: dict):

        logger.debug(f'path: {path}, method_info_json: {method_info_json}')

        for method in filter(lambda x: x.upper() in ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'], method_info_json.keys()):
            api_path_format_keys = {i[1]: ".+" for i in Formatter().parse(path) if i[1] is not None}
            # api_path = self.API_PATH_PREFIX + path
            api_path = path

            HttpMethodModel.get_or_create(
                method=method.upper(),
                path=api_path,
                regexp=api_path.format(**api_path_format_keys) if api_path_format_keys else None
            )

    @classmethod
    def report_models(cls):

        USED_METHODS_MODELS_LIST = []
        SKIPPED_METHODS_MODELS_LIST = []

        for method in HttpMethodModel.select().where(
            HttpMethodModel.path.not_in(cls.exclude_json)
        ):

            query = UsedHttpMethodModel.select(
                UsedHttpMethodModel.method,
                UsedHttpMethodModel.host,
                UsedHttpMethodModel.path,
                peewee.fn.COUNT("*").alias('count')
            ) \
                .where(
                UsedHttpMethodModel.method == method.method,
            ) \
                .group_by(UsedHttpMethodModel.method, UsedHttpMethodModel.path)

            logger.debug(f'Grouped stats count: {query.count()}')

            for used_method in filter(
                    lambda x: x.count,
                    query
            ):

                logger.debug(method)
                logger.debug(used_method.path)

                logger.debug(f'method.path == used_method.path : {method.path in used_method.path}')

                logger.debug(
                    f'(method.regexp is not None and re.compile(method.regexp).match(used_method.path) : {method.regexp is not None and re.compile(method.regexp).findall(used_method.path)}')

                if method.path in used_method.path or \
                        (method.regexp is not None and re.compile(method.regexp).findall(used_method.path)):
                    method_dict = model_to_dict(method)
                    method_dict['count'] = used_method.count
                    method_dict['host'] = used_method.host

                    USED_METHODS_MODELS_LIST.append(
                        method_dict
                    )
                    break


            else:
                SKIPPED_METHODS_MODELS_LIST.append(
                    model_to_dict(method)
                )

        logger.debug(f'USED_METHODS_MODELS_LIST: {USED_METHODS_MODELS_LIST}')
        logger.debug(f'SKIPPED_METHODS_MODELS_LIST: {SKIPPED_METHODS_MODELS_LIST}')

        return USED_METHODS_MODELS_LIST, SKIPPED_METHODS_MODELS_LIST

    def handle_response(self, response: requests.Response, *args, **kwargs):

        request_path = response.request.path_url.split('?')[0]

        self.handle_strings(response.request.method, urlparse(response.url).netloc, request_path)

    def handle_strings(
            self,
            method: Literal['GET', 'POST', 'PUT', 'PATCH', 'TRACE', 'OPTION', 'DELETE', 'HEAD'],
            host: str,
            path: str
    ):

        logger.debug(f'[{method}] {path}')

        model = UsedHttpMethodModel.create(method=method, host=host, path=path)

        logger.debug(f'[{method}] {path} - {model}')

    def register_as_hook(self, session: "requests.Session"):

        # logger.debug('Registering as hook')
        #
        # session.hooks['response'] = self.handle_response
        #
        # logger.debug(session.hooks)

        for scheme in ("http://", "https://"):
            session.mount(scheme, LoggingHTTPAdapter(swagger=self))

    @classmethod
    def render(
            cls,
            service,
            report_path
    ):
        USED_METHODS_LIST, SKIPPED_METHODS_LIST = cls.report_models()

        TOTAL_METHODS_COUNT = len(USED_METHODS_LIST) + len(SKIPPED_METHODS_LIST)

        env = Environment(
            loader=FileSystemLoader(
                pathlib.Path(__file__).parent.absolute().__str__()),
            autoescape=select_autoescape(['html'])
        )

        template = env.get_template('template.html')

        rendered_page = template.render(
            service=service,
            used_methods=list(USED_METHODS_LIST),
            used_methods_count=len(USED_METHODS_LIST),
            skipped_methods=SKIPPED_METHODS_LIST,
            skipped_methods_count=len(SKIPPED_METHODS_LIST),
            total_methods_count=TOTAL_METHODS_COUNT
        )

        report_folder_object = pathlib.Path(report_path)

        report_folder_object.mkdir(parents=True, exist_ok=True)

        report_path_object = report_folder_object.joinpath(
            f'spy-report-{service}.html')

        report_path_object.write_text(rendered_page)

        logger.info(f'Report is saved to {report_path_object.absolute()}')

    @classmethod
    def build_report(cls):
        logger.info('Trying to build report from .swagger-spy-db.sqlite')

        service = ReportInfo.select(ReportInfo.info_text).where(ReportInfo.info_type == 'service').first().info_text
        report_folder = ReportInfo.select(ReportInfo.info_text).where(
            ReportInfo.info_type == 'report_path').first().info_text

        cls.exclude_json = ReportInfo.select(
            ReportInfo.info_text).where(
                ReportInfo.info_type == 'exclude_json'
            ).first().info_text

        if cls.exclude_json is not None:
            cls.exclude_json = json.loads(
                pathlib.Path(cls.exclude_json).read_text())
        else:
            cls.exclude_json = []

        cls.render(service, report_folder)

    def report(self, force_db_save: bool = False):

        logger.debug('Assembling report in worker')

        if self.report_path is None:
            raise ValueError('Report path is None')

        USED_METHODS_LIST, SKIPPED_METHODS_LIST = self.report_models()

        TOTAL_METHODS_COUNT = len(USED_METHODS_LIST) + len(SKIPPED_METHODS_LIST)

        logger.debug(f'TOTAL_METHODS_COUNT: {TOTAL_METHODS_COUNT}')

        for info in [
            {
                'info_type': 'service', 'info_text': self.service
            },
            {
                'info_type': 'report_path', 'info_text': self.report_path
            },
            {
                'info_type': 'exclude_json',
                'info_text': self.exclude_json
            }
        ]:
            try:
                ReportInfo.get_or_create(**info)
            except peewee.IntegrityError:
                model = ReportInfo.get(info_type=info['info_type'])
                model.info_text = info['info_text']
                model.save()

        logger.info('Report saved in database, ensure to run "python -m im_swagger_spy build" to get html report')


class LoggingHTTPAdapter(HTTPAdapter):
    def __init__(self, swagger, *args, **kwargs):
        super(LoggingHTTPAdapter, self).__init__(*args, **kwargs)

        self.swagger = swagger

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):

        response = super(LoggingHTTPAdapter, self).send(request, stream, timeout, verify, cert, proxies)

        self.swagger.handle_response(response)

        return response
