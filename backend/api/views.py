from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Patient, TestType, Result, Notification, Message, Testimonial
from .serializers import PatientSerializer, TestTypeSerializer, ResultSerializer, NotificationSerializer, MessageSerializer, TestimonialSerializer

# ... [existing code] ...

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.filter(is_approved=True)
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny] # Allow read for everyone (homepage testimonials)

    def get_queryset(self):
        # Return only approved testimonials
        return Testimonial.objects.filter(is_approved=True).order_by('-created_at')

    def perform_create(self, serializer):
        # User must be authenticated to create
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise permissions.exceptions.PermissionDenied("You must be logged in to submit a review.")


User = get_user_model()

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestTypeViewSet(viewsets.ModelViewSet):
    queryset = TestType.objects.all()
    serializer_class = TestTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.select_related('patient', 'test_type').all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'patient', 'test_type']
    search_fields = ['patient__username', 'patient__email', 'patient__first_name', 'patient__last_name', 'test_type__name', 'result_value']
    ordering_fields = ['issued_at', 'status']
    ordering = ['-issued_at']

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        result = self.get_object()
        result.status = 'archived'
        result.save()
        return Response({'status': 'success', 'message': 'تم أرشفة النتيجة بنجاح'})

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        from django.http import FileResponse, Http404
        result = self.get_object()
        # Get the first associated file (assuming one main PDF per result for now)
        pdf_file = result.files.first()
        
        if pdf_file and pdf_file.file:
            response = FileResponse(pdf_file.file.open(), content_type='application/pdf')
            # Optional: to force download instead of view
            # response['Content-Disposition'] = f'attachment; filename="result_{result.id}.pdf"'
            return response
        else:
            raise Http404("PDF file not found for this result.")

    def create(self, request, *args, **kwargs):
        import json
        from .models import File
        
        data = request.data.copy()
        
        # Parse result_data JSON if present
        result_data_str = data.get('result_data')
        if result_data_str:
            try:
                result_data = json.loads(result_data_str)
                # Map notes/value from JSON to model fields
                data['notes'] = result_data.get('notes', '')
                data['value'] = result_data.get('value', data.get('notes', ''))
            except:
                pass
        
        # Ensure issued_by is set
        data['issued_by'] = request.user.id if request.user.is_authenticated else None
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        result_instance = serializer.instance
        
        # Handle PDF/File upload
        pdf_file = request.FILES.get('pdf')
        if pdf_file:
            File.objects.create(result=result_instance, file=pdf_file)
            
        # Create Notification for Patient
        try:
            patient_user = result_instance.patient.user
            Notification.objects.create(
                user=patient_user,
                title='نتيجة تحليل جديدة',
                message=f'تم إصدار نتيجة تحليل جديدة: {result_instance.test_type.name if result_instance.test_type else "تحليل عام"}.',
                is_read=False,
                result=result_instance
            )
        except Exception as e:
            print(f"Failed to create notification: {e}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'], url_path='send_email')
    def send_email(self, request, pk=None):
        from django.core.mail import EmailMessage
        from django.conf import settings
        
        result = self.get_object()
        
        # التأكد من أن المستخدم لديه صلاحية (طبيب أو مسؤول)
        if request.user.role not in ['doctor', 'admin'] and request.user != result.patient.user:
             return Response({'detail': 'ليس لديك صلاحية لإجراء هذا العمل.'}, status=status.HTTP_403_FORBIDDEN)

        patient_email = result.patient.user.email
        if not patient_email:
             return Response({'detail': 'المريض ليس لديه بريد إلكتروني مسجل.'}, status=status.HTTP_400_BAD_REQUEST)

        subject = f"نتيجة تحليل طبي - {result.test_type.name} - MyLabLink"
        patient_name = result.patient.user.first_name or result.patient.user.username
        
        message = f"""
        مرحباً {patient_name},
        
        نود إخبارك بأن نتيجة تحليل "{result.test_type.name}" الصادرة بتاريخ {result.issued_at.strftime('%Y-%m-%d')} جاهزة.
        
        الحالة: {result.status}
        النتيجة: {result.value if result.value else 'يرجى مراجعة الملف المرفق'}
        
        يمكنك الاطلاع على التفاصيل الكاملة عبر تسجيل الدخول إلى حسابك في MyLabLink.
        
        مع تمنياتنا بالصحة والعافية،
        فريق MyLabLink
        """
        
        try:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [patient_email],
            )
            
            # إرفاق الملفات
            for f in result.files.all():
                if f.file:
                    email.attach_file(f.file.path)
            
            email.send()
            
            return Response({'detail': 'تم إرسال النتيجة إلى البريد الإلكتروني بنجاح.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'فشل إرسال البريد: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a single notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all marked read'})

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get all messages where user is either sender or receiver"""
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver').order_by('timestamp')

    def perform_create(self, serializer):
        """Set sender to current user before saving"""
        message = serializer.save(sender=self.request.user)
        
        # Create notification for the receiver
        try:
            Notification.objects.create(
                user=message.receiver,
                sender=self.request.user,
                title=f'رسالة جديدة من {self.request.user.first_name or self.request.user.username}',
                message=f'{message.content[:50]}...',
                is_read=False
            )
        except Exception as e:
            print(f"Failed to create notification: {e}")

    @action(detail=False, methods=['get'])
    def conversations(self, request):
        """Get list of users the current user has conversations with"""
        user = request.user
        
        # Get all unique conversation partners
        sent_to = Message.objects.filter(sender=user).values_list('receiver', flat=True).distinct()
        received_from = Message.objects.filter(receiver=user).values_list('sender', flat=True).distinct()
        
        partner_ids = set(list(sent_to) + list(received_from))
        partners = User.objects.filter(id__in=partner_ids)
        
        from .serializers import UserSerializer
        serializer = UserSerializer(partners, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_patients(self, request):
        """Get list of patients for the current doctor (patients who have results OR appointments with this doctor)"""
        if request.user.role != 'doctor':
            return Response({'error': 'Only doctors can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get patients who have results issued by this doctor
        from .models import Result
        
        # Patients with results
        result_patient_ids = Result.objects.filter(
            issued_by=request.user
        ).values_list('patient', flat=True).distinct()

        # Patients with appointments
        # appointment_patient_ids removed
        
        # Combine
        patient_ids = set(list(result_patient_ids))
        
        # If list is still empty, maybe show all patients? 
        # For now, let's keep it scoped to interactions.
        
        patients = User.objects.filter(id__in=patient_ids)
        
        from .serializers import UserSerializer
        serializer = UserSerializer(patients, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_doctors(self, request):
        """Get list of doctors for the current patient"""
        if request.user.role != 'patient':
             return Response({'error': 'Only patients can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
        
        from .models import Result, Patient
        
        try:
            patient_profile = request.user.patient_profile
        except:
             return Response([])

        # Doctors who issued results
        result_doctor_ids = Result.objects.filter(
            patient=patient_profile
        ).values_list('issued_by', flat=True).distinct()

        # appointment_doctor_ids removed

        # Combine
        doctor_user_ids = set(list(result_doctor_ids))
        
        doctors = User.objects.filter(id__in=doctor_user_ids)
        
        from .serializers import UserSerializer
        serializer = UserSerializer(doctors, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def conversation_with(self, request):
        """Get all messages in a conversation with a specific user"""
        other_user_id = request.query_params.get('user_id')
        if not other_user_id:
            return Response({'error': 'user_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get all messages between current user and other user
        messages = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        ).select_related('sender', 'receiver').order_by('timestamp')
        
        # Mark received messages as read
        messages.filter(receiver=request.user, is_read=False).update(is_read=True)
        
        serializer = self.get_serializer(messages, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread messages"""
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return Response({'count': count})

    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        """Mark messages as read"""
        message_ids = request.data.get('message_ids', [])
        if message_ids:
            Message.objects.filter(
                id__in=message_ids, 
                receiver=request.user
            ).update(is_read=True)
        return Response({'status': 'success'})

    @action(detail=False, methods=['post'], url_path='mark_as_read')
    def mark_conversation_as_read(self, request):
        """Mark all messages from a specific user as read"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Mark all messages from other_user to current user as read
        updated_count = Message.objects.filter(
            sender=other_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        
        return Response({
            'status': 'success',
            'marked_count': updated_count
        })

