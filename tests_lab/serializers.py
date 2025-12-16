from rest_framework import serializers
from .models import TestType

class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = ['id', 'code', 'name', 'description', 'price']
