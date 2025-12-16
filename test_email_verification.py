#!/usr/bin/env python
"""
Complete Email Verification System Test
"""
import os
import sys
import django
import requests
import json

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from accounts.models import User
from accounts.utils import generate_email_token
import random

API_BASE = "http://127.0.0.1:8000"

def print_test(num, description):
    print(f"\nTest {num}: {description}")
    print("-" * 70)

def print_pass(message):
    print(f"   ✓ PASS - {message}")

def print_fail(message):
    print(f"   ✗ FAIL - {message}")

def main():
    print("=" * 70)
    print("Testing Email Verification System")
    print("=" * 70)
    
    tests_passed = 0
    tests_failed = 0
    
    # Generate test data
    random_num = random.randint(10000, 99999)
    test_email = f"emailtest{random_num}@example.com"
    test_username = f"emailtest{random_num}"
    test_password = "TestPass123!"
    
    # Test 1: Register user
    print_test(1, "Registering a new user")
    
    register_data = {
        "username": test_username,
        "email": test_email,
        "first_name": "Email",
        "last_name": "Test",
        "password": test_password,
        "password2": test_password,
        "phone": "0912345678",
        "national_id": str(random.randint(100000000000, 999999999999)),
        "governorate": "Tripoli"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/api/accounts/register/",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print_pass(f"User registered: {test_email}")
            tests_passed += 1
        else:
            print_fail(f"Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            tests_failed += 1
            return
    except Exception as e:
        print_fail(f"Registration error: {str(e)}")
        tests_failed += 1
        return
    
    # Test 2: Check user is inactive
    print_test(2, "Checking user is inactive (not verified)")
    
    try:
        user = User.objects.get(email=test_email)
        if not user.is_active:
            print_pass("User is inactive (waiting for verification)")
            tests_passed += 1
        else:
            print_fail("User should be inactive!")
            tests_failed += 1
    except User.DoesNotExist:
        print_fail("User not found in database!")
        tests_failed += 1
        return
    
    # Test 3: Generate verification token
    print_test(3, "Generating verification token")
    
    try:
        token = generate_email_token(user)
        if token and len(token) > 20:
            print_pass(f"Token generated: {token[:30]}...")
            tests_passed += 1
        else:
            print_fail("Token generation failed")
            tests_failed += 1
            return
    except Exception as e:
        print_fail(f"Token generation error: {str(e)}")
        tests_failed += 1
        return
    
    # Test 4: Verify email
    print_test(4, "Verifying email with token")
    
    try:
        response = requests.get(f"{API_BASE}/api/accounts/verify-email/{token}/")
        
        if response.status_code == 200:
            print_pass("Email verified successfully")
            print(f"   Response: {response.json()}")
            tests_passed += 1
        else:
            print_fail(f"Verification failed: {response.status_code}")
            print(f"   Response: {response.text}")
            tests_failed += 1
    except Exception as e:
        print_fail(f"Verification error: {str(e)}")
        tests_failed += 1
    
    # Test 5: Check user is now active
    print_test(5, "Checking user is now active")
    
    try:
        user.refresh_from_db()
        if user.is_active:
            print_pass("User is now active!")
            tests_passed += 1
        else:
            print_fail("User should be active after verification!")
            tests_failed += 1
    except Exception as e:
        print_fail(f"Error checking user status: {str(e)}")
        tests_failed += 1
    
    # Test 6: Try to login
    print_test(6, "Testing login with verified account")
    
    login_data = {
        "username": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/api/auth/token/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'access' in data and 'refresh' in data:
                print_pass("Login successful with verified account")
                print(f"   Access token: {data['access'][:30]}...")
                print(f"   Refresh token: {data['refresh'][:30]}...")
                tests_passed += 1
            else:
                print_fail("Login succeeded but no tokens received")
                tests_failed += 1
        else:
            print_fail(f"Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            tests_failed += 1
    except Exception as e:
        print_fail(f"Login error: {str(e)}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Total Tests: {tests_passed + tests_failed}")
    print(f"Passed: {tests_passed}")
    print(f"Failed: {tests_failed}")
    print()
    
    if tests_failed == 0:
        print("=" * 70)
        print("✓ ALL TESTS PASSED! Email verification system works perfectly!")
        print("=" * 70)
        print("\nWhat was tested:")
        print("1. ✓ User registration")
        print("2. ✓ User starts as inactive")
        print("3. ✓ Verification token generation")
        print("4. ✓ Email verification with token")
        print("5. ✓ User becomes active after verification")
        print("6. ✓ Login works with verified account")
    else:
        print("=" * 70)
        print("✗ SOME TESTS FAILED! Please review the errors above.")
        print("=" * 70)
    
    print(f"\nTest user created:")
    print(f"  Email: {test_email}")
    print(f"  Username: {test_username}")
    print(f"  Password: {test_password}")
    print()

if __name__ == "__main__":
    main()
