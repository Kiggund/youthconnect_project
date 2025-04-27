from django.urls import path
from . import views
app_name = 'join'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('verify-otp/<str:email>/', views.verify_otp, name='verify_otp'),
    path('resend-otp/<str:email>/', views.resend_otp, name='resend_otp'),
    path('success/', views.success, name='success'),
   # path('contact/', views.contact, name='contact'),
]
