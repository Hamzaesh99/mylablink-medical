from django.contrib import admin
from .models import Patient, TestType, Result, File, Doctor, Message, Notification, Testimonial

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'dob')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty')
    search_fields = ('user__username', 'user__email', 'specialty')

@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test_type', 'status', 'issued_by', 'issued_at')
    list_filter = ('status', 'issued_at', 'test_type')
    search_fields = ('patient__user__username', 'patient__user__email')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('result', 'file', 'uploaded_at')



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('user__username', 'content')
