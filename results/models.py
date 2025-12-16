from django.db import models
from django.conf import settings
from tests_lab.models import TestType


class TestResult(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('critical', 'Critical'),
    )
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    values = models.JSONField()  # flexible because values may vary
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='issued_results')
    issued_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    pdf = models.FileField(upload_to='results_pdfs/', null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_type.name} - {self.patient.username}"
