from main import app
from models import db
from models.user import User
from models.department import Department
from models.room import Room
from models.patient import Patient
from datetime import datetime, date, timedelta
import random

def seed_database():
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            print("Database already seeded. Skipping...")
            return
        
        print("Seeding database...")
        
        # Create departments
        departments = [
            Department(name='Emergency', description='Emergency Department'),
            Department(name='Internal Medicine', description='Internal Medicine Department'),
            Department(name='Cardiology', description='Cardiology Department'),
            Department(name='Surgery', description='Surgery Department'),
            Department(name='Pediatrics', description='Pediatrics Department')
        ]
        
        for dept in departments:
            db.session.add(dept)
        
        db.session.commit()
        print("Departments created")
        
        # Create users
        users = [
            User(
                username='admin',
                email='admin@medcore.com',
                full_name='System Administrator',
                role='administrator',
                department_id=None
            ),
            User(
                username='dr.williams',
                email='williams@medcore.com',
                full_name='Dr. Sarah Williams',
                role='physician',
                department_id=departments[1].id
            ),
            User(
                username='dr.johnson',
                email='johnson@medcore.com',
                full_name='Dr. Michael Johnson',
                role='physician',
                department_id=departments[2].id
            ),
            User(
                username='dr.brown',
                email='brown@medcore.com',
                full_name='Dr. Emily Brown',
                role='specialist',
                department_id=departments[3].id
            ),
            User(
                username='nurse.davis',
                email='davis@medcore.com',
                full_name='Nurse Jennifer Davis',
                role='nurse',
                department_id=departments[0].id
            ),
            User(
                username='nurse.miller',
                email='miller@medcore.com',
                full_name='Nurse Robert Miller',
                role='nurse',
                department_id=departments[1].id
            )
        ]
        
        # Set default password for all users
        for user in users:
            user.set_password('admin')
            db.session.add(user)
        
        db.session.commit()
        print("Users created (default password: admin)")
        
        # Update department heads
        departments[0].head_id = users[4].id  # Nurse Davis heads Emergency
        departments[1].head_id = users[1].id  # Dr. Williams heads Internal Medicine
        departments[2].head_id = users[2].id  # Dr. Johnson heads Cardiology
        departments[3].head_id = users[3].id  # Dr. Brown heads Surgery
        departments[4].head_id = users[1].id  # Dr. Williams also heads Pediatrics
        
        db.session.commit()
        
        # Create rooms
        room_types = ['ICU', 'ER', 'General Ward', 'OR', 'Pediatric']
        rooms = []
        
        for i, room_type in enumerate(room_types):
            for j in range(1, 5):
                room = Room(
                    room_number=f'{i+1}0{j}',
                    room_type=room_type,
                    department_id=departments[i].id,
                    is_occupied=False
                )
                rooms.append(room)
                db.session.add(room)
        
        db.session.commit()
        print("Rooms created")
        
        # Create sample patients
        patients_data = [
            {
                'full_name': 'John Smith',
                'date_of_birth': date(1975, 5, 15),
                'gender': 'Male',
                'blood_type': 'O+',
                'phone': '555-0101',
                'diagnosis': 'Hypertension',
                'status': 'active',
                'assigned_doctor': users[1],
                'assigned_nurse': users[5],
                'room': rooms[0]
            },
            {
                'full_name': 'Mary Johnson',
                'date_of_birth': date(1982, 8, 22),
                'gender': 'Female',
                'blood_type': 'A+',
                'phone': '555-0102',
                'diagnosis': 'Diabetes Type 2',
                'status': 'active',
                'assigned_doctor': users[1],
                'assigned_nurse': users[5],
                'room': rooms[1]
            },
            {
                'full_name': 'Robert Williams',
                'date_of_birth': date(1968, 3, 10),
                'gender': 'Male',
                'blood_type': 'B+',
                'phone': '555-0103',
                'diagnosis': 'Cardiac Arrhythmia',
                'status': 'critical',
                'assigned_doctor': users[2],
                'assigned_nurse': users[4],
                'room': rooms[4]
            }
        ]
        
        for idx, patient_data in enumerate(patients_data, 1):
            patient = Patient(
                medical_record_number=f'MRN{datetime.now().year}{idx:05d}',
                full_name=patient_data['full_name'],
                date_of_birth=patient_data['date_of_birth'],
                gender=patient_data['gender'],
                blood_type=patient_data['blood_type'],
                phone=patient_data['phone'],
                email=f"{patient_data['full_name'].lower().replace(' ', '.')}@email.com",
                address=f'{random.randint(100, 999)} Main St, City, State',
                emergency_contact_name=f"{patient_data['full_name'].split()[0]} Emergency Contact",
                emergency_contact_phone=f'555-{random.randint(1000, 9999)}',
                admission_date=datetime.now() - timedelta(days=random.randint(1, 10)),
                diagnosis=patient_data['diagnosis'],
                medical_history='See detailed records',
                allergies='None reported',
                status=patient_data['status'],
                assigned_doctor_id=patient_data['assigned_doctor'].id,
                assigned_nurse_id=patient_data['assigned_nurse'].id,
                room_id=patient_data['room'].id
            )
            db.session.add(patient)
            
            # Mark room as occupied
            patient_data['room'].is_occupied = True
            patient_data['room'].current_patient_id = patient.id
        
        db.session.commit()
        print("Sample patients created")
        print("\nDatabase seeding completed successfully!")
        print("\nLogin credentials:")
        print("  Username: admin | Password: admin (Administrator)")
        print("  Username: dr.williams | Password: admin (Physician)")
        print("  Username: nurse.davis | Password: admin (Nurse)")

if __name__ == '__main__':
    seed_database()
