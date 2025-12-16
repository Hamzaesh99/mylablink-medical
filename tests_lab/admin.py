from django.contrib import admin
from .models import TestType


@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price')
    search_fields = ('code', 'name')
