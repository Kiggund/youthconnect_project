from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_welcome_email(user):
    """Send professional welcome email to new members"""
    context = {
        'username': user.username,
        'company_name': 'Youth Connect Group',
        'site_url': f'{settings.SITE_URL}/dashboard',
        'unsubscribe_url': f'{settings.SITE_URL}/unsubscribe',
        'privacy_url': f'{settings.SITE_URL}/privacy',
        'STATIC_URL': settings.STATIC_URL
    }

    # Render both templates
    html_content = render_to_string('email/welcome.html', context)
    text_content = render_to_string('email/welcome.txt', context)

    # Create email
    email = EmailMultiAlternatives(
        subject=f'Welcome to {context["company_name"]}',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.mixed_subtype = 'related'  # For embedded images
    email.send()
