from flask.views import MethodView
from flask import request
from main import UserManager


class QueryUserView(MethodView):

    def get(self):
         params = request.args
         data = UserManager.query_user(params)
         return data
