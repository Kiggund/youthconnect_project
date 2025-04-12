from django.urls import path
from .views import leader_list

urlpatterns = [
    path('', leader_list, name='leader_list'),
]
