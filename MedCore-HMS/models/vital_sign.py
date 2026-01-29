from models import db
from datetime import datetime

class VitalSign(db.Model):
    __tablename__ = 'vital_signs'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    recorded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Vital measurements
    temperature = db.Column(db.Float, nullable=True)  # in Celsius
    blood_pressure_systolic = db.Column(db.Integer, nullable=True)
    blood_pressure_diastolic = db.Column(db.Integer, nullable=True)
    heart_rate = db.Column(db.Integer, nullable=True)  # beats per minute
    respiratory_rate = db.Column(db.Integer, nullable=True)  # breaths per minute
    oxygen_saturation = db.Column(db.Float, nullable=True)  # percentage
    blood_glucose = db.Column(db.Float, nullable=True)  # mg/dL
    
    notes = db.Column(db.Text, nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    patient = db.relationship('Patient', backref='vital_signs')
    recorded_by = db.relationship('User', backref='recorded_vital_signs')
    
    def __repr__(self):
        return f'<VitalSign for Patient ID {self.patient_id} at {self.recorded_at}>'
