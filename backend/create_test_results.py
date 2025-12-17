
import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import Result, TestType, Patient

User = get_user_model()

def create_data():
    username = 'hamzaeshtiba5'
    user, created = User.objects.get_or_create(username=username, defaults={'role': 'patient', 'email': 'hamza@example.com'})
    if created:
         user.set_password('password123')
         user.save()
         print(f"Created user: {username}")
    else:
        print(f"Found user: {username}")

    # Create Patient Profile if not exists
    patient_profile, created = Patient.objects.get_or_create(user=user)
    
    # Find or create a doctor
    doctor_user, created = User.objects.get_or_create(username='doctor_ahmed', defaults={'role': 'doctor', 'email': 'doctor@example.com', 'first_name': 'أحمد', 'last_name': 'محمد'})
    if created:
        doctor_user.set_password('password123')
        doctor_user.save()

    # Create Test Types if not exist
    types = ['CBC', 'Blood Sugar', 'Lipid Profile', 'Vitamin D']
    test_types = []
    for t_name in types:
        tt, _ = TestType.objects.get_or_create(name=t_name, defaults={'description': f'Analysis for {t_name}'})
        test_types.append(tt)

    # Create Results
    statuses = ['completed', 'completed', 'pending'] 
    
    for i in range(3):
        tt = random.choice(test_types)
        status = statuses[i]
        
        days_ago = random.randint(0, 30)
        date = timezone.now() - timedelta(days=days_ago)
        
        result = Result.objects.create(
            patient=patient_profile,
            test_type=tt,
            value=f"{random.uniform(10, 200):.1f} mg/dL",
            status=status,
            issued_by=doctor_user,
            notes='Mock result data for Hamza.',
            created_at=date
        )
        result.issued_at = date
        result.save()
        
        print(f"Created result for {username}: {tt.name}")

if __name__ == '__main__':
    create_data()
