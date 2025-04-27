from django.urls import path
from .views import contact_page, send_message

app_name = 'contact'

urlpatterns = [
    path('', contact_page, name='contact_page'),  # Fixed the name to 'contact_page'
    path('send/', send_message, name='send'),  # No change here
]
