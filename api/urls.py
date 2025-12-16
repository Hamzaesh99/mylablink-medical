from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'test-types', views.TestTypeViewSet)
router.register(r'results', views.ResultViewSet)
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'testimonials', views.TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('', include(router.urls)),
]
