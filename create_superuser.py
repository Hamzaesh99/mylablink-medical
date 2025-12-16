import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from accounts.models import CustomUser

# Create superuser
username = 'admin'
email = 'admin@mylablink.local'
password = 'admin123'  # Change this to a secure password

# Check if user already exists
if CustomUser.objects.filter(email=email).exists():
    print(f"✓ Admin user '{email}' already exists")
    user = CustomUser.objects.get(email=email)
else:
    user = CustomUser.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Admin',
        last_name='User',
        role='patient'  # Using 'patient' since 'admin' is not in ROLE_CHOICES
    )
    # Make sure the user is active
    user.is_active = True
    user.save()
    print(f"✓ Superuser created successfully!")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print(f"  Role: {user.role}")
    print(f"  Is Active: {user.is_active}")
