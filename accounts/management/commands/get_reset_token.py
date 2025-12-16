from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from accounts.utils import generate_password_reset_token


class Command(BaseCommand):
    help = 'Generate password reset token for a user'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='User email address')

    def handle(self, *args, **options):
        email = options.get('email')
        
        if not email:
            # Show all users
            users = CustomUser.objects.all()
            
            if not users.exists():
                self.stdout.write(self.style.WARNING('No users found!'))
                return
            
            self.stdout.write(self.style.SUCCESS('=' * 70))
            self.stdout.write(self.style.SUCCESS('AVAILABLE USERS:'))
            self.stdout.write(self.style.SUCCESS('=' * 70))
            
            for user in users:
                status = "✓ Active" if user.is_active else "✗ Inactive"
                self.stdout.write(f"{user.email:40s} | {status}")
            
            self.stdout.write(self.style.SUCCESS('=' * 70))
            self.stdout.write('')
            self.stdout.write('Usage: python manage.py get_reset_token --email=user@example.com')
            return
        
        # Get user by email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with email {email} not found!'))
            return
        
        # Generate token
        token = generate_password_reset_token(user)
        
        # Generate URLs
        reset_url = f"http://127.0.0.1:8000/reset-password/?token={token}"
        api_url = f"http://127.0.0.1:8000/api/accounts/password-reset/confirm/"
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('PASSWORD RESET TOKEN GENERATED'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        self.stdout.write(f'User: {user.username}')
        self.stdout.write(f'Email: {user.email}')
        self.stdout.write(f'Active: {user.is_active}')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('-' * 70))
        self.stdout.write(self.style.WARNING('RESET TOKEN:'))
        self.stdout.write(self.style.WARNING('-' * 70))
        self.stdout.write(self.style.HTTP_INFO(token))
        self.stdout.write(self.style.WARNING('-' * 70))
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('-' * 70))
        self.stdout.write(self.style.WARNING('FRONTEND RESET URL:'))
        self.stdout.write(self.style.WARNING('-' * 70))
        self.stdout.write(self.style.HTTP_INFO(reset_url))
        self.stdout.write(self.style.WARNING('-' * 70))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('TESTING INSTRUCTIONS:'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        self.stdout.write('1. Copy the TOKEN above')
        self.stdout.write('2. Use it in Postman or PowerShell script:')
        self.stdout.write('')
        self.stdout.write(f'   POST {api_url}')
        self.stdout.write('   Content-Type: application/json')
        self.stdout.write('')
        self.stdout.write('   Body:')
        self.stdout.write('   {')
        self.stdout.write(f'     "token": "{token}",')
        self.stdout.write('     "new_password": "NewPass123!",')
        self.stdout.write('     "new_password_confirm": "NewPass123!"')
        self.stdout.write('   }')
        self.stdout.write('')
        self.stdout.write('3. Or run: .\\test_password_reset_confirm.ps1')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.WARNING('NOTE: Token is valid for 24 hours'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
