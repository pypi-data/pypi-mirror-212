import pathlib

import peewee

from playhouse.sqlite_ext import SqliteExtDatabase


database = SqliteExtDatabase(
        str(pathlib.Path('.').joinpath('.im-swagger-spy-db.sqlite')),
        regexp_function=True,
        pragmas={
            'journal_mode': 'wal',
            'cache_size': -1024 * 64
        }
)


class BaseModel(peewee.Model):

    class Meta:
        database = database


class ReportInfo(BaseModel):

    info_type = peewee.TextField(unique=True)
    info_text = peewee.TextField(null=True)


class HttpMethodModel(BaseModel):

    method = peewee.TextField()
    path = peewee.TextField()
    regexp = peewee.TextField(null=True)

    def __str__(self):
        return f'HttpMethodModel([{self.method}] {self.path} - {self.regexp})'

    class Meta:
        constraints = [peewee.SQL('UNIQUE (method, path)')]


class UsedHttpMethodModel(BaseModel):

    method = peewee.TextField()
    host = peewee.TextField()
    path = peewee.TextField()


database.create_tables([
    ReportInfo,
    HttpMethodModel,
    UsedHttpMethodModel
])
