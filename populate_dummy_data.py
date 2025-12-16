
import os
import django
import sys
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mylablink_python.settings")
django.setup()

from django.contrib.auth import get_user_model
from api.models import Patient, TestType, Result

User = get_user_model()

def populate_dummy_data():
    print("Creating dummy data...")

    # 1. Create Patients
    patients_data = [
        {"username": "ahmed_ali", "email": "ahmed@example.com", "first_name": "أحمد", "last_name": "علي", "phone": "0912345678", "gender": "male"},
        {"username": "fatma_hassan", "email": "fatma@example.com", "first_name": "فاطمة", "last_name": "حسن", "phone": "0923456789", "gender": "female"},
        {"username": "khaled_omar", "email": "khaled@example.com", "first_name": "خالد", "last_name": "عمر", "phone": "0911223344", "gender": "male"},
        {"username": "sara_moh", "email": "sara@example.com", "first_name": "سارة", "last_name": "محمد", "phone": "0922334455", "gender": "female"},
    ]

    created_patients = []
    
    for pd in patients_data:
        user, created = User.objects.get_or_create(
            email=pd["email"],
            defaults={
                "username": pd["username"],
                "first_name": pd["first_name"],
                "last_name": pd["last_name"],
                "role": "patient",
                "phone": pd["phone"],
                "is_active": True
            }
        )
        if created:
            user.set_password("password123")
            user.save()
            print(f"Created user: {user.username}")
        
        patient, _ = Patient.objects.get_or_create(user=user)
        created_patients.append(patient)

    # 2. Results
    test_types = TestType.objects.all()
    if not test_types:
        print("No test types found. Run populate_test_types.py first.")
        return

    statuses = ['completed', 'pending', 'critical', 'draft']
    
    # Get a doctor user for 'issued_by'
    doctor = User.objects.filter(role='doctor').first()
    if not doctor:
        print("No doctor found. Creating one...")
        doctor = User.objects.create(
            username="doctor_demo", 
            email="doctor@demo.com", 
            first_name="Doctor", 
            last_name="Demo", 
            role="doctor",
            is_active=True
        )
        doctor.set_password("doctor123")
        doctor.save()

    print("Creating results...")
    for patient in created_patients:
        # Create 2-3 results for each patient
        for _ in range(random.randint(1, 3)):
            test_type = random.choice(test_types)
            status = random.choice(statuses)
            issued_at = timezone.now() - timedelta(days=random.randint(0, 30))
            
            result = Result.objects.create(
                patient=patient,
                test_type=test_type,
                value=f"Sample result value for {test_type.name}",
                notes="تيريل تجريبي تم إنشاؤه تلقائياً",
                status=status,
                issued_by=doctor,
                issued_at=issued_at
            )
            print(f"Created result for {patient.user.username}: {test_type.name}")

    print("Done! Dummy data populated.")

if __name__ == "__main__":
    populate_dummy_data()
