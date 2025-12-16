from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from accounts.views import ActivatedTokenObtainPairView

urlpatterns = [
    # Django admin (built-in) - MUST be first!
    path('admin/', admin.site.urls),
    
    # Frontend pages served as templates
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html'), name='home-html'),
    path('auth.html', TemplateView.as_view(template_name='auth.html'), name='auth'),
    path('auth/', TemplateView.as_view(template_name='auth.html'), name='auth-page'),
    path('email-check/', TemplateView.as_view(template_name='email-check.html'), name='email-check'),
    path('email-verified-success/', TemplateView.as_view(template_name='email-verified-success.html'), name='email-verified-success'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard_patient.html'), name='dashboard'),
    path('reset-password/', TemplateView.as_view(template_name='reset_password.html'), name='reset-password'),
    
    # Direct file access paths (matching frontend links)
    path('archive.html', TemplateView.as_view(template_name='archive.html'), name='archive'),
    path('dashboard_doctor.html', TemplateView.as_view(template_name='dashboard_doctor.html'), name='dashboard-doctor'),

    path('settings_doctor.html', TemplateView.as_view(template_name='settings_doctor.html'), name='settings-doctor'),
    path('notifications_doctor.html', TemplateView.as_view(template_name='notifications_doctor.html'), name='notifications-doctor'),
    path('messages_doctor.html', TemplateView.as_view(template_name='messages_doctor.html'), name='messages-doctor'),
    path('settings_patient.html', TemplateView.as_view(template_name='settings_patient.html'), name='settings-patient'),
    path('dashboard_patient.html', TemplateView.as_view(template_name='dashboard_patient.html'), name='dashboard-patient'),

    path('messages_patient.html', TemplateView.as_view(template_name='messages_patient.html'), name='messages-patient'),
    path('tips_patient.html', TemplateView.as_view(template_name='tips_patient.html'), name='tips-patient'),
    path('notifications_patient.html', TemplateView.as_view(template_name='notifications_patient.html'), name='notifications-patient'),

    # Per-role dashboards (serve the frontend HTML files under frontend/<role>/dashboard.html)
    path('patient/dashboard/', TemplateView.as_view(template_name='dashboard_patient.html'), name='patient-dashboard'),
    path('patient/dashboard.html', TemplateView.as_view(template_name='dashboard_patient.html'), name='patient-dashboard-html'),
    path('doctor/dashboard/', TemplateView.as_view(template_name='dashboard_doctor.html'), name='doctor-dashboard'),
    path('doctor/dashboard.html', TemplateView.as_view(template_name='dashboard_doctor.html'), name='doctor-dashboard-html'),
    path('admin-panel/', TemplateView.as_view(template_name='admin/index.html'), name='admin-dashboard'),
    path('email-sent-confirmation/', TemplateView.as_view(template_name='account/email_sent_confirmation.html'), name='email-sent-confirmation'),

    # JWT auth
    path('api/auth/token/', ActivatedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API modules
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('api/notifications/', include('notifications.urls')),

    # django-allauth routes
    path('accounts/', include('allauth.urls')),
]

# Serve static & media during development
if settings.DEBUG:
    # Serve files from STATICFILES_DIRS (frontend/assets, backend/static) during development
    urlpatterns += staticfiles_urlpatterns()
    # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
