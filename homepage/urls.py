from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root path linked to the "index" view
]
