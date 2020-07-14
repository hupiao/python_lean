# -*- coding:utf-8 -*-
# __author__ = "hupiao"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BIGINT, Float

engine = create_engine("postgresql://postgres:Qihoo-postgresql-123!@#@localhost:5432/antapt", encoding="utf-8",
                       echo=True, max_overflow=5)
# 连接pg数据库，echo为是否打印结果


AntaptBase = declarative_base(name='AntaptBase')  # 生成orm基类


class Cvelib(AntaptBase):
    __tablename__ = 'cve_lib'

    id = Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    name = Column(String(256), nullable=True)
    public_time = Column(String(32), nullable=True)
    cve_id = Column(String(32), nullable=False, index=True)
    cnnvd_id = Column(String(32), nullable=True)
    bug_type = Column(String(64), nullable=True)
    bug_level = Column(String(64), nullable=True)
    cvss_scole = Column(Float(10, 1), nullable=True)
    usability = Column(String(64), nullable=True)
    bug_describe = Column(String(20480), nullable=True)
    solve_way = Column(String(20480), nullable=True)
    ref = Column(String(256), nullable=True)

    def as_dict(self):
        return {
            'name': self.name if self.name != u'无' else self.cve_id,
            'public_time': self.public_time,
            'cve_id': self.cve_id,
            'cnnvd_id': self.cnnvd_id,
            'bug_type': self.bug_type,
            'bug_level': self.bug_level,
            'cvss_scole': self.cvss_scole,
            'usability': self.usability,
            'bug_describe': self.bug_describe,
            'solve_way': self.solve_way,
            'ref': self.ref,
        }


AntaptBase.metadata.create_all(engine)  # 创建表结构
