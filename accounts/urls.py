from django.urls import path
from accounts.views import edit_account
from accounts.views import profile

urlpatterns = [
    path('edit/', edit_account, name='edit_account'),
    path('profile/', profile, name='profile'),
]
