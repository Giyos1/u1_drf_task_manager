from django.urls import path
from accounts import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('token-login', views.LoginWithTokenViewSet, basename='login_token')
router.register('users', views.UserViewSet, basename='users')
router.register('test', views.TestCelery, basename='test')
urlpatterns = [
                  # path('login/', views.LoginAPIView.as_view(), name='login'),
                  path('logout/', views.LogoutAPIView.as_view(), name='logout'),
                  path('session/', views.SessionAPIView.as_view(), name='session'),
                  path('register/', views.RegisterAPIView.as_view(), name='register'),
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
