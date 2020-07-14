#! /usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sshtunnel import SSHTunnelForwarder


class MyPsgres(object):
    def __init__(self, database, user, pwd, host, port='5432'):
        con_info = 'postgresql://' + user + ':' + pwd + '@' + host + ':' + port + '/' + database
        print(con_info)
        try:
            con = create_engine(con_info)
            DBSession = sessionmaker(bind=con)
            self.session = DBSession()
        except Exception:
            print("Failed to connect postgres.Exception is ",
                  traceback.print_exc())

