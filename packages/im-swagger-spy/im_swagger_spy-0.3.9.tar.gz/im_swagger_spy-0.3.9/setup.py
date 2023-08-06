from setuptools import setup, find_packages
import pathlib

import im_swagger_spy

setup(
    name='im-swagger-spy',
    version=im_swagger_spy.__version__,
    description='A example Python package',
    url='https://gitlab.corp.mail.ru/imqa/im-swagger-spy',
    author='Valerii Korobov',
    author_email='v.korobov@corp.mail.ru',
    license='MIT',
    packages=find_packages(exclude=['example', 'tests', 'openapi']),
    install_requires=pathlib.Path('requirements.txt').read_text().splitlines(),
    package_data={'': ['template.html']},
    entry_points={"pytest11": ["im_swagger_spy = im_swagger_spy.plugin"]},
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    include_package_data=True,
    python_requires='>=3.8'
)
