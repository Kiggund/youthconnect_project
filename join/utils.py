import dns.resolver
from django.core.exceptions import ValidationError
import random

#generate otp code
def generate_otp():
    return str(random.randint(100000, 999999))  # Generates a 6-digit OTP

def validate_email_domain(email):
    # Temporarily skip domain validation
    pass
"""
def validate_email_domain(email):
    try:
        # Extract the domain from the email
        domain = email.split('@')[-1]
        
        # Set custom DNS resolvers (Google DNS)
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '8.8.4.4']

        # Query for MX records to check domain validity
        resolver.resolve(domain, 'MX')
    except Exception as e:
        raise ValidationError(f"Error during domain validation: {str(e)}")
"""
