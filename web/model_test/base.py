# -*-coding: utf-8 -*-

from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class Singleton(object):
    _instances = {}
    _obj = {}

    def __new__(cls, *args, **kwargs):
        key = (cls, args, tuple(kwargs.values()))
        if not cls._instances.get(key):
            orig = super(Singleton, cls)
            obj = orig.__new__(cls, *args, **kwargs)
            cls._instances[key] = obj
            cls._obj[obj] = dict(init=False)
            setattr(cls, '__init__', cls.decorate_init(cls.__init__))
        return cls._instances[key]

    @classmethod
    def decorate_init(cls, fun):
        def warp_init(*args, **kwargs):
            if not cls._obj.get(args[0], {}).get('init'):
                fun(*args, **kwargs)

        return warp_init


def register_db_event(db):
    def handle_error(exception_context):
        conn = db.session.connection()
        if conn.in_transaction():
            db.session.rollback()

        if exception_context.is_disconnect is True:
            db._engine.dispose()
            # 重建连接池
            if getattr(db._engine, "pool", None):
                db._engine.pool = db._engine.pool.recreate()

    event.listen(db._engine, "handle_error", handle_error)


class Database(Singleton):

    def __init__(self, base, uri, pool_size=10, pool_recycle=3600):
        self.base = base
        self._engine = create_engine(
            uri,
            echo=False,
            encoding="utf-8",
            pool_size=pool_size,
            pool_recycle=pool_recycle)
        self.session = self.make_session()
        register_db_event(self)

    def __del__(self):
        """Disconnects pool."""
        self._engine.dispose()

    def create_tables(self):
        self.base.metadata.create_all(self._engine)

    def make_session(self):
        session_factory = sessionmaker(bind=self._engine)
        session_class = scoped_session(session_factory)
        return session_class()

    def close(self):
        self.session.close()

    def close_session(self, session):
        if session:
            session.close()

    # @property
    # def session(self):
    #     return self.make_session()
