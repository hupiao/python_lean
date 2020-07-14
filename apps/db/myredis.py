# -*- coding:utf-8 -*-
import redis
from apps.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWD, SESSION_REDIS_DB


class Myredis(object):

    def __init__(self, host, port, pwd, db):
        self.host = host
        self.port = port
        self.pwd = pwd
        self.db = db
        self._connect(self.host, self.port, self.pwd, self.db)

    def _connect(self, host, port, pwd, db):
        self.client = redis.Redis(host, port, password=pwd, db=db)
        self.client.ping()


# if __name__ == "__main__":
#     client = Myredis(REDIS_HOST, REDIS_PORT, REDIS_PASSWD, SESSION_REDIS_DB)
