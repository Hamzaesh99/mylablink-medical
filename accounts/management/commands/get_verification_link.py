from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from accounts.utils import generate_email_token


class Command(BaseCommand):
    help = 'Generate email verification link for inactive users'

    def handle(self, *args, **options):
        # Get all inactive users
        inactive_users = CustomUser.objects.filter(is_active=False)
        
        if not inactive_users.exists():
            self.stdout.write(self.style.WARNING('No inactive users found!'))
            self.stdout.write('All users are already activated.')
            return
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('INACTIVE USERS:'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        for user in inactive_users:
            token = generate_email_token(user)
            link = f"http://127.0.0.1:8000/api/accounts/verify-email/{token}/"
            
            self.stdout.write('')
            self.stdout.write(f"User: {user.username}")
            self.stdout.write(f"Email: {user.email}")
            self.stdout.write(f"Name: {user.first_name or 'N/A'}")
            self.stdout.write(self.style.WARNING('-' * 70))
            self.stdout.write(self.style.SUCCESS('VERIFICATION LINK:'))
            self.stdout.write(self.style.HTTP_INFO(link))
            self.stdout.write(self.style.WARNING('-' * 70))
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('INSTRUCTIONS:'))
        self.stdout.write('1. Copy the verification link above')
        self.stdout.write('2. Paste it in your browser')
        self.stdout.write('3. Press Enter')
        self.stdout.write('4. The account will be activated!')
        self.stdout.write(self.style.SUCCESS('=' * 70))
