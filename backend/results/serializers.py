from rest_framework import serializers
from .models import TestResult
from tests_lab.serializers import TestTypeSerializer
from accounts.serializers import UserSerializer
from tests_lab.models import TestType
from django.contrib.auth import get_user_model

User = get_user_model()

class TestResultSerializer(serializers.ModelSerializer):
    # read-only nested representation
    test_type = TestTypeSerializer(read_only=True)
    issued_by = UserSerializer(read_only=True)
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='patient'))
    # write-only field to accept test_type id on create/update
    test_type_id = serializers.PrimaryKeyRelatedField(queryset=TestType.objects.all(), write_only=True, source='test_type')

    class Meta:
        model = TestResult
        fields = ['id','patient','test_type','test_type_id','values','status','issued_by','issued_at','published_at','pdf']
        read_only_fields = ['issued_at','published_at','pdf','issued_by']

    def create(self, validated_data):
        # issued_by will be set in the view's perform_create
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
