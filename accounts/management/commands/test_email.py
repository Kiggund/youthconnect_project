from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email configuration'

    def handle(self, *args, **options):
        try:
            sent = send_mail(
                subject=f"{settings.SITE_NAME} Email Test",
                message="This confirms your email setup is working.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMINS[0][1]],
                fail_silently=False
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Success! {sent} email sent"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed: {str(e)}"))
