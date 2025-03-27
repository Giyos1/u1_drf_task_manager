from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError("username or password incorrect")

        if not user.is_active:
            raise ValidationError('user in active')

        return {"user": user}


class ResetPasswordSerializers(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        user = User.objects.filter(email=email)
        if not user:
            raise ValidationError('Email not Found')

        send_mail(
            'Forget Password',
            'reset password ushbu linkni bos',
            'giyosoripov4@gmail.com',
            [email, ]
        )
        return email
