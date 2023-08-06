import sys
import logging

from im_swagger_spy.base import SwaggerBaseSpy


logging.basicConfig(
    level=logging.INFO,
    format=' '.join([
        '[%(asctime)s]',
        '[%(levelname)s]',
        '[%(name)s]',
        '%(message)s',
        '(%(filename)s:%(lineno)s)'
    ])
)

if sys.argv[1] == 'build':
    SwaggerBaseSpy.build_report()
