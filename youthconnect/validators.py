import dns.resolver
import smtplib
import socket
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class EmailDomainValidator:
    """Comprehensive email domain validator for Django"""
    
    disposable_domains = [
        'mailinator.com', 'tempmail.com', '10minutemail.com',
        'guerrillamail.com', 'yopmail.com', 'trashmail.com'
    ]
    
    def __init__(self, check_mx=True, check_smtp=False):
        self.check_mx = check_mx
        self.check_smtp = check_smtp
        
    def __call__(self, email):
        domain = self.extract_domain(email)
        
        if self.is_disposable(domain):
            raise ValidationError(
                _("Temporary email providers are not allowed."),
                code='disposable_email'
            )
            
        if self.check_mx and not self.has_mx_records(domain):
            raise ValidationError(
                _("The email domain doesn't exist or can't receive emails."),
                code='no_mx_records'
            )
            
        if self.check_smtp and not self.smtp_handshake(domain):
            raise ValidationError(
                _("We couldn't verify the email server."),
                code='smtp_verification_failed'
            )
    
    @staticmethod
    def extract_domain(email):
        try:
            return email.split('@')[1].lower()
        except IndexError:
            raise ValidationError(
                _("Invalid email format."),
                code='invalid_email'
            )
    
    def is_disposable(self, domain):
        return domain in self.disposable_domains
    
    def has_mx_records(self, domain):
        try:
            return bool(dns.resolver.resolve(domain, 'MX'))
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            return False
        except Exception:
            try:
                import socket
                socket.gethostbyname(domain)
                return True
            except:
                return False
    
    def smtp_handshake(self, domain):
        """Optional SMTP verification (may be slow)"""
        try:
            records = dns.resolver.resolve(domain, 'MX')
            mx_record = str(records[0].exchange)
            
            with smtplib.SMTP(timeout=10) as server:
                server.connect(mx_record)
            return True
        except:
            return False
