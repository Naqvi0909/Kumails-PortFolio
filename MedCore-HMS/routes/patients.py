from flask import Blueprint

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

@patients_bp.route('/')
def index():
    return "Patients module - Coming soon"
