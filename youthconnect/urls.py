"""
URL configuration for youthconnect project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from paypal.standard.ipn.views import ipn
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
    path('about/', include('about.urls')),
    path('join/', include('join.urls', namespace='join')),
    path('contact/', include('contact.urls')),
    path('send-message/', views.send_message, name='send_message'),
    path('payments/', include("payments.urls")),
    path('paypal-ipn/', ipn, name='paypal-ipn'),
]

# Static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
