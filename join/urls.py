from django.urls import path
from . import views

app_name ='join'

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('register/', views.register, name='register'),  # Form submission
    path('success/', views.success, name='success'),  # Success page after registration
    path('contact/', views.contact, name='contact'),  # Contact page (if needed)
]
