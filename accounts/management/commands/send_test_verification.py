from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from accounts.utils import send_verification_email


class Command(BaseCommand):
    help = "Send a verification email to a user (create user if needed)."

    def add_arguments(self, parser):
        parser.add_argument('--email', required=True, help='Email address to send verification to')
        parser.add_argument('--create', action='store_true', help='Create a test user if not exists')

    def handle(self, *args, **options):
        User = get_user_model()
        email = options.get('email')
        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f'Found user: {email}'))
        except ObjectDoesNotExist:
            if not options.get('create'):
                self.stderr.write(self.style.ERROR('User not found. Use --create to create a test user.'))
                return
            # create a minimal inactive user
            user = User.objects.create_user(email=email, password='TestPass123')
            user.is_active = False
            # best-effort: set a name if fields exist
            if hasattr(user, 'first_name'):
                try:
                    user.first_name = 'Test'
                except Exception:
                    pass
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created test user: {email} (inactive)'))

        # Use the project's send_verification_email util which respects SITE_BASE_URL when request is None
        try:
            send_verification_email(user, request=None)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to send verification email: {e}'))
            raise

        self.stdout.write(self.style.SUCCESS(f'Verification email sent to {email}'))
