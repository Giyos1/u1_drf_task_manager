from django.urls import path
from accounts import views

urlpatterns = [
    path('auth/', views.AuthAPIView.as_view(), name='login'),
    path('reset/', views.ResetPasswordAPIView.as_view(), name='reset'),
    path('confirm/<str:token>/', views.ResetPasswordAPIView.as_view(), name='reset'),
]
