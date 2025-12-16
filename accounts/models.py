from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid
import secrets


class CustomUser(AbstractUser):
    """
    Custom User model with role-based access.
    Supports two main roles: doctor and patient.
    """
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    # Optional fields for user profile
    phone = models.CharField(max_length=20, blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    governorate = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class AuthenticationLog(models.Model):
    """
    نموذج لتسجيل جميع عمليات المصادقة (تسجيل الدخول وإنشاء الحساب)
    """
    ACTION_CHOICES = [
        ('register', 'إنشاء حساب'),
        ('login', 'تسجيل الدخول'),
        ('login_failed', 'فشل تسجيل الدخول'),
        ('logout', 'تسجيل الخروج'),
        ('password_reset_request', 'طلب إعادة تعيين كلمة المرور'),
        ('password_reset_confirm', 'تأكيد إعادة تعيين كلمة المرور'),
        ('email_verification', 'تفعيل البريد الإلكتروني'),
        ('email_verification_resend', 'إعادة إرسال رابط التفعيل'),
    ]
    
    action = models.CharField(max_length=30, choices=ACTION_CHOICES, verbose_name='العملية')
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='auth_logs',
        verbose_name='المستخدم'
    )
    email = models.EmailField(verbose_name='البريد الإلكتروني', null=True, blank=True)
    username = models.CharField(max_length=150, verbose_name='اسم المستخدم', null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='عنوان IP')
    user_agent = models.TextField(null=True, blank=True, verbose_name='User Agent')
    success = models.BooleanField(default=True, verbose_name='نجحت العملية')
    error_message = models.TextField(null=True, blank=True, verbose_name='رسالة الخطأ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ العملية')
    
    class Meta:
        verbose_name = 'سجل المصادقة'
        verbose_name_plural = 'سجلات المصادقة'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
            models.Index(fields=['email', '-created_at']),
            models.Index(fields=['ip_address', '-created_at']),
        ]
    
    def __str__(self):
        user_info = self.user.username if self.user else (self.username or self.email or 'غير معروف')
        status = 'نجح' if self.success else 'فشل'
        return f"{self.get_action_display()} - {user_info} - {status} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class PendingUser(models.Model):
    """
    نموذج لحفظ بيانات المستخدمين المؤقتة قبل تأكيد البريد الإلكتروني
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password_hash = models.CharField(max_length=255)  # سنحفظ password hash
    role = models.CharField(max_length=10, default='patient')
    phone = models.CharField(max_length=20, blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    governorate = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    
    # Token للتحقق
    verification_token = models.CharField(max_length=100, unique=True, default=secrets.token_urlsafe)
    
    # التواريخ
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # سينتهي بعد 48 ساعة
    
    class Meta:
        verbose_name = 'مستخدم مؤقت'
        verbose_name_plural = 'مستخدمين مؤقتين'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['verification_token']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def is_expired(self):
        """التحقق من انتهاء صلاحية الرابط"""
        return timezone.now() > self.expires_at
    
    def save(self, *args, **kwargs):
        """تعيين تاريخ انتهاء الصلاحية تلقائياً (48 ساعة)"""
        if not self.expires_at:
            from datetime import timedelta
            self.expires_at = timezone.now() + timedelta(hours=48)
        super().save(*args, **kwargs)

