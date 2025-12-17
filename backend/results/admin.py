from django.contrib import admin
from .models import TestResult


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_type', 'patient', 'status', 'issued_at')
    list_filter = ('status', 'is_archived')
    search_fields = ('patient__username', 'test_type__name')
