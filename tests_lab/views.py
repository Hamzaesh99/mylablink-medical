from rest_framework import viewsets, permissions
from .models import TestType
from .serializers import TestTypeSerializer

class TestTypeViewSet(viewsets.ModelViewSet):
    queryset = TestType.objects.all()
    serializer_class = TestTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
