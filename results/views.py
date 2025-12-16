from rest_framework import viewsets, permissions
from .models import TestResult
from .serializers import TestResultSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404

class IsLabOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('admin','staff','doctor')

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

    def get_permissions(self):
        if self.action in ['create','update','partial_update','publish']:
            permission_classes = [IsLabOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        serializer.save(issued_by=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        result = self.get_object()
        result.status = 'published'
        result.published_at = timezone.now()
        result.save()
        # here you could schedule PDF generation and notification task
        return Response({'status':'published'})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def download_pdf(self, request, pk=None):
        result = self.get_object()
        user = request.user
        if not (user == result.patient or user.role in ('admin','doctor','staff')):
            return Response({'detail':'Not allowed'}, status=403)
        if not result.pdf:
            raise Http404("No file")
        return FileResponse(result.pdf.open('rb'), as_attachment=True, filename=f'result_{result.id}.pdf')
