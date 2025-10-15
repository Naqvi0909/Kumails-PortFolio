from flask import Blueprint

hospital_bp = Blueprint('hospital', __name__, url_prefix='/hospital')

@hospital_bp.route('/')
def index():
    return "Hospital Resources module - Coming soon"
