from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()


class ANTAPT_Database(object):
    def __init__(self, connection_string, create_table=True):
        self._engine = create_engine(
            connection_string,
            echo=False,
            encoding="utf-8",
            pool_size=100,
            pool_recycle=3600)
        if create_table:
            Base.metadata.create_all(self._engine)
        self.dbsession = None

    def make_session(self):
        session_factory = sessionmaker(bind=self._engine)
        Session = scoped_session(session_factory)
        self.dbsession = Session()
        return self.dbsession

    def close_session(self):
        self.dbsession.close()
