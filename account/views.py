from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid

from .serializers import (
    PasswordResetEmailSerializer,
    PasswordResetConfirmSerializer,
    VerifyOTPSerializer,
    ResendVerificationSerializer,
)
from .models import PasswordResetToken
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
)
from .utils import generate_otp
from .models import User
from .permissions import IsLoggedOut, IsOwnerOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserProfileSerializer
from .emails import send_verification_email
from django.shortcuts import get_object_or_404
from .models import EmailVerification
from .tasks import send_otp_email_task
from django.db import transaction

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        otp = generate_otp()
        verification = EmailVerification.objects.create(
            user=user,
            otp=otp,
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        #  AFTER RESPONSE SAFE CALL
        transaction.on_commit(
            lambda: send_otp_email_task.delay(
                user.email,
                otp,
                str(verification.token),
            )
        )

        return Response(
            {
            
                "message": "Registration successful",
                "email": user.email,
                "role": user.role,
                "otp": otp,
                "token": str(verification.token),
            },
            status=201,
        )
class VerifyEmailView(APIView):
    def post(self, request, token):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        opt = serializer.validated_data["otp"]

        verification = get_object_or_404(
            EmailVerification, token=token, is_verified=False
        )

        if verification.is_expired():
            return Response({"error": "OTP expired"}, status=400)

        if verification.otp != opt:
            return Response({"error": "Invalid OTP"}, status=400)

        verification.is_verified = True
        verification.save()

        user = verification.user
        user.is_active = True
        user.is_verified = True
        user.save()

        return Response({"message": "Email verified successfully"})


class VerifyEmailByLinkView(APIView):
    def get(self, request, token):
        verification = get_object_or_404(
            EmailVerification, token=token, is_verified=False
        )

        if verification.is_expired():
            return Response({"error": "Verification link expired"}, status=400)

        verification.is_verified = True
        verification.save()

        user = verification.user
        user.is_active = True
        user.is_verified = True
        user.save()

        return Response({"message": "Email verified successfully"})


class ResendVerificationView(APIView):
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = get_object_or_404(User, email=email)

        if user.is_verified:
            return Response({"message": "User already verified."}, status=400)

        verification, created = EmailVerification.objects.get_or_create(user=user)

        verification.otp = generate_otp()
        verification.token = verification.token if not created else verification.token
        verification.expires_at = timezone.now() + timezone.timedelta(minutes=10)
        verification.is_verified = False
        verification.save()

        send_verification_email(verification)

        return Response(
            {
                "message": "Verification email resent successfully.",
                "email": user.email,
                "otp": verification.otp,
                "token": str(verification.token),
            },
            status=200,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except KeyError:
            return Response(
                {"error": "The 'refresh' token field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"error": "Invalid token provided."}, status=status.HTTP_400_BAD_REQUEST
            )


TOKEN_EXPIRY_MINUTES = 5


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetEmailSerializer
    permission_classes = [IsLoggedOut]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if user:
            PasswordResetToken.objects.filter(user=user, is_used=False).delete()

            new_token_value = str(uuid.uuid4()).replace('-', '')
            expires_at = timezone.now() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
            PasswordResetToken.objects.create(
                user=user, token=new_token_value, expires_at=expires_at
            )

            REACT_RESET_URL = getattr(
                settings, 'REACT_RESET_URL', 'http://localhost:5173/reset-password'
            )
            reset_link = f"{REACT_RESET_URL}/{new_token_value}/"

            email_subject = "Password Reset Request"
            email_body = (
                f"You have requested a password reset for your account.\n\n"
                f"Click here to reset your password:\n{reset_link}\n\n"
                f"**IMPORTANT:** This link will expire in "
                f"**{TOKEN_EXPIRY_MINUTES} minutes**.\n"
                f"If you did not request this, please ignore this email."
            )

            send_mail(
                email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email]
            )

        return Response(
            {"detail": "Password reset email has been sent if the account exists."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [IsLoggedOut]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_token_obj = serializer.reset_token
        user = reset_token_obj.user
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        reset_token_obj.is_used = True
        reset_token_obj.save()

        return Response(
            {"detail": "Password has been successfully reset."},
            status=status.HTTP_200_OK,
        )


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password updated successfully"}, status=status.HTTP_200_OK
        )
