from django.urls import path
from . import views
from .views import (
    redirect_to_register, register, login_view, logout_view, edit_profile,
    verify_otp, resend_otp, success, dashboard
)

app_name = "join"

urlpatterns = [
    path("", redirect_to_register, name="redirect_to_register"),
    path("register/", register, name="register"),
    path("verify-otp/", verify_otp, name="verify_otp"),  # ✅ Removed `<str:email>` from URL
    path("resend-otp/", resend_otp, name="resend_otp"),  # ✅ Removed `<str:email>` from URL
    path("success/", success, name="success"),
    path('capture_id_front/', views.capture_id_front, name='capture_id_front'),
    path('capture_id_back/', views.capture_id_back, name='capture_id_back'),

    # Authentication routes
    path('dashboard/', dashboard, name='dashboard'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("edit-profile/", edit_profile, name="edit_profile"),
]
