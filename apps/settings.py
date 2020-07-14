# -*- coding: utf-8 -*-
NAME = "hupiao"
DB_APT_URI = "postgresql://postgres:123456@192.168.217.137:5432/flask_learn"

BASE_DIR = '/opt/work/'


# redis配置
REDIS_ENCRYPT = "YES"
REDIS_PASSWD = "123456"

REDIS_HOST = '192.168.217.135'
REDIS_PORT = 7378

SESSION_REDIS_DB = 0
CACHE_REDIS_DB = 1

# rpc配置
GUISH_RPC_SERVER_ADDR = '127.0.0.1'
GUISH_RPC_SERVER_PORT = 18861
