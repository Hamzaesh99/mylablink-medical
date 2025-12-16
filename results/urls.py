from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestResultViewSet

router = DefaultRouter()
router.register(r'', TestResultViewSet, basename='testresult')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'results'

# Create router and register our viewsets with it
router = DefaultRouter()
router.register(r'', views.TestResultViewSet, basename='testresult')

urlpatterns = [
    # This automatically creates:
    # / - List & Create (GET, POST)
    # /{id}/ - Detail, Update, Delete (GET, PUT, PATCH, DELETE)
    # /{id}/publish/ - Custom action
    # /{id}/download_pdf/ - Custom action
    path('', include(router.urls)),
]
