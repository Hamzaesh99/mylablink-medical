import os
import sys
import django

# Set up Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.db import connection

print("=" * 70)
print("فحص بنية جدول api_notification")
print("=" * 70)
print()

with connection.cursor() as cursor:
    # Check if table exists
    cursor.execute("""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = DATABASE() 
        AND table_name = 'api_notification'
    """)
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        print("⚠ جدول api_notification غير موجود!")
    else:
        print("✓ جدول api_notification موجود")
        print()
        print("الأعمدة الموجودة:")
        print("-" * 70)
        
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM information_schema.COLUMNS 
            WHERE table_schema = DATABASE() 
            AND table_name = 'api_notification'
            ORDER BY ORDINAL_POSITION
        """)
        
        for column in cursor.fetchall():
            col_name, data_type, nullable, default = column
            nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
            default_str = f" DEFAULT {default}" if default else ""
            print(f"  • {col_name:20s} {data_type:15s} {nullable_str}{default_str}")

print()
print("=" * 70)
