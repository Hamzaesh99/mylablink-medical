
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import Appointment, Patient, TestType

User = get_user_model()

# 1. Get a doctor (assuming current user context, but fetch first doctor)
doctors = User.objects.filter(role='doctor')
if not doctors.exists():
    print("No doctors found!")
    exit()
doctor = doctors.first()
print(f"Using Doctor: {doctor.username}")

# 2. Get or Create a Patient User
patient_user, created = User.objects.get_or_create(
    username='test_patient',
    defaults={
        'email': 'patient@test.com',
        'first_name': 'Test',
        'last_name': 'Patient',
        'role': 'patient'
    }
)
if created:
    patient_user.set_password('password123')
    patient_user.save()
    print("Created test patient user")

# Ensure Patient Profile
patient_profile, created = Patient.objects.get_or_create(user=patient_user, defaults={'dob': '1990-01-01', 'phone': '0912345678'})

# 3. Create an Appointment
test_type = TestType.objects.first()
if not test_type:
    test_type = TestType.objects.create(name='General Checkup', description='Routine check', price=50)

Appointment.objects.create(
    patient=patient_profile,
    doctor=doctor,
    test_type=test_type,
    date=datetime.now().date(),
    time=datetime.now().time(),
    status='pending'
)

print(f"Created appointment for {patient_user.username} with {doctor.username}")
