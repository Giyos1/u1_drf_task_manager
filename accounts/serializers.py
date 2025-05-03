from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.utils import create_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name'
        )


class UserCreateSerializers(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "re_password"
        )

    def validate(self, attrs):
        re_password = attrs.pop('re_password')
        password = attrs.get('password')
        if re_password != password:
            raise ValidationError("password not equal re password")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError('Email or Password incorrect')

        if not user.is_active:
            raise ValidationError('user in active')

        return {"user": user}


class LoginWithTokenSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError('Email or Password incorrect')

        if not user.is_active:
            raise ValidationError('user in active')

        token = create_token(user.id)
        return {"access": token.get('access'), 'refresh': token.get('refresh')}


class TestSerializers(serializers.Serializer):
    id = serializers.CharField(max_length=200)
