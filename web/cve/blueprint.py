from flask import Blueprint
from .views import CveView, CveHomeView

cve_bp = Blueprint('cve', __name__, url_prefix='/api/v2/cve')

cve_bp.add_url_rule('/cve_info', view_func=CveView.as_view('cve_info'), methods=['GET'])
cve_bp.add_url_rule('/cve_home', view_func=CveHomeView.as_view('cve_home'), methods=['GET'])
