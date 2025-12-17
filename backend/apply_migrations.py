import os
import sys
import django

# Set up Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

print("=" * 60)
print("تطبيق التحديثات على قاعدة البيانات")
print("=" * 60)
print()

# Show current migration status
print("حالة Migrations الحالية:")
print("-" * 60)
call_command('showmigrations', 'api')
print()

# Apply migrations
print("=" * 60)
print("تطبيق Migrations...")
print("-" * 60)
try:
    call_command('migrate', 'api', verbosity=2)
    print()
    print("=" * 60)
    print("✓ تم تطبيق Migrations بنجاح!")
    print("=" * 60)
except Exception as e:
    print()
    print("=" * 60)
    print(f"✗ حدث خطأ: {e}")
    print("=" * 60)
    sys.exit(1)

# Show final migration status
print()
print("حالة Migrations النهائية:")
print("-" * 60)
call_command('showmigrations', 'api')
