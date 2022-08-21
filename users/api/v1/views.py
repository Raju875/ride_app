from django.shortcuts import get_object_or_404
from requests import delete
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import timedelta
from rest_framework.viewsets import ModelViewSet, ViewSet

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from users.models import *
from .serializers import *
from users.utils import TimeZoneUtil


class CustomerProfileViewSet(ViewSet):
    authentication_class = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.none()

    def get(self, request):
        request_user = self.request.user
        try:
            profile = CustomerProfileSerializer(CustomerProfile.objects.filter(
                user=request_user, user__user_type=2).first(), many=False)
            documents = CustomerDocumentsSerializer(CustomerDocuments.objects.filter(
                user=request_user, user__user_type=2).first(), context={'request': request}, many=False)
            return Response({
                'profile': profile.data,
                'documents': documents.data
            })
        except Exception as e:
            return Response({"error": _(str(e) + ' [CP-101]')}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        request_user = self.request.user
        try:
            from modules.push_notifications.client import Client
            from modules.push_notifications.constants import API_ROOT
            client = Client(settings.ONE_SIGNAL_APP_ID,
                            settings.ONE_SIGNAL_REST_API_KEY,
                            settings.USER_AUTH_KEY,
                            API_ROOT)
            client.create_notification({"brand": "Ford",
                                       "model": "Mustang",
                                       "year": 1964})
            print|(1)
            breakpoint()

            queryset = CustomerProfile.objects.filter(
                user=self.request.user, user__user_type=2).first()
            if queryset:
                serializer = CustomerProfileSerializer(
                    queryset, data=request.data, context={'request': request})
            else:
                serializer = CustomerProfileSerializer(
                    data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(user=request_user)
                return Response({"success": "Data stored successfully."}, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors})
        except Exception as e:
            import sys
            _type, _object, _traceback = sys.exc_info()
            filename = _traceback.tb_frame.f_code.co_filename
            line_number = _traceback.tb_lineno

            print("Exception type: ", _type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            print("Exception: ", e)

            return Response({"error": _(str(e) + ' [CP-101]')}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        queryset = get_object_or_404(CustomerProfile, user=self.request.user)
        queryset.delete()
        return Response({"success": "Data deleted successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def add_customer_documents(self, request):
        request_user = self.request.user
        try:
            queryset = CustomerDocuments.objects.filter(
                user=request_user).first()
            if queryset:
                serializer = CustomerDocumentsSerializer(
                    queryset, data=request.data, context={'request': request})
            else:
                serializer = CustomerDocumentsSerializer(
                    data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(user=request_user)
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        except Exception as e:
            return Response({"error": _(str(e) + ' [CP-101]')}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_customer_documents(self, request):
        try:
            queryset = CustomerDocuments.objects.filter(
                user=self.request.user).first()
            serializer = CustomerDocumentsSerializer(
                queryset, context={'request': request}, many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": _(str(e) + ' [CP-101]')}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete_customer_documents(self, request):
        request_user = self.request.user
        queryset = get_object_or_404(CustomerDocuments, user=request_user)
        queryset.delete()
        return Response({"success": "Data deleted successfully."})


class DriverProfileViewSet(ModelViewSet):
    authentication_class = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]
    serializer_class = DriverProfileSerializer
    queryset = DriverProfile.objects.none()

    def get_queryset(self):
        return DriverProfile.objects.filter(user=self.request.user, user__user_type=3)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response({"error": _(str(e)+'[DP-101]')}, status=status.HTTP_400_BAD_REQUEST)


class VehicleInfoViewSet(ModelViewSet):
    authentication_class = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]
    serializer_class = VehicleInfoSerializer
    queryset = VehicleInfo.objects.none()

    def get_queryset(self):
        return VehicleInfo.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user,
                            driver=self.request.user.driver_profile)
        except Exception as e:
            return Response(_(str(e) + '[VI-102]'), status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ForgotPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except Exception:
            return Response({
                "success": False,
                "message": _("Your entered email does not exist. Please enter a valid email or Create New Account.")}, status=status.HTTP_404_NOT_FOUND)
        try:
            code = VerificationCode.generate_code_for_user(user)
            email_context = {
                "email": email,
                "code": code
            }
            html_content = render_to_string(
                'forgot_password.html', email_context)
            message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=email,
                subject='Forget Password',
                html_content=html_content)
            sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
            sg.send(message)

            return Response({"success": True,
                            "message": _("A mail is sent to " + email + ". Please check it."),
                            "data": email_context['email']}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"success": False, "message": str(e) + '[UFP-101]'}, status=status.HTTP_400_BAD_REQUEST)


class VerificationViewSet(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny, ]
    serializer_class = VerificationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        code = request.data['code']
        try:
            user_code = VerificationCode.objects.get(
                code=code, is_used=False, user__email=email)
        except Exception:
            return Response({"success": False,
                            "message": _('Invalid Code! Please provide a valid verification code')}, status=status.HTTP_400_BAD_REQUEST)

        now = TimeZoneUtil.get_datetime()
        expired_date = TimeZoneUtil.utc_to_timezone(
            user_code.updated_at + timedelta(minutes=60))
        if expired_date < now:
            return Response({"success": False,
                            "message": _("Token expired!")}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True,
                        'data': {"email": email, "code": code}}, status=status.HTTP_200_OK)


class ResetPasswordSetView(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        code = request.data['code']
        try:
            user_code = VerificationCode.objects.get(
                code=code, is_used=False, user__email=email)
        except Exception:
            return Response({"success": False,
                            "message": _('Invalid Code! Please try again.')}, status=status.HTTP_400_BAD_REQUEST)

        expired_date = TimeZoneUtil.utc_to_timezone(
            user_code.updated_at + timedelta(minutes=60))
        now = TimeZoneUtil.get_datetime()
        if expired_date < now:
            return Response({"success": False,
                            "message": _("Token expired!")}, status=status.HTTP_400_BAD_REQUEST)

        if request.data['password'] != request.data['confirm_password']:
            return Response({"success": False,
                            "message": _("Those passwords don't match.")}, status=status.HTTP_400_BAD_REQUEST)

        user = user_code.user
        user.set_password(request.data['password'])
        user.save()

        user_code.is_used = True
        user_code.save()

        return Response({"success": True,
                        "message": _("Password update successfully.")}, status=status.HTTP_201_CREATED)
