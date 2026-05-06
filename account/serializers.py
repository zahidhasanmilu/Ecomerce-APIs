from rest_framework import serializers
from account.tasks import send_otp_email_task
from .models import User
from django.contrib.sites.models import Site
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import PasswordResetToken
from django.utils import timezone
from .utils import generate_otp
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site


def get_current_site():
    return Site.objects.get_current()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        try:
            current_site = Site.objects.get_current()
        except (Site.DoesNotExist, ImproperlyConfigured):
            current_site = None

        profile_picture_url = None

        if self.user.profile.profile_picture and current_site:
            profile_picture_url = (
                current_site.domain + self.user.profile.profile_picture.url
            )

        data.update(
            {
                "user": {
                    "id": self.user.id,
                    "first_name": self.user.first_name,
                    "last_name": self.user.last_name,
                    "username": self.user.username,
                    "email": self.user.email,
                    "is_active": self.user.is_active,
                    "role": self.user.role,
                    "phone_number": self.user.profile.phone_number,
                    "profile_picture": profile_picture_url,
                }
            }
        )

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=8, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "password",
            "confirm_password",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Password and confirm password do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role=validated_data.get("role", "customer"),
            password=validated_data["password"],
            is_active=False,
            is_verified=False,
        )
        return user


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    # Profile fields mapped via `source`
    phone_number = serializers.CharField(source='profile.phone_number', required=False)
    address = serializers.CharField(source='profile.address', required=False)
    date_of_birth = serializers.DateField(
        source='profile.date_of_birth', required=False
    )
    profile_picture = serializers.ImageField(
        source='profile.profile_picture', required=False
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            # Profile fields
            'phone_number',
            'address',
            'date_of_birth',
            'profile_picture',
        ]
        read_only_fields = ['email']  # Email should not be editable

    def update(self, instance, validated_data):
        # Extract profile fields
        profile_data = validated_data.pop('profile', {})

        # -------------------------------
        # Update USER fields
        # -------------------------------
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # -------------------------------
        # Update PROFILE fields
        # -------------------------------
        profile = instance.profile

        for attr, value in profile_data.items():
            setattr(profile, attr, value)

        profile.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user

        # 1. Old password check
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect"}
            )

        # 2. New password match check
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "New passwords do not match"}
            )

        # 3. New password validation (Django default validators)
        try:
            validate_password(attrs['new_password'], user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# -----------------------------------------------------------------
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            self.user = None
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=6)
    re_new_password = serializers.CharField(
        write_only=True, required=True, min_length=6
    )

    def validate(self, data):
        if data['new_password'] != data['re_new_password']:
            raise serializers.ValidationError(
                {"new_password": "New passwords must match."}
            )

        try:
            reset_token_obj = PasswordResetToken.objects.get(
                token=data['token'], is_used=False, expires_at__gt=timezone.now()
            )

            self.reset_token = reset_token_obj
            return data

        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "Invalid, expired, or already used reset link/token."}
            )


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            self.user = None
        return value
