#!/usr/bin/env python
"""Simple script to generate verification link"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from accounts.models import CustomUser
from accounts.utils import generate_email_token

# Get the last registered user
user = CustomUser.objects.filter(is_active=False).last()

if not user:
    print("No inactive users found!")
    print("All users are already activated or no users exist.")
    sys.exit(1)

print("=" * 70)
print(f"User: {user.username}")
print(f"Email: {user.email}")
print(f"Name: {user.first_name}")
print(f"Active: {user.is_active}")
print("=" * 70)
print()

# Generate token
token = generate_email_token(user)

# Generate link
verification_link = f"http://127.0.0.1:8000/api/accounts/verify-email/{token}/"

print("VERIFICATION LINK:")
print("-" * 70)
print(verification_link)
print("-" * 70)
print()
print("INSTRUCTIONS:")
print("1. Copy the link above")
print("2. Paste it in your browser")
print("3. Press Enter")
print("4. Your account will be activated!")
print()
print("=" * 70)
