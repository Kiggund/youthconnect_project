from .views import redirect_to_register
from django.urls import path
from . import views

app_name = 'join'

urlpatterns = [
   # path('', views.IndexView.as_view(), name='index'),
    path('api/verify-otp/', views.api_verify_otp, name='api-verify-otp'),
    path('', redirect_to_register, name='redirect_to_register'),
    path('register/', views.register, name='register'),  # Fixed this line
    path('verify-otp/<str:email>/', views.verify_otp, name='verify_otp'),
    path('resend-otp/<str:email>/', views.resend_otp, name='resend_otp'),
    path('success/', views.success, name='success'),
]
