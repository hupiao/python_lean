from apps.db import User, dbsession


class UserManager(object):
    @classmethod
    def query_user(cls, params):
        search_user = dbsession.query(User)
        return []



