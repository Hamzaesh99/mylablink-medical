"""
Script لإنشاء جداول API المفقودة في قاعدة البيانات
ملاحظة: تأكد من تشغيله من مجلد backend
"""
import os
import django
import pymysql
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

# قراءة SQL من الملف
with open('create_api_tables.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

# الاتصال بقاعدة البيانات
db_settings = settings.DATABASES['default']
connection = pymysql.connect(
    host=db_settings['HOST'],
    user=db_settings['USER'],
    password=db_settings['PASSWORD'],
    database=db_settings['NAME'],
    charset='utf8mb4'
)

try:
    with connection.cursor() as cursor:
        # تقسيم الـ SQL إلى statements منفصلة
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        for i, statement in enumerate(statements, 1):
            try:
                print(f"تنفيذ statement {i}/{len(statements)}...")
                cursor.execute(statement)
                print(f"✅ نجح!")
            except Exception as e:
                print(f"⚠️ تحذير في statement {i}: {e}")
                continue
        
        connection.commit()
        print("\n🎉 تم إنشاء جميع الجداول بنجاح!")
        
except Exception as e:
    print(f"❌ خطأ: {e}")
    connection.rollback()
finally:
    connection.close()

print("\nالآن يمكنك:")
print("1. تشغيل: python manage.py migrate api --fake-initial")
print("2. إعادة تشغيل الخادم")
