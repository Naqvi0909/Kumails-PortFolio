from models import db
from datetime import datetime

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)  # ICU, ER, General Ward, OR, Pediatric
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    is_occupied = db.Column(db.Boolean, default=False, nullable=False)
    current_patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    department = db.relationship('Department', backref='rooms')
    current_patient = db.relationship('Patient', foreign_keys=[current_patient_id], backref='current_room')
    
    def __repr__(self):
        return f'<Room {self.room_number} ({self.room_type})>'
