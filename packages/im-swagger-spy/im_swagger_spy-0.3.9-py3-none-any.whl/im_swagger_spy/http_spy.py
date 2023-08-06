from typing import Optional

import requests
import logging

from im_swagger_spy.base import SwaggerBaseSpy


logger = logging.getLogger('im-swagger-spy.http')


class SwaggerHttpSpy(SwaggerBaseSpy):

    def __init__(
            self,
            service_name: str,
            targets: list[str],
            api_prefix: str = '',
            report_path: str = '.',
            exclude_json: Optional[list] = None
    ):

        super().__init__(service_name, targets, api_prefix, report_path, exclude_json)

    def load_schema(self):

        with requests.Session() as local_session:

            for swagger_url in self.swagger_urls:

                response = local_session.get(swagger_url)

                logger.debug(
                    f'{response.request.method} '
                    f'{response.request.path_url} - {response}'
                )

                for path, value in self.safe_load(response.text)['paths'].items():

                    if "$ref" in value:
                        response = local_session.get(
                            '/'.join(swagger_url.split('/')[:-1] + [value["$ref"]])
                        )

                        logger.debug(
                            f'{response.request.method} '
                            f'{response.request.path_url} - {response}'
                        )

                        self.add_path(
                            path,
                            self.safe_load(
                                response.text
                            )
                        )

                    else:

                        logger.debug(f'Adding info for path {path}')

                        self.add_path(
                            path,
                            value
                        )
