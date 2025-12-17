
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import Message

User = get_user_model()

# Get Doctor and Patient
doctor = User.objects.filter(role='doctor').first()
patient = User.objects.filter(role='patient', username='patient_demo').first()

if doctor and patient:
    # 1. Patient asking
    Message.objects.create(
        sender=patient,
        receiver=doctor,
        content='السلام عليكم دكتور، متى تظهر نتيجة التحليل؟',
        is_read=False
    )
    print("Patient message sent")
    
    # 2. Doctor replying
    Message.objects.create(
        sender=doctor,
        receiver=patient,
        content='وعليكم السلام، النتيجة ستكون جاهزة غداً بإذن الله.',
        is_read=True 
    )
    print("Doctor reply sent")

    # 3. Another message
    Message.objects.create(
        sender=patient,
        receiver=doctor,
        content='شكراً جزيلاً لك',
        is_read=False
    )
    print("Conversation created!")
else:
    print("Could not find doctor or demo patient")
