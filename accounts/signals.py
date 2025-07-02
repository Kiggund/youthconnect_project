from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
from .utils import send_welcome_email

User = get_user_model()

@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    """Combined signal handler for profile and email"""
    if created:
        # Create profile
        Profile.objects.get_or_create(user=instance)
        
        # Send welcome email
        try:
            send_welcome_email(instance)
        except Exception as e:
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(f"Email failed: {e}")
    
    # Save profile updates
    if hasattr(instance, 'profile'):
        instance.profile.save()
