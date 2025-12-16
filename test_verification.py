"""
سكريبت اختبار نظام التحقق من البريد الإلكتروني
يمكن تشغيله من سطر الأوامر لاختبار النظام
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.utils import generate_email_token, verify_email_token, send_verification_email
from django.conf import settings

User = get_user_model()

def test_verification_system():
    """اختبار نظام التحقق من البريد الإلكتروني"""
    
    print("=" * 60)
    print("اختبار نظام التحقق من البريد الإلكتروني")
    print("=" * 60)
    
    # 1. فحص إعدادات البريد الإلكتروني
    print("\n1. إعدادات البريد الإلكتروني:")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   SITE_BASE_URL: {settings.SITE_BASE_URL}")
    
    # 2. البحث عن مستخدم غير مفعّل
    print("\n2. البحث عن مستخدمين غير مفعّلين:")
    inactive_users = User.objects.filter(is_active=False)
    print(f"   عدد المستخدمين غير المفعّلين: {inactive_users.count()}")
    
    if inactive_users.exists():
        for user in inactive_users[:5]:  # عرض أول 5 مستخدمين
            print(f"   - {user.username} ({user.email}) - تاريخ الإنشاء: {user.date_joined}")
    
    # 3. اختبار توليد التوكن
    print("\n3. اختبار توليد التوكن:")
    if inactive_users.exists():
        test_user = inactive_users.first()
        token = generate_email_token(test_user)
        print(f"   التوكن المُولّد: {token[:50]}...")
        
        # 4. اختبار التحقق من التوكن
        print("\n4. اختبار التحقق من التوكن:")
        result = verify_email_token(token)
        print(f"   نتيجة التحقق: {result}")
        
        # 5. بناء رابط التفعيل
        print("\n5. رابط التفعيل:")
        verify_path = f"/api/accounts/verify-email/{token}/"
        verify_url = f"{settings.SITE_BASE_URL}{verify_path}"
        print(f"   {verify_url}")
        
        # 6. اختبار إرسال البريد الإلكتروني
        print("\n6. اختبار إرسال البريد الإلكتروني:")
        try:
            send_verification_email(test_user)
            print("   ✓ تم إرسال البريد الإلكتروني بنجاح")
            print("   (تحقق من الكونسول لرؤية محتوى البريد)")
        except Exception as e:
            print(f"   ✗ فشل إرسال البريد الإلكتروني: {e}")
    else:
        print("   لا يوجد مستخدمين غير مفعّلين للاختبار")
    
    print("\n" + "=" * 60)
    print("انتهى الاختبار")
    print("=" * 60)

if __name__ == '__main__':
    test_verification_system()
