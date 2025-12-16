#!/usr/bin/env python
"""
فحص وإنشاء جدول الرسائل في قاعدة البيانات
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.db import connection
from api.models import Message, User
from django.contrib.auth import get_user_model

def check_message_table():
    """فحص جدول الرسائل"""
    print("=" * 60)
    print("🔍 فحص جدول الرسائل في قاعدة البيانات")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # 1. فحص وجود الجدول
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name = 'api_message'
        """)
        table_exists = cursor.fetchone()[0] > 0
        
        if table_exists:
            print("✅ جدول api_message موجود في قاعدة البيانات")
            
            # 2. عرض بنية الجدول
            cursor.execute("DESCRIBE api_message")
            columns = cursor.fetchall()
            
            print("\n📋 بنية جدول الرسائل:")
            print("-" * 60)
            for col in columns:
                print(f"  - {col[0]}: {col[1]} {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
            
            # 3. عدد الرسائل
            cursor.execute("SELECT COUNT(*) FROM api_message")
            count = cursor.fetchone()[0]
            print(f"\n📊 إجمالي الرسائل المخزنة: {count}")
            
            # 4. عرض آخر 5 رسائل
            if count > 0:
                cursor.execute("""
                    SELECT id, sender_id, receiver_id, 
                           LEFT(content, 50) as preview,
                           is_read, timestamp 
                    FROM api_message 
                    ORDER BY timestamp DESC 
                    LIMIT 5
                """)
                messages = cursor.fetchall()
                
                print("\n📨 آخر 5 رسائل:")
                print("-" * 60)
                for msg in messages:
                    read_status = "✓ مقروءة" if msg[4] else "○ غير مقروءة"
                    print(f"  ID: {msg[0]} | من: {msg[1]} إلى: {msg[2]}")
                    print(f"    النص: {msg[3]}...")
                    print(f"    الحالة: {read_status} | الوقت: {msg[5]}")
                    print("-" * 60)
            
            # 5. إحصائيات
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN is_read = 1 THEN 1 ELSE 0 END) as read_count,
                    SUM(CASE WHEN is_read = 0 THEN 1 ELSE 0 END) as unread_count
                FROM api_message
            """)
            stats = cursor.fetchone()
            
            print(f"\n📈 إحصائيات الرسائل:")
            print(f"  - إجمالي الرسائل: {stats[0]}")
            print(f"  - الرسائل المقروءة: {stats[1]}")
            print(f"  - الرسائل غير المقروءة: {stats[2]}")
            
        else:
            print("❌ جدول api_message غير موجود!")
            print("\n💡 لإنشاء الجدول، قم بتنفيذ:")
            print("   python manage.py makemigrations api")
            print("   python manage.py migrate")

def test_message_operations():
    """اختبار عمليات الرسائل"""
    print("\n" + "=" * 60)
    print("🧪 اختبار عمليات الرسائل")
    print("=" * 60)
    
    try:
        # التحقق من وجود مستخدمين
        User = get_user_model()
        users = User.objects.all()[:2]
        
        if len(users) < 2:
            print("⚠️  يجب وجود مستخدمين على الأقل للاختبار")
            return
        
        user1, user2 = users[0], users[1]
        print(f"✅ مستخدمين للاختبار: {user1.username} و {user2.username}")
        
        # إنشاء رسالة تجريبية
        test_message = Message.objects.create(
            sender=user1,
            receiver=user2,
            content="رسالة تجريبية من نظام فحص قاعدة البيانات",
            is_read=False
        )
        print(f"✅ تم إنشاء رسالة تجريبية برقم: {test_message.id}")
        
        # قراءة الرسالة
        messages = Message.objects.filter(sender=user1, receiver=user2)
        print(f"✅ تم جلب {messages.count()} رسالة من قاعدة البيانات")
        
        # تعليم كمقروءة
        test_message.is_read = True
        test_message.save()
        print(f"✅ تم تعليم الرسالة كمقروءة")
        
        # حذف الرسالة التجريبية
        test_message.delete()
        print(f"✅ تم حذف الرسالة التجريبية")
        
        print("\n✨ جميع عمليات قاعدة البيانات تعمل بشكل صحيح!")
        
    except Exception as e:
        print(f"❌ خطأ أثناء الاختبار: {str(e)}")

def show_database_schema():
    """عرض مخطط قاعدة البيانات للرسائل"""
    print("\n" + "=" * 60)
    print("🗂️  مخطط قاعدة البيانات - نظام الرسائل")
    print("=" * 60)
    
    schema = """
    جدول: api_message
    ==================
    
    الحقول:
    --------
    - id (INT, PRIMARY KEY, AUTO_INCREMENT)
      المعرف الفريد للرسالة
    
    - sender_id (INT, FOREIGN KEY -> accounts_user.id)
      معرف المستخدم المرسل
    
    - receiver_id (INT, FOREIGN KEY -> accounts_user.id)
      معرف المستخدم المستقبل
    
    - content (TEXT)
      محتوى الرسالة النصي
    
    - file_attachment (VARCHAR, NULLABLE)
      مسار الملف المرفق (اختياري)
    
    - is_read (BOOLEAN, DEFAULT=0)
      حالة القراءة (0 = غير مقروءة, 1 = مقروءة)
    
    - timestamp (DATETIME, AUTO_NOW_ADD)
      وقت إرسال الرسالة
    
    الفهارس:
    ---------
    - PRIMARY KEY: id
    - INDEX: sender_id
    - INDEX: receiver_id
    - INDEX: timestamp
    - INDEX: is_read
    
    العلاقات:
    ---------
    - sender -> accounts_user (Many-to-One)
    - receiver -> accounts_user (Many-to-One)
    
    الميزات:
    ---------
    ✓ التخزين الآمن للرسائل
    ✓ تتبع حالة القراءة
    ✓ دعم المرفقات
    ✓ ترتيب زمني
    ✓ فهرسة للأداء العالي
    """
    
    print(schema)

if __name__ == '__main__':
    check_message_table()
    test_message_operations()
    show_database_schema()
    
    print("\n" + "=" * 60)
    print("✅ تم الانتهاء من الفحص")
    print("=" * 60)
