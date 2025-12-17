#!/usr/bin/env python
"""
Generate verification link for a user
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from accounts.models import CustomUser
from accounts.utils import generate_email_token

def main():
    print("=" * 60)
    print("Generate Email Verification Link")
    print("=" * 60)
    print()
    
    # Get all users
    users = CustomUser.objects.all()
    
    if not users.exists():
        print("No users found in database!")
        return
    
    print("Available users:")
    print("-" * 60)
    for user in users:
        status = "✓ Active" if user.is_active else "✗ Inactive"
        print(f"ID: {user.id:3d} | {user.username:20s} | {user.email:30s} | {status}")
    print("-" * 60)
    print()
    
    # Get user ID from input
    try:
        user_id = input("Enter user ID to generate verification link (or press Enter for last user): ").strip()
        
        if not user_id:
            user = users.last()
            print(f"Using last user: {user.username}")
        else:
            user = CustomUser.objects.get(id=int(user_id))
            
    except (ValueError, CustomUser.DoesNotExist):
        print("Invalid user ID!")
        return
    
    print()
    print("=" * 60)
    print(f"User: {user.username} ({user.email})")
    print(f"Active: {user.is_active}")
    print("=" * 60)
    print()
    
    # Generate token
    token = generate_email_token(user)
    
    # Generate link
    verification_link = f"http://127.0.0.1:8000/api/accounts/verify-email/{token}/"
    
    print("Verification Link:")
    print("-" * 60)
    print(verification_link)
    print("-" * 60)
    print()
    print("Instructions:")
    print("1. Copy the link above")
    print("2. Paste it in your browser")
    print("3. The account will be activated")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
