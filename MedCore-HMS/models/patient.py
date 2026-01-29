from models import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    medical_record_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    blood_type = db.Column(db.String(5), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    emergency_contact_name = db.Column(db.String(200), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    
    # Medical information
    admission_date = db.Column(db.DateTime, nullable=True)
    discharge_date = db.Column(db.DateTime, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    medical_history = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='active', nullable=False)  # active, discharged, critical
    
    # Assignments
    assigned_doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_nurse_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    assigned_doctor = db.relationship('User', foreign_keys=[assigned_doctor_id], backref='patients_as_doctor')
    assigned_nurse = db.relationship('User', foreign_keys=[assigned_nurse_id], backref='patients_as_nurse')
    room = db.relationship('Room', foreign_keys=[room_id], backref='patients')
    
    def __repr__(self):
        return f'<Patient {self.full_name} (MRN: {self.medical_record_number})>'
