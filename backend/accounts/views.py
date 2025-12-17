from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, RegisterSerializer, 
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    ChangePasswordSerializer
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache import cache
from .utils import (
    send_verification_email, verify_email_token,
    send_password_reset_email, verify_password_reset_token,
    send_otp_email,
    log_authentication
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Public create (although we also expose a RegisterView)
        if self.action == 'create':
            return [permissions.AllowAny()]

        # Allow authenticated users (doctors) to list patients
        if self.action == 'list':
            return [permissions.IsAuthenticated()]

        # For retrieve/update/destroy, allow the user themself or admins
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdminOrSelf()]

        # Default: authenticated
        return [permissions.IsAuthenticated()]


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        from .models import PendingUser
        from django.contrib.auth.hashers import make_password
        from datetime import timedelta
        from django.utils import timezone
        from .utils import send_pending_verification_email
        
        data = request.data.copy()
        
        # التحقق من البيانات الأساسية
        email = data.get('email')
        username = data.get('username') or email
        password = data.get('password')
        password2 = data.get('password2')
        role = data.get('role', 'patient')
        
        # ✅ التحقق من صحة نوع الحساب (منع رفع الصلاحيات للمسؤول)
        ALLOWED_ROLES = ['patient', 'doctor']
        if role not in ALLOWED_ROLES:
            return Response({
                'detail': 'نوع الحساب غير صحيح. يرجى اختيار مريض أو طبيب.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not email or not password:
            return Response({
                'detail': 'البريد الإلكتروني وكلمة المرور مطلوبان.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if password != password2:
            return Response({
                'detail': 'كلمتا المرور غير متطابقتين.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(password) < 8:
            return Response({
                'detail': 'كلمة المرور يجب أن تكون 8 أحرف على الأقل.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # التحقق من أن البريد غير مستخدم
        if User.objects.filter(email=email).exists():
            return Response({
                'detail': 'البريد الإلكتروني مسجل بالفعل.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # حذف أي pending user قديم لنفس البريد
        PendingUser.objects.filter(email=email).delete()
        
        # إنشاء PendingUser
        try:
            pending_user = PendingUser.objects.create(
                username=username,
                email=email,
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                password_hash=make_password(password),
                role=data.get('role', 'patient'),
                phone=data.get('phone'),
                national_id=data.get('national_id'),
                governorate=data.get('governorate'),
                dob=data.get('dob'),
                expires_at=timezone.now() + timedelta(hours=48)
            )
            
            # تسجيل بداية عملية التسجيل
            log_authentication(
                action='register',
                request=request,
                email=email,
                username=username,
                success=True
            )
            
            # إرسال البريد الإلكتروني
            try:
                send_pending_verification_email(pending_user, request=request)
                log_authentication(
                    action='email_verification',
                    request=request,
                    email=email,
                    success=True
                )
            except Exception as e:
                log_authentication(
                    action='email_verification',
                    request=request,
                    email=email,
                    success=False,
                    error_message=str(e)
                )
                # حتى لو فشل البريد، نعيد نجاح مع تحذير
                return Response({
                    'detail': 'تم إنشاء الطلب ولكن فشل إرسال بريد التفعيل. حاول لاحقاً أو تواصل مع الدعم.',
                    'verification_required': True
                }, status=status.HTTP_201_CREATED)

            return Response({
                'detail': 'تم إرسال رابط التفعيل إلى بريدك الإلكتروني. يرجى تأكيد حسابك خلال 48 ساعة.',
                'email': email,
                'verification_required': True
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            log_authentication(
                action='register',
                request=request,
                email=email,
                username=username,
                success=False,
                error_message=str(e)
            )
            return Response({
                'detail': f'حدث خطأ أثناء التسجيل: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class ConfirmRegistrationView(APIView):
    """تأكيد التسجيل عبر رابط البريد الإلكتروني - إنشاء User من PendingUser"""
    permission_classes = [AllowAny]
    
    def get(self, request, token: str):
        from .models import PendingUser
        from api.models import Patient
        
        try:
            pending_user = PendingUser.objects.get(verification_token=token)
        except PendingUser.DoesNotExist:
            # رابط غير صحيح
            return redirect('/email-verification-failed/?reason=invalid')
        
        # التحقق من انتهاء الصلاحية
        if pending_user.is_expired():
            pending_user.delete()  # حذف البيانات المنتهية
            return redirect('/email-verification-failed/?reason=expired')
        
        # التحقق من أن البريد غير مستخدم بالفعل
        if User.objects.filter(email=pending_user.email).exists():
            pending_user.delete()
            return redirect('/email-verification-failed/?reason=already_exists')
        
        # إنشاء المستخدم
        try:
            user = User.objects.create(
                username=pending_user.username,
                email=pending_user.email,
                first_name=pending_user.first_name,
                last_name=pending_user.last_name,
                role=pending_user.role,
                phone=pending_user.phone,
                national_id=pending_user.national_id,
                governorate=pending_user.governorate,
                is_active=True  # مفعّل مباشرة
            )
            user.password = pending_user.password_hash  # نستخدم الـ hash المحفوظ
            user.save()
            
            # إنشاء Patient إذا كان الدور مريض، أو Doctor إذا كان الدور طبيب
            if pending_user.role == 'patient':
                Patient.objects.create(user=user, dob=pending_user.dob)
            elif pending_user.role == 'doctor':
                from api.models import Doctor
                Doctor.objects.create(user=user)
            
            # حذف PendingUser بعد إنشاء User
            pending_user.delete()
            
            # تسجيل نجاح التفعيل
            log_authentication(
                action='email_verification',
                request=request,
                user=user,
                success=True
            )
            
            # توجيه المستخدم لصفحة نجاح مع إمكانية تسجيل الدخول
            return redirect('/email-verified-success/')
            
        except Exception as e:
            log_authentication(
                action='email_verification',
                request=request,
                email=pending_user.email,
                success=False,
                error_message=str(e)
            )
            return redirect(f'/email-verification-failed/?reason=error&message={str(e)}')


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token: str):
        result = verify_email_token(token)
        context = {}
        if not result or not result.get('ok'):
            reason = (result or {}).get('error')
            msg = 'رابط التفعيل غير صالح أو منتهي.'
            if reason == 'expired':
                msg = 'انتهت صلاحية رابط التفعيل. يرجى طلب رابط جديد.'
            
            # تسجيل فشل التفعيل
            log_authentication(
                action='email_verification',
                request=request,
                success=False,
                error_message=reason or 'invalid_token'
            )
            
            if request.accepted_renderer.format == 'html':
                return render(request, 'accounts/verify_failed.html', {'reason': reason, 'message': msg}, status=400)
            return Response({'detail': msg, 'reason': reason}, status=status.HTTP_400_BAD_REQUEST)

        UserModel = get_user_model()
        try:
            data = result.get('data', {})
            user = UserModel.objects.get(pk=data.get('uid'), email=data.get('email'))
        except UserModel.DoesNotExist:
            log_authentication(
                action='email_verification',
                request=request,
                email=data.get('email'),
                success=False,
                error_message='user_not_found'
            )
            if request.accepted_renderer.format == 'html':
                return render(request, 'accounts/verify_failed.html', status=404)
            return Response({'detail': 'المستخدم غير موجود.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])
            # تسجيل نجاح التفعيل
            log_authentication(
                action='email_verification',
                request=request,
                user=user,
                success=True
            )

        if request.accepted_renderer.format == 'html':
            return redirect(getattr(settings, 'LOGIN_REDIRECT_URL', '/'))
        return Response({'detail': 'تم تفعيل الحساب بنجاح.'}, status=status.HTTP_200_OK)


class ResendVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email') or request.query_params.get('email')
        if not email:
            return Response({'detail': 'يرجى تزويد البريد الإلكتروني.'}, status=status.HTTP_400_BAD_REQUEST)

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            # لا نكشف إن كان البريد موجوداً أم لا
            return Response({'detail': 'تم إرسال رابط التفعيل إن كان البريد مسجلاً.'}, status=status.HTTP_200_OK)

        if user.is_active:
            return Response({'detail': 'الحساب مفعل بالفعل. يمكنك تسجيل الدخول.'}, status=status.HTTP_200_OK)

        try:
            send_verification_email(user, request=request)
            log_authentication(
                action='email_verification_resend',
                request=request,
                user=user,
                success=True
            )
        except Exception as e:
            log_authentication(
                action='email_verification_resend',
                request=request,
                user=user,
                success=False,
                error_message=str(e)
            )
            return Response({'detail': 'تعذر إرسال بريد التفعيل حالياً. حاول لاحقاً.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({'detail': 'تم إرسال رابط التفعيل إلى بريدك الإلكتروني.'}, status=status.HTTP_200_OK)


class ActivatedTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role
        token['name'] = user.get_full_name() or user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            user = self.user
            if not user.is_active:
                # تسجيل فشل تسجيل الدخول - حساب غير مفعّل
                log_authentication(
                    action='login_failed',
                    request=self.context.get('request'),
                    user=user,
                    email=user.email,
                    username=user.username,
                    success=False,
                    error_message='حساب غير مفعّل'
                )
                raise AuthenticationFailed('حسابك غير مفعّل. يرجى تفعيل البريد الإلكتروني أولاً.', code='user_inactive')
            
            # تسجيل نجاح تسجيل الدخول
            log_authentication(
                action='login',
                request=self.context.get('request'),
                user=user,
                email=user.email,
                username=user.username,
                success=True
            )
            
            # Add user details to response
            data['role'] = user.role
            data['name'] = user.get_full_name() or user.username
            data['email'] = user.email
            
            return data
        except AuthenticationFailed:
            raise
        except Exception as e:
            # تسجيل فشل تسجيل الدخول - بيانات خاطئة
            username = attrs.get('username', '')
            log_authentication(
                action='login_failed',
                request=self.context.get('request'),
                email=username if '@' in username else None,
                username=username if '@' not in username else None,
                success=False,
                error_message=str(e)
            )
            raise


class ActivatedTokenObtainPairView(TokenObtainPairView):
    serializer_class = ActivatedTokenObtainPairSerializer


class PasswordResetRequestView(APIView):
    """طلب إعادة تعيين كلمة المرور - إرسال رمز OTP"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        UserModel = get_user_model()
        
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            # لا نكشف إن كان البريد موجوداً أم لا (أمان)
            return Response({
                'detail': 'إذا كان البريد الإلكتروني مسجلاً، ستتلقى رمز التحقق لإعادة تعيين كلمة المرور.'
            }, status=status.HTTP_200_OK)

        try:
            send_otp_email(user, request=request)
            log_authentication(
                action='password_reset_request',
                request=request,
                user=user,
                success=True
            )
        except Exception as e:
            log_authentication(
                action='password_reset_request',
                request=request,
                user=user,
                success=False,
                error_message=str(e)
            )
            return Response({
                'detail': 'تعذر إرسال البريد الإلكتروني حالياً. حاول لاحقاً.'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({
            'detail': 'تم إرسال رمز التحقق إلى بريدك الإلكتروني.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """تأكيد إعادة تعيين كلمة المرور برمز OTP"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        # التحقق من OTP من الكاش
        cache_key = f'password_reset_otp_{email}'
        cached_otp = cache.get(cache_key)

        # Debug logging
        print("\n" + "="*60)
        print(f"🔍 OTP VERIFICATION ATTEMPT")
        print(f"📧 Email: {email}")
        print(f"🔢 Received OTP: '{otp}' (type: {type(otp).__name__})")
        print(f"💾 Cached OTP: '{cached_otp}' (type: {type(cached_otp).__name__})")
        print(f"✅ Match: {str(cached_otp) == str(otp)}")
        print("="*60 + "\n")

        if not cached_otp or str(cached_otp) != str(otp):
             log_authentication(
                action='password_reset_confirm',
                request=request,
                email=email,
                success=False,
                error_message='invalid_or_expired_otp'
            )
             return Response({'detail': 'رمز التحقق غير صحيح أو منتهي الصلاحية.'}, status=status.HTTP_400_BAD_REQUEST)

        # الحصول على المستخدم
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
             return Response({'detail': 'المستخدم غير موجود.'}, status=status.HTTP_404_NOT_FOUND)

        # تحديث كلمة المرور
        user.set_password(new_password)
        user.save()
        
        # حذف OTP من الكاش بعد الاستخدام الناجح
        cache.delete(cache_key)
        
        # تسجيل نجاح إعادة تعيين كلمة المرور
        log_authentication(
            action='password_reset_confirm',
            request=request,
            user=user,
            success=True
        )

        print(f"✅ Password reset successful for {email}\n")

        return Response({
            'detail': 'تم تغيير كلمة المرور بنجاح. يمكنك الآن تسجيل الدخول.'
        }, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """تغيير كلمة المرور للمستخدم المسجل"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'detail': 'تم تغيير كلمة المرور بنجاح.'
        }, status=status.HTTP_200_OK)

