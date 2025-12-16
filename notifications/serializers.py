from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='user')

    class Meta:
        model = Notification
        fields = ['id', 'user', 'user_id', 'type', 'payload', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']
