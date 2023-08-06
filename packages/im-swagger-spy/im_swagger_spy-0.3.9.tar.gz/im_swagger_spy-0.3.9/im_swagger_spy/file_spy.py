import logging
from typing import Optional

from im_swagger_spy.base import SwaggerBaseSpy


logger = logging.getLogger('im-swagger-spy.file')


class SwaggerFileSpy(SwaggerBaseSpy):

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

        for base_path in self.base_paths:

            for path, value in self.safe_load(base_path.read_text())['paths'].items():

                logger.debug(f'{path} - {value}')

                if "$ref" in value:
                    current_file = base_path.parent.joinpath(value["$ref"])

                    self.add_path(
                        path,
                        self.safe_load(
                            current_file.open()
                        )
                    )
                else:
                    self.add_path(
                        path,
                        value
                    )
