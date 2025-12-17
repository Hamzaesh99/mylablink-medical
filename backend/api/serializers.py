from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, TestType, Result, File, Notification, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'avatar']



class MessageSerializer(serializers.ModelSerializer):

    sender_info = UserSerializer(source='sender', read_only=True)
    receiver_info = UserSerializer(source='receiver', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_info', 'receiver', 'receiver_info', 'content', 'file_attachment', 'file_url', 'is_read', 'timestamp']
        read_only_fields = ['sender', 'timestamp']
    
    def get_file_url(self, obj):
        if obj.file_attachment:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file_attachment.url)
            return obj.file_attachment.url
        return None

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'user', 'phone', 'dob']

class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = ['id', 'name', 'description']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'uploaded_at']

class ResultSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    test_type_info = TestTypeSerializer(source='test_type', read_only=True)
    patient_info = PatientSerializer(source='patient', read_only=True)
    issued_by_info = UserSerializer(source='issued_by', read_only=True)

    class Meta:
        model = Result
        fields = ['id', 'patient', 'patient_info', 'test_type', 'test_type_info', 'value', 'notes', 'status', 'issued_by', 'issued_by_info', 'issued_at', 'created_at', 'files']

class NotificationSerializer(serializers.ModelSerializer):
    result_info = ResultSerializer(source='result', read_only=True)

    sender_info = UserSerializer(source='sender', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'sender', 'sender_info', 'title', 'message', 'is_read', 'created_at', 'result', 'result_info']


from .models import Testimonial

class TestimonialSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Testimonial
        fields = ['id', 'user', 'user_info', 'content', 'rating', 'is_approved', 'created_at']
        read_only_fields = ['user', 'is_approved', 'created_at']

