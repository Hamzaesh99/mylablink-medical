from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # users should only see their own notifications unless staff
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        # default to current user if not provided
        if not serializer.validated_data.get('user'):
            serializer.save(user=self.request.user)
        else:
            serializer.save()
