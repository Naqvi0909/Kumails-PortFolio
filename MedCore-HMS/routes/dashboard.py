from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import db
from models.patient import Patient
from models.room import Room
from models.user import User
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    # Get statistics
    total_patients = Patient.query.count()
    active_patients = Patient.query.filter_by(status='active').count()
    critical_patients = Patient.query.filter_by(status='critical').count()
    discharged_patients = Patient.query.filter_by(status='discharged').count()
    
    total_rooms = Room.query.count()
    occupied_rooms = Room.query.filter_by(is_occupied=True).count()
    available_rooms = total_rooms - occupied_rooms
    
    total_staff = User.query.count()
    
    # Get recent patients
    recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html',
                         total_patients=total_patients,
                         active_patients=active_patients,
                         critical_patients=critical_patients,
                         discharged_patients=discharged_patients,
                         total_rooms=total_rooms,
                         occupied_rooms=occupied_rooms,
                         available_rooms=available_rooms,
                         total_staff=total_staff,
                         recent_patients=recent_patients)
