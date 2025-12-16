from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone = models.CharField(max_length=30, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

class TestType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Result(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='results')
    test_type = models.ForeignKey(TestType, on_delete=models.SET_NULL, null=True)
    value = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='completed')
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='api_issued_results')
    issued_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result {self.id} for {self.patient}"

class File(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='results/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# --- جداول جديدة: الطبيب، المواعيد، الرسائل، الإشعارات ---

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=150, verbose_name="التخصص", default="عام")
    bio = models.TextField(blank=True, verbose_name="نبذة عن الطبيب")
    schedule = models.TextField(blank=True, verbose_name="جدول المواعيد", help_text="مثال: الأحد - الخميس: 9ص - 5م")

    def __str__(self):
        return f"د. {self.user.get_full_name() or self.user.username}"



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="المرسل", null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name="المستقبل", null=True, blank=True)
    content = models.TextField(verbose_name="نص الرسالة", default='', blank=True, null=True)
    file_attachment = models.FileField(upload_to='chat_files/', blank=True, null=True, verbose_name="مرفق")
    is_read = models.BooleanField(default=False, verbose_name="تمت القراءة")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="وقت الإرسال")

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'رسالة'
        verbose_name_plural = 'الرسائل'

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="المستخدم")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='triggered_notifications', verbose_name="المرسل")
    title = models.CharField(max_length=255, verbose_name="العنوان")
    message = models.TextField(verbose_name="الرسالة")
    is_read = models.BooleanField(default=False, verbose_name="تمت القراءة")
    result = models.ForeignKey('Result', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications', verbose_name="النتيجة المرتبطة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'إشعار'
        verbose_name_plural = 'الإشعارات'

    def __str__(self):
        return f"{self.title} - {self.user}"

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials', verbose_name="المستخدم")
    content = models.TextField(verbose_name="نص الرأي")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="التقييم")
    is_approved = models.BooleanField(default=False, verbose_name="تمت الموافقة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'رأي مستخدم'
        verbose_name_plural = 'آراء المستخدمين'

    def __str__(self):
        return f"رأي من {self.user.get_full_name() or self.user.username}"
