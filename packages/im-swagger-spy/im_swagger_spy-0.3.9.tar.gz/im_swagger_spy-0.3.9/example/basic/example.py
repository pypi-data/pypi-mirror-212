import requests

from im_swagger_spy.http_spy import SwaggerHttpSpy

import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s (%(filename)s:%(lineno)s)'
)


# swag_spy = SwaggerFileSpy('yaml.icq.net', 'openapi/yaml/api.yaml', '/api/openapi_example')
swag_spy = SwaggerHttpSpy('myteam.mail.ru', 'http://100.99.4.29:8000/client/v101/u/api.yaml', '/api/v101')
swag_spy.load_schema()

ss = requests.Session()
ss.hooks['response'].append(swag_spy.handle_response)


ss.get('https://ya.ru/bot/v1/chats/getMembers')
ss.get('https://ya.ru/api/v101/files/info/1234')
ss.get('https://ya.ru/api/v101/files/info/1234')
ss.get('https://ya.ru/api/v101/files/info/1234')
ss.get('https://ya.ru/api/v101/files/info/1234/')
ss.get('https://ya.ru/api/v101/rapi/auth/oidc/authorize')
ss.post('https://ya.ru/api/v101/rapi/auth/sendCode')

swag_spy.report()
