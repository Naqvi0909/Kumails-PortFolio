from flask import Blueprint

medical_records_bp = Blueprint('medical_records', __name__, url_prefix='/medical-records')

@medical_records_bp.route('/')
def index():
    return "Medical Records module - Coming soon"
