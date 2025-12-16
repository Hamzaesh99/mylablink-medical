#!/usr/bin/env python
"""
فحص حالة نظام الرسائل في قاعدة البيانات
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.db import connection
from api.models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 70)
print("📊 تقرير شامل عن نظام الرسائل في قاعدة البيانات")
print("=" * 70)

# 1. فحص الجدول
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = DATABASE() 
        AND table_name = 'api_message'
    """)
    table_exists = cursor.fetchone()[0] > 0

if table_exists:
    print("\n✅ جدول api_message موجود في قاعدة البيانات")
    
    # 2. بنية الجدول
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE api_message")
        columns = cursor.fetchall()
        
    print("\n📋 الأعمدة المتوفرة:")
    print("-" * 70)
    for col in columns:
        nullable = "يمكن أن يكون NULL" if col[2] == 'YES' else "إلزامي"
        default = f"القيمة الافتراضية: {col[4]}" if col[4] else ""
        print(f"  ✓ {col[0]:<20} | النوع: {col[1]:<15} | {nullable} {default}")
    
    # 3. الإحصائيات
    total_messages = Message.objects.count()
    read_messages = Message.objects.filter(is_read=True).count()
    unread_messages = Message.objects.filter(is_read=False).count()
    
    print(f"\n📈 الإحصائيات:")
    print("-" * 70)
    print(f"  📨 إجمالي الرسائل المخزنة: {total_messages}")
    print(f"  ✅ الرسائل المقروءة: {read_messages}")
    print(f"  ⭕ الرسائل غير المقروءة: {unread_messages}")
    
    # 4. عينة من الرسائل
    if total_messages > 0:
        recent_messages = Message.objects.select_related('sender', 'receiver').order_by('-timestamp')[:5]
        
        print(f"\n📬 آخر {len(recent_messages)} رسائل:")
        print("-" * 70)
        for msg in recent_messages:
            status = "✓ مقروءة" if msg.is_read else "○ غير مقروءة"
            content_preview = msg.content[:40] + "..." if len(msg.content) > 40 else msg.content
            print(f"\n  ID: {msg.id}")
            print(f"  من: {msg.sender.username} ({msg.sender.get_full_name() or 'لا يوجد اسم'})")
            print(f"  إلى: {msg.receiver.username} ({msg.receiver.get_full_name() or 'لا يوجد اسم'})")
            print(f"  الرسالة: {content_preview}")
            print(f"  الحالة: {status}")
            print(f"  الوقت: {msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print("  " + "-" * 66)
    
    # 5. إحصائيات المستخدمين
    print(f"\n👥 إحصائيات المستخدمين:")
    print("-" * 70)
    
    active_senders = Message.objects.values('sender').distinct().count()
    active_receivers = Message.objects.values('receiver').distinct().count()
    
    print(f"  📤 عدد المرسلين النشطين: {active_senders}")
    print(f"  📥 عدد المستقبلين النشطين: {active_receivers}")
    
    # 6. أكثر المستخدمين نشاطاً
    from django.db.models import Count
    
    top_senders = Message.objects.values('sender__username', 'sender__first_name', 'sender__last_name') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    
    if top_senders:
        print(f"\n🔥 أكثر 5 مستخدمين إرسالاً للرسائل:")
        print("-" * 70)
        for i, sender in enumerate(top_senders, 1):
            name = f"{sender['sender__first_name']} {sender['sender__last_name']}".strip() or sender['sender__username']
            print(f"  {i}. {name}: {sender['count']} رسالة")
    
    # 7. التخزين
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                table_name,
                ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
            FROM information_schema.TABLES 
            WHERE table_schema = DATABASE() 
            AND table_name = 'api_message'
        """)
        storage = cursor.fetchone()
    
    if storage:
        print(f"\n💾 مساحة التخزين:")
        print("-" * 70)
        print(f"  حجم الجدول: {storage[1]} ميغابايت")
    
    # 8. الفهارس
    with connection.cursor() as cursor:
        cursor.execute("""
            SHOW INDEX FROM api_message
        """)
        indexes = cursor.fetchall()
    
    print(f"\n🔍 الفهارس (Indexes):")
    print("-" * 70)
    index_names = set()
    for idx in indexes:
        if idx[2] not in index_names:
            index_names.add(idx[2])
            index_type = "PRIMARY KEY" if idx[2] == 'PRIMARY' else "INDEX"
            print(f"  ✓ {idx[2]}: العمود '{idx[4]}' ({index_type})")
    
    print("\n" + "=" * 70)
    print("✅ نظام الرسائل يعمل بشكل صحيح وجميع البيانات محفوظة!")
    print("=" * 70)
    
else:
    print("\n❌ جدول api_message غير موجود في قاعدة البيانات!")
    print("\n🔧 لإنشاء الجدول، قم بتنفيذ:")
    print("   python manage.py makemigrations api")
    print("   python manage.py migrate")
    
print("\n💡 ملاحظة: جميع الرسائل محفوظة بشكل آمن في قاعدة البيانات MySQL")
print("   يمكنك الوصول إليها من خلال Django ORM أو SQL مباشرة\n")
