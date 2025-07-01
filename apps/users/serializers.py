# apps/users/serializers.py
import re

from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User, PasswordResetToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'role',
            'date_joined',
        ]
        read_only_fields = ['id', 'email', 'date_joined']

    def validate(self, attrs):
        for field in self.Meta.read_only_fields:
            if field in self.initial_data:
                raise serializers.ValidationError({field: "This field is read-only."})
        return super().validate(attrs)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'password', 'password2', 'tokens']

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'role': {'required': True},
            'password': {'required': True},
            'password2': {'required': True},
        }
        read_only_fields = ['id']

    def get_tokens(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
        )
        return user

    def validate_password(self, value):
        return validate_password(value)


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        return validate_password(value)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        if old_password == new_password:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password."})
        return attrs


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email found.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        PasswordResetToken.objects.filter(user=user).delete()
        reset_token = PasswordResetToken.objects.create(user=user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/confirm/?token={reset_token.token}"

        # TODO: Send email with reset_link hier (exemple dev):
        print(f"[DEV] Sending password reset link to {user.email}: {reset_link}")


class ConfirmPasswordResetSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        return validate_password(value)

    def validate(self, attrs):
        try:
            reset_token = PasswordResetToken.objects.get(token=attrs['token'])
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        if reset_token.is_expired():
            reset_token.delete()
            raise serializers.ValidationError({"token": "Token has expired."})

        attrs['user'] = reset_token.user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        PasswordResetToken.objects.filter(user=user).delete()


def validate_password(value):
    if len(value) < 9:
        raise serializers.ValidationError("Password too short (min 8 characters)")
    if len(value) > 16:
        raise serializers.ValidationError("Password too long (max 16 characters)")
    if not re.search(r"[A-Z]", value):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"\d", value):
        raise serializers.ValidationError("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        raise serializers.ValidationError("Password must contain at least one special character [!@#$%^&*(),"
                                          ".?\":{}|<>].")
    return value
