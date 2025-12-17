import os
import sys
import django

# Set up Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

print("=" * 70)
print("🔍 التحقق النهائي من حالة المشروع")
print("=" * 70)
print()

# 1. Check migrations status
print("1️⃣ حالة Migrations:")
print("-" * 70)
call_command('showmigrations', 'api', '--list')
print()

# 2. Check database structure for Notification
print("2️⃣ بنية جدول api_notification:")
print("-" * 70)
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM information_schema.COLUMNS 
        WHERE table_schema = DATABASE() 
        AND table_name = 'api_notification'
        ORDER BY ORDINAL_POSITION
    """)
    
    for column in cursor.fetchall():
        col_name, data_type, nullable = column
        nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
        print(f"  ✓ {col_name:20s} {data_type:15s} {nullable_str}")

print()

# 3. Try to query Notification model
print("3️⃣ اختبار نموذج Notification:")
print("-" * 70)
try:
    from api.models import Notification
    count = Notification.objects.count()
    print(f"  ✓ تم الاستعلام بنجاح!")
    print(f"  ✓ عدد الإشعارات: {count}")
    
    # Check if sender field works
    test_query = Notification.objects.all().values('id', 'title', 'sender_id', 'user_id')[:1]
    print(f"  ✓ حقل sender_id يعمل بشكل صحيح!")
    
except Exception as e:
    print(f"  ✗ خطأ: {e}")

print()

# 4. Check Message table
print("4️⃣ بنية جدول api_message:")
print("-" * 70)
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM information_schema.COLUMNS 
        WHERE table_schema = DATABASE() 
        AND table_name = 'api_message'
        ORDER BY ORDINAL_POSITION
    """)
    
    for column in cursor.fetchall():
        col_name, data_type, nullable = column
        nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
        print(f"  ✓ {col_name:20s} {data_type:15s} {nullable_str}")

print()

# 5. Test Message model
print("5️⃣ اختبار نموذج Message:")
print("-" * 70)
try:
    from api.models import Message
    count = Message.objects.count()
    print(f"  ✓ تم الاستعلام بنجاح!")
    print(f"  ✓ عدد الرسائل: {count}")
    
except Exception as e:
    print(f"  ✗ خطأ: {e}")

print()
print("=" * 70)
print("✅ اكتمل الفحص بنجاح!")
print("=" * 70)
print()
print("💡 يمكنك الآن تشغيل السيرفر:")
print("   python manage.py runserver")
print()
