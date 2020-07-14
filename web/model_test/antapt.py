# -*-coding: utf-8 -*-

from base import Database
from model import AntaptBase


class DatabaseConfig(object):
    ANTAPT_URI = 'postgresql://postgres:Qihoo-postgresql-123!@#@localhost:5432/antapt'
    WEBMANAGE_URI = 'postgresql://postgres:Qihoo-postgresql-123!@#@localhost:5432/webmanage'
    SAMPLE_URI = 'postgresql://postgres:Qihoo-postgresql-123!@#@127.0.0.1:5432/sample'


class AntaptDatabase(Database):

    def __init__(self, uri=None, pool_size=10, pool_recycle=3600):
        self.uri = uri or DatabaseConfig.ANTAPT_URI
        super(AntaptDatabase, self).__init__(
            base=AntaptBase,
            uri=self.uri,
            pool_size=pool_size,
            pool_recycle=pool_recycle
        )
