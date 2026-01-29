from models import db
from datetime import datetime

class Medication(db.Model):
    __tablename__ = 'medications'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medication_name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(100), nullable=False)
    route = db.Column(db.String(50), nullable=False)  # oral, IV, topical, etc.
    prescribed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='active', nullable=False)  # active, completed, discontinued
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    patient = db.relationship('Patient', backref='medications')
    prescribed_by = db.relationship('User', backref='prescribed_medications')
    
    def __repr__(self):
        return f'<Medication {self.medication_name} for Patient ID {self.patient_id}>'
