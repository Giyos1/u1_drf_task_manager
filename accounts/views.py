from config import celery_app
from celery.result import AsyncResult
from django.contrib.auth import login, logout
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from yaml import serialize

from accounts.models import User
from accounts.serializers import LoginSerializers, UserSerializer, UserCreateSerializers, LoginWithTokenSerializer, \
    TestSerializers
from accounts.tasks import add


class LoginAPIView(APIView):
    def post(self, request):
        serializers = LoginSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data.get('user')
        login(request, user)
        return Response(UserSerializer(user).data)


class LogoutAPIView(APIView):
    def delete(self, request):
        logout(request)
        return Response(data={"message": "logout"})


class SessionAPIView(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return Response(data={"message": "not login"})
        return Response(UserSerializer(request.user).data)


class RegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserCreateSerializers,
        responses={
            200: openapi.Response(
                'Success', UserSerializer
            )
        }
    )
    def post(self, request):
        serializers = UserCreateSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        return Response(UserSerializer(user).data)


class LoginWithTokenViewSet(GenericViewSet):
    serializer_class = LoginWithTokenSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UserViewSet(GenericViewSet, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class TestCelery(GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = TestSerializers

    @action(methods=['get'], detail=False)
    def run_task(self, request):
        task = add.delay(12, 15)
        return Response({'task_id': task.id})

    @action(methods=['post'], detail=False)
    def done_task(self, request):
        serializer = TestSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AsyncResult(serializer.validated_data['id'], app=celery_app)
        if result.ready():
            return Response({'message': result.result})
        return Response({'message': 'processing'})
