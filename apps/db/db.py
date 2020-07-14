# -*- coding: utf-8 -*-
import re
import sys
from sqlalchemy import Column, Integer, String, DateTime, Float, BIGINT, Text
# from sqlalchemy import create_engine
# from mypsgres import MyPsgres
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from apps.settings import DB_APT_URI
from apps.db.database import ANTAPT_Database

reload(sys)
sys.setdefaultencoding('utf-8')

Base = declarative_base()
dbsession = ANTAPT_Database(DB_APT_URI).make_session()


class User(Base):
    __tablename__ = "user"
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column('name', String, nullable=True)
    password = Column('password', String, nullable=True)
    # url_test = Column(String, nullable=True)
    file_type = Column('file_type', String, nullable=True)
    create_time = Column('sreate_time', DateTime, default=datetime.utcnow())
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    def __init__(self, id, name, password, file_type, create_time):
        self.id = id
        self.name = name
        self.password = password
        self.file_type = file_type
        self.create_time = create_time


class White(Base):
    __tablename__ = "white"

    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    mail_address = Column('mail_address', String(128), nullable=False)
    create_dt = Column("create_dt", DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}


class Cvelib(Base):
    __tablename__ = 'cve_lib'

    id = Column('id', BIGINT, primary_key=True, autoincrement=True, index=True)
    name = Column('name', String(256), nullable=True)
    public_time = Column('public_time', String(32), nullable=True)
    cve_id = Column('cve_id', String(32), nullable=True)
    cnnvd_id = Column('cnnvd_id', String(32), nullable=True)
    bug_type = Column('bug_type', String(64), nullable=True)
    bug_level = Column('bug_level', String(64), nullable=True)
    cvss_scole = Column('cvss_scole', Float(10, 1), nullable=True)
    usability = Column('usability', String(64), nullable=True)
    bug_describe = Column('bug_describe', String(20480), nullable=True)
    solve_way = Column('solve_way', String(20480), nullable=True)
    ref = Column('ref', String(256), nullable=True)

    def __repr__(self):
        return "<Cvelib('{0}','{1}')>".format(self.id, self.name)


def test(**kwargs):
    if 'id' in kwargs:
        print(User(**kwargs))
        # print(**kwargs)
        print(kwargs['id'])


def search_escape(s):
    return re.sub(r"[(){}\[\].*?|^$\\+-]", r"\\\g<0>", s)

#
# engine = create_engine('postgresql://postgres:123456@192.168.217.135:5432/flask_learn',encoding='utf-8',echo=True)
# Base.metadata.create_all(engine)
