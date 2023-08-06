# im-swagger-spy

pytest plugin for matching methods in swagger with those used in tests

## Установка

```bash
pip install git+https://github.com/dasshit/im-swagger-spy.git
```

## Использование

Есть несколько вариантов использования

### Вариант №1

pytest.ini
```ini
[pytest]
addopts = --swagger-url http://localhost/client/v101/u/api.yaml # Адрес, с которого можно получить swagger.json|yaml или openapi.json|yaml
            --swagger-prefix /api/v101                          # Префикс к path методов из документации
            --swagger-name test.ru                              # Название сервиса (для отчета)
            --swagger-report  reports/                          # Путь к папке для сохранения отчета
```
conftest.py
```python
import pytest
import requests


@pytest.fixture(scope='session')
def session(swagger_http_spy):

    session = requests.Session()

    swagger_http_spy.register_as_hook(session)

    yield session # Запросы этой сессии попадут в отчет
``` 
CI
```bash
pytest tests/
python -m im_swagger_spy build
```

### Другие примеры

Можно посмотреть в example/
