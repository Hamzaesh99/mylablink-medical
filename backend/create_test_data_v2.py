
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import Appointment, Patient, TestType, Doctor

User = get_user_model()

# 1. Get a doctor user
doctors = User.objects.filter(role='doctor')
if not doctors.exists():
    print("No doctor users found!")
    exit()
doctor_user = doctors.first()
print(f"Using Doctor User: {doctor_user.username}")

# 2. Get/Create Doctor Profile
doctor_profile, created = Doctor.objects.get_or_create(
    user=doctor_user,
    defaults={'specialty': 'Genetics', 'bio': 'Expert in genetics'}
)
if created:
    print("Created doctor profile")

# 3. Get or Create a Patient User
patient_user, created = User.objects.get_or_create(
    username='patient_demo',
    defaults={
        'email': 'patient_demo@test.com',
        'first_name': 'سعيد',
        'last_name': 'المريض',
        'role': 'patient'
    }
)
if created:
    patient_user.set_password('password123')
    patient_user.save()
    print("Created demo patient user")

# Ensure Patient Profile
patient_profile, created = Patient.objects.get_or_create(user=patient_user, defaults={'dob': '1995-05-05', 'phone': '0919998877'})

# 4. Create an Appointment (Future date)
test_type = TestType.objects.first()
if not test_type:
    test_type = TestType.objects.create(name='General Checkup', description='Routine check', price=50)

# Create/Get Appointment
Appointment.objects.create(
    patient=patient_profile,
    doctor=doctor_profile,
    date=datetime.now() + timedelta(days=1),
    status='confirmed'
)

print(f"Created appointment for {patient_user.first_name} with Dr. {doctor_user.first_name}")

# Also create a past result so logic works both ways
from api.models import Result
Result.objects.create(
    patient=patient_profile,
    test_type=test_type,
    value='Normal',
    status='completed',
    issued_by=doctor_user
)
print("Created a result record as well.")
