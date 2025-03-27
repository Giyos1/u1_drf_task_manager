from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import LoginSerializers, UserSerializers, ResetPasswordSerializers


class AuthAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        login(request, user)
        return Response(UserSerializers(user).data)

    def delete(self, request):
        logout(request)
        return Response(data={"message": "success"})

    def get(self, request):
        if not request.user.is_anonymous:
            return Response(UserSerializers(request.user).data)
        return Response(data={
            "detail": "Method \"GET\" not allowed."
        })


class ResetPasswordAPIView(APIView):
    def post(self, request):
        serializers = ResetPasswordSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        return Response(data={
            "message": "success"
        })
