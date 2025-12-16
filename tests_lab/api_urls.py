from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TestTypeViewSet

router = DefaultRouter()
router.register(r'test-types', TestTypeViewSet, basename='testtypes')

urlpatterns = [
    path('', include(router.urls)),
]
