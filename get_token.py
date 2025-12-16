import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from accounts.models import CustomUser
from accounts.utils import generate_password_reset_token

# Get user
email = sys.argv[1] if len(sys.argv) > 1 else 'test@example.com'

try:
    user = CustomUser.objects.get(email=email)
    token = generate_password_reset_token(user)
    
    print("=" * 70)
    print(f"User: {user.username}")
    print(f"Email: {user.email}")
    print("=" * 70)
    print()
    print("RESET TOKEN:")
    print("-" * 70)
    print(token)
    print("-" * 70)
    print()
    print("RESET URL:")
    print("-" * 70)
    print(f"http://127.0.0.1:8000/reset-password/?token={token}")
    print("-" * 70)
    
except CustomUser.DoesNotExist:
    print(f"User with email {email} not found!")
