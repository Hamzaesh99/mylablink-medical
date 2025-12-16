from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestTypeViewSet

router = DefaultRouter()
router.register(r'types', TestTypeViewSet, basename='testtype')

urlpatterns = [
	path('', include(router.urls)),
]
