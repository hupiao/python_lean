from flask import Blueprint
from .views import LoginView, HomeView

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

admin_bp.add_url_rule('/login', view_func=LoginView.as_view('login'), methods=['GET', 'POST'])
admin_bp.add_url_rule('/home', view_func=HomeView.as_view('home'), methods=['GET', ])

