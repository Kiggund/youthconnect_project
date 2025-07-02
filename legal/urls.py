from django.urls import path
from .views import privacy_policy, terms_conditions
from . import views
urlpatterns = [
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("terms-and-conditions/", terms_conditions, name="terms_conditions"),
]
