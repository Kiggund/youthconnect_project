# test_signals.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youthconnect.settings')
import django
django.setup()

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
import random

User = get_user_model()

def inspect_signals():
    # Clean up previous test user if exists
    User.objects.filter(username__startswith='testuser_').delete()
    
    # Generate random username
    test_username = f'testuser_{random.randint(1000, 9999)}'
    
    # Check signals
    receivers = post_save._live_receivers(User)
    print(f"\nFound {len(receivers)} User post_save receivers:")
    
    for i, receiver in enumerate(receivers, 1):
        try:
            print(f"{i}. {receiver.__module__}.{receiver.__name__}")
        except AttributeError:
            print(f"{i}. {receiver.__class__}")

    # Create test user
    print(f"\nCreating user {test_username}...")
    user = User.objects.create_user(
        username=test_username,
        email=f'{test_username}@example.com',
        password='test123'
    )
    print(f"Profile exists: {hasattr(user, 'profile')}")

if __name__ == '__main__':
    inspect_signals()
