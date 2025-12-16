from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from api.models import Patient

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'national_id', 'governorate', 'avatar']
        read_only_fields = ['id', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm password')
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='patient', required=False)
    national_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    governorate = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'password2', 'role', 'phone', 'national_id', 'governorate', 'dob']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs.get('password') != attrs.pop('password2', None):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def validate_national_id(self, value):
        # Ensure national_id is unique (if provided)
        if value:
            qs = User.objects.filter(national_id=value)
            if qs.exists():
                raise serializers.ValidationError('رقم الهوية مسجل بالفعل. يرجى التحقق أو التواصل مع الدعم.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role', 'patient')
        dob = validated_data.pop('dob', None)

        user = User(**validated_data)
        # Require email verification before login
        user.is_active = False
        user.role = role
        user.set_password(password)
        user.save()

        # إذا كان الدور مريض، ننشئ سجل Patient مرتبط مع تاريخ الميلاد (إن وجد)
        if role == 'patient':
            Patient.objects.create(user=user, dob=dob)

        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """طلب إعادة تعيين كلمة المرور عبر البريد الإلكتروني"""
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """تأكيد إعادة تعيين كلمة المرور بالرمز OTP"""
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, min_length=6, max_length=6)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({'new_password_confirm': 'كلمتا المرور غير متطابقتين.'})
        
        # التحقق من قوة كلمة المرور
        try:
            validate_password(attrs.get('new_password'))
        except Exception as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """تغيير كلمة المرور للمستخدم المسجل"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('كلمة المرور الحالية غير صحيحة.')
        return value

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({'new_password_confirm': 'كلمتا المرور غير متطابقتين.'})
        
        # التحقق من قوة كلمة المرور
        try:
            validate_password(attrs.get('new_password'))
        except Exception as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

