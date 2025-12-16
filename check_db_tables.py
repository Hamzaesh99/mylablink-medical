"""
فحص الجداول الموجودة في قاعدة البيانات
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.db import connection

def check_tables():
    """عرض جميع الجداول في قاعدة البيانات"""
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("=" * 60)
        print("الجداول الموجودة في قاعدة البيانات:")
        print("=" * 60)
        
        if tables:
            for table in tables:
                print(f"  ✓ {table[0]}")
        else:
            print("  ⚠ لا توجد جداول في قاعدة البيانات!")
        
        print("\n" + "=" * 60)
        print("البحث عن جدول accounts_customuser:")
        print("=" * 60)
        
        table_names = [t[0] for t in tables]
        if 'accounts_customuser' in table_names:
            print("  ✓ الجدول موجود")
        else:
            print("  ✗ الجدول غير موجود!")
            print("\n  💡 الحل: تنفيذ الأمر التالي:")
            print("     python manage.py migrate --run-syncdb")

if __name__ == '__main__':
    check_tables()
