"""
URL configuration for youthconnect project.
"""

from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from paypal.standard.ipn.views import ipn
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from .views import CustomPasswordResetForm, CustomPasswordResetDoneView
from accounts.views import edit_account
from privacy_policy.views import  privacy_policy
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Root URL redirect (new addition)
    path('', RedirectView.as_view(url='/homepage/'), name='root_redirect'),
    
    # Existing URLs
    path('admin/', admin.site.urls),
    path('leaders/', include('leaders.urls')),
    path('homepage/', include('homepage.urls')),
    path('news_events/', include('news_events.urls')),
    path('resources/', include('resources.urls')),
    path('privacy_policy/', privacy_policy,  name='privacy_policy'),
    path('edit/', edit_account, name='edit_account'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about/', include('about.urls')),
    path("legal/", include("legal.urls")),
    path('join/', include('join.urls', namespace='join')),
    path('accounts/', include('accounts.urls')),
    path('contact/', include('contact.urls')),
    path('send-message/', views.send_message, name='send_message'),
    path('payments/', include("payments.urls")),
    path('paypal-ipn/', ipn, name='paypal-ipn'),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html',
            form_class=CustomPasswordResetForm,
            success_url=reverse_lazy('password_reset_done'),
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt'
        ),
        name='password_reset'),

    path('password-reset/done/',
        CustomPasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]

# Static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
