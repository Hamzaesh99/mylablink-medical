from accounts.models import CustomUser
from accounts.utils import generate_email_token

user = CustomUser.objects.filter(is_active=False).last()

if not user:
    print("No inactive users found!")
else:
    token = generate_email_token(user)
    link = f"http://127.0.0.1:8000/api/accounts/verify-email/{token}/"
    
    print("=" * 70)
    print(f"User: {user.username}")
    print(f"Email: {user.email}")
    print(f"Name: {user.first_name}")
    print("=" * 70)
    print()
    print("VERIFICATION LINK:")
    print("-" * 70)
    print(link)
    print("-" * 70)
