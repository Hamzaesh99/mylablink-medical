from django.conf import settings
from django.core import signing
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.http import url_has_allowed_host_and_scheme

SALT = 'email-verify'
MAX_AGE = 60 * 60 * 48  # 48 hours


def log_authentication(action, request, user=None, email=None, username=None, success=True, error_message=None):
    """
    دالة مساعدة لتسجيل عمليات المصادقة في قاعدة البيانات
    
    Args:
        action: نوع العملية (register, login, login_failed, etc.)
        request: HttpRequest object للحصول على IP و User Agent
        user: المستخدم (إن وجد)
        email: البريد الإلكتروني
        username: اسم المستخدم
        success: هل نجحت العملية
        error_message: رسالة الخطأ (إن وجدت)
    """
    try:
        from .models import AuthenticationLog
        
        # الحصول على IP address
        ip_address = None
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
        
        # الحصول على User Agent
        user_agent = None
        if request:
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]  # Limit length
        
        # الحصول على email أو username من user إن كان موجوداً
        if user:
            email = email or user.email
            username = username or user.username
        
        AuthenticationLog.objects.create(
            action=action,
            user=user,
            email=email,
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=error_message
        )
    except Exception as e:
        # لا نريد أن تفشل العملية الرئيسية بسبب فشل التسجيل
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to log authentication: {e}")


def generate_email_token(user):
    payload = {'uid': user.pk, 'email': user.email}
    return signing.dumps(payload, salt=SALT)


def verify_email_token(token):
    try:
        data = signing.loads(token, salt=SALT, max_age=MAX_AGE)
        return {'ok': True, 'data': data}
    except signing.SignatureExpired:
        return {'ok': False, 'error': 'expired'}
    except signing.BadSignature:
        return {'ok': False, 'error': 'bad'}


def build_absolute_uri(request, path: str) -> str:
    if request is not None:
        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        return f"{scheme}://{host}{path}"
    base = getattr(settings, 'SITE_BASE_URL', 'http://127.0.0.1:8000')
    return f"{base}{path}"


def send_verification_email(user, request=None):
    token = generate_email_token(user)
    verify_path = f"/api/accounts/verify-email/{token}/"
    verify_url = build_absolute_uri(request, verify_path)

    context = {
        'app_name': 'MyLabLink',
        'user': user,
        'verify_url': verify_url,
    }
    subject = 'تفعيل حسابك في MyLabLink'
    html_body = render_to_string('emails/verify_email.html', context)

    message = EmailMultiAlternatives(
        subject=subject,
        body=(
            'يرجى فتح الرسالة بصيغة HTML لعرض رابط التفعيل.\n\n'
            f'رابط التفعيل المباشر (نسخ/لصق في المتصفح):\n{verify_url}\n'
        ),
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
        to=[user.email],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=False)


def send_pending_verification_email(pending_user, request=None):
    """إرسال بريد التحقق للمستخدم المؤقت (PendingUser)"""
    verify_path = f"/api/accounts/confirm-registration/{pending_user.verification_token}/"
    verify_url = build_absolute_uri(request, verify_path)

    # 🔍 DEBUG: طباعة معلومات البريد الإلكتروني
    print("\n" + "="*80)
    print("📧 EMAIL SENDING DEBUG INFO")
    print("="*80)
    print(f"🎯 To: {pending_user.email}")
    print(f"📤 From: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'NOT SET')}")
    print(f"🔗 Verification URL: {verify_url}")
    print(f"⚙️  EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'NOT SET')}")
    print(f"🌐 EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'NOT SET')}")
    print(f"🔌 EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'NOT SET')}")
    print(f"👤 EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'NOT SET')}")
    print(f"🔐 EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'NOT SET')}")
    print("="*80)

    context = {
        'app_name': 'MyLabLink',
        'user_name': pending_user.first_name or pending_user.email,
        'verify_url': verify_url,
    }
    subject = 'تأكيد إنشاء حسابك في MyLabLink'
    
    html_body = f"""
    <html dir="rtl">
    <body style="font-family: 'Tajawal', Arial, sans-serif; direction: rtl; text-align: right; background-color: #f9fafb; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #000; font-weight: 900; font-size: 32px; margin: 0;">MyLabLink</h1>
                <p style="color: #667eea; font-size: 14px; margin-top: 5px;">نظام إدارة المختبرات الطبية</p>
            </div>
            
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px;">
                <h2 style="color: white; margin: 0; font-size: 24px;">مرحباً بك!</h2>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">
                    أهلاً {context['user_name']} 👋
                </p>
            </div>
            
            <div style="padding: 0 10px;">
                <p style="color: #4b5563; font-size: 16px; line-height: 1.8; margin-bottom: 25px;">
                    شكراً لاختيارك MyLabLink! لإكمال إنشاء حسابك وتفعيله، يرجى النقر على الزر أدناه:
                </p>
                
                <div style="text-align: center; margin: 35px 0;">
                    <a href="{verify_url}" style="background: linear-gradient(135deg, #FF1744 0%, #FF5252 50%, #FF6E40 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 10px; display: inline-block; font-weight: bold; font-size: 16px; box-shadow: 0 4px 15px rgba(255, 23, 68, 0.4);">
                        ✓ تأكيد الحساب الآن
                    </a>
                </div>
                
                <div style="background: #fef3c7; border-right: 4px solid #f59e0b; padding: 15px; border-radius: 8px; margin: 25px 0;">
                    <p style="color: #92400e; margin: 0; font-size: 14px;">
                        <strong>⏰ مهم:</strong> هذا الرابط صالح لمدة 48 ساعة فقط.
                    </p>
                </div>
                
                <p style="color: #6b7280; font-size: 14px; margin-top: 25px;">
                    إذا لم تقم بإنشاء حساب في MyLabLink، يرجى تجاهل هذه الرسالة.
                </p>
                
                <p style="color: #9ca3af; font-size: 12px; margin-top: 15px;">
                    أو انسخ الرابط التالي في المتصفح:<br>
                    <span style="color: #667eea; word-break: break-all;">{verify_url}</span>
                </p>
            </div>
            
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
            
            <p style="color: #9ca3af; font-size: 12px; text-align: center; margin: 0;">
                © 2025 MyLabLink - جميع الحقوق محفوظة
            </p>
        </div>
    </body>
    </html>
    """

    try:
        print("📮 Attempting to send email...")
        message = EmailMultiAlternatives(
            subject=subject,
            body=(
                f'مرحباً {context["user_name"]},\n\n'
                'شكراً لاختيارك MyLabLink!\n\n'
                f'لتأكيد حسابك، يرجى فتح الرابط التالي:\n{verify_url}\n\n'
                'هذا الرابط صالح لمدة 48 ساعة.\n\n'
                'إذا لم تقم بإنشاء هذا الحساب، يرجى تجاهل هذه الرسالة.\n'
            ),
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            to=[pending_user.email],
        )
        message.attach_alternative(html_body, 'text/html')
        result = message.send(fail_silently=False)
        print(f"✅ Email sent successfully! Result: {result}")
        print("="*80 + "\n")
    except Exception as e:
        print(f"❌ ERROR sending email: {type(e).__name__}: {str(e)}")
        print("="*80 + "\n")
        raise  # Re-raise the exception to handle it in views.py


# Password Reset utilities
RESET_SALT = 'password-reset'
RESET_MAX_AGE = 60 * 60 * 24  # 24 hours


def generate_password_reset_token(user):
    """توليد توكن لإعادة تعيين كلمة المرور"""
    payload = {'uid': user.pk, 'email': user.email}
    return signing.dumps(payload, salt=RESET_SALT)


def verify_password_reset_token(token):
    """التحقق من توكن إعادة تعيين كلمة المرور"""
    try:
        data = signing.loads(token, salt=RESET_SALT, max_age=RESET_MAX_AGE)
        return {'ok': True, 'data': data}
    except signing.SignatureExpired:
        return {'ok': False, 'error': 'expired'}
    except signing.BadSignature:
        return {'ok': False, 'error': 'bad'}


def send_password_reset_email(user, request=None):
    """إرسال بريد إلكتروني لإعادة تعيين كلمة المرور"""
    token = generate_password_reset_token(user)
    reset_path = f"/reset-password/?token={token}"
    reset_url = build_absolute_uri(request, reset_path)

    context = {
        'app_name': 'MyLabLink',
        'user': user,
        'reset_url': reset_url,
        'token': token,
    }
    subject = 'إعادة تعيين كلمة المرور - MyLabLink'
    
    # استخدام template بسيط إذا لم يكن موجود
    try:
        html_body = render_to_string('emails/password_reset.html', context)
    except:
        html_body = f"""
        <html dir="rtl">
        <body style="font-family: Arial, sans-serif; direction: rtl; text-align: right;">
            <h2>مرحباً {user.first_name or user.username}</h2>
            <p>تلقينا طلباً لإعادة تعيين كلمة المرور لحسابك في MyLabLink.</p>
            <p>لإعادة تعيين كلمة المرور، يرجى النقر على الرابط التالي:</p>
            <p><a href="{reset_url}" style="background: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block;">إعادة تعيين كلمة المرور</a></p>
            <p>أو انسخ الرابط التالي في المتصفح:</p>
            <p style="background: #f3f4f6; padding: 10px; border-radius: 4px; word-break: break-all;">{reset_url}</p>
            <p><strong>رمز التحقق:</strong> <code style="background: #fef3c7; padding: 4px 8px; border-radius: 4px;">{token}</code></p>
            <p style="color: #dc2626; font-weight: bold;">هذا الرابط صالح لمدة 24 ساعة فقط.</p>
            <p>إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذه الرسالة.</p>
            <hr>
            <p style="color: #6b7280; font-size: 12px;">MyLabLink - نظام إدارة نتائج المختبرات الطبية</p>
        </body>
        </html>
        """

    message = EmailMultiAlternatives(
        subject=subject,
        body=(
            f'مرحباً {user.first_name or user.username},\n\n'
            'تلقينا طلباً لإعادة تعيين كلمة المرور لحسابك.\n\n'
            f'رابط إعادة التعيين:\n{reset_url}\n\n'
            f'رمز التحقق: {token}\n\n'
            'هذا الرابط صالح لمدة 24 ساعة فقط.\n\n'
            'إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذه الرسالة.\n'
        ),
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
        to=[user.email],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=False)


# OTP Utilities
import random
import string
from django.core.cache import cache

def generate_otp(length=6):
    """Generate a numeric OTP"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(user, request=None):
    """Send OTP via email for password reset"""
    otp = generate_otp()
    # Store OTP in cache for 5 minutes
    # Key format: password_reset_otp_<email>
    cache_key = f'password_reset_otp_{user.email}'
    cache.set(cache_key, otp, 300)  # 5 minutes expiration

    # Print OTP to console for development/testing
    print("\n" + "="*60)
    print(f"🔐 PASSWORD RESET OTP FOR: {user.email}")
    print(f"📧 OTP CODE: {otp}")
    print(f"⏰ Valid for 5 minutes")
    print("="*60 + "\n")

    context = {
        'user': user,
        'otp': otp,
    }
    subject = 'رمز التحقق لإعادة تعيين كلمة المرور - MyLabLink'
    
    html_body = f"""
    <html dir="rtl">
    <body style="font-family: 'Tajawal', Arial, sans-serif; direction: rtl; text-align: right; background-color: #f9fafb; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="color: #000; font-weight: 900;">MyLabLink</h2>
            </div>
            
            <h3 style="color: #1a1a1a; margin-bottom: 20px;">مرحباً {user.first_name or user.username}</h3>
            
            <p style="color: #4b5563; font-size: 16px; line-height: 1.6;">
                تلقينا طلباً لإعادة تعيين كلمة المرور الخاصة بحسابك.
                استخدم رمز التحقق التالي لإتمام العملية:
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <div style="background: #f3f4f6; color: #1f2937; font-size: 32px; font-weight: bold; letter-spacing: 5px; padding: 15px 30px; border-radius: 8px; display: inline-block; border: 2px dashed #d1d5db;">
                    {otp}
                </div>
            </div>
            
            <p style="color: #dc2626; font-size: 14px; font-weight: bold; text-align: center;">
                هذا الرمز صالح لمدة 5 دقائق فقط.
            </p>
            
            <p style="color: #4b5563; font-size: 14px; margin-top: 30px;">
                إذا لم تطلب هذا الرمز، يرجى تجاهل هذه الرسالة أو التواصل مع الدعم الفني.
            </p>
            
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
            
            <p style="color: #9ca3af; font-size: 12px; text-align: center;">
                MyLabLink - منصة إدارة المختبرات الطبية الذكية
            </p>
        </div>
    </body>
    </html>
    """

    message = EmailMultiAlternatives(
        subject=subject,
        body=f'رمز التحقق الخاص بك هو: {otp}',
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
        to=[user.email],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=False)

