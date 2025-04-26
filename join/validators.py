import dns.resolver
from django.core.exceptions import ValidationError

def validate_email_domain(email):
    """Validate email domain for existence and disposability"""
    domain = email.split('@')[-1]
    if domain in ['mailinator.com', 'tempmail.com', 'yopmail.com', 'trashmail.com']:
        raise ValidationError("Temporary email providers are not allowed.")
    try:
        dns.resolver.resolve(domain, 'MX')
    except dns.resolver.NoAnswer:
        raise ValidationError("Email domain exists but can't receive emails.")
    except dns.resolver.NXDOMAIN:
        raise ValidationError("Email domain does not exist.")
    except Exception as e:
        raise ValidationError(f"Error during domain validation: {str(e)}")
