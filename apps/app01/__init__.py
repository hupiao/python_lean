from flask import Blueprint
from .views import QueryUserView

app01_bp = Blueprint('app01', __name__, url_prefix='/app01')

queryuser_view = QueryUserView.as_view('query_user')

app01_bp.add_url_rule('/query_user', view_func=queryuser_view, methods=['GET'])
