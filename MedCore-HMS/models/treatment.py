from models import db
from datetime import datetime

class Treatment(db.Model):
    __tablename__ = 'treatments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    treatment_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prescribed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='ongoing', nullable=False)  # ongoing, completed, discontinued
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    patient = db.relationship('Patient', backref='treatments')
    prescribed_by = db.relationship('User', backref='prescribed_treatments')
    
    def __repr__(self):
        return f'<Treatment {self.treatment_type} for Patient ID {self.patient_id}>'
