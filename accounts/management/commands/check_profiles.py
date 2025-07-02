# accounts/management/commands/check_profiles.py
from django.core.management.base import BaseCommand
from django.db.models import Q
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Verifies profile data integrity'

    def handle(self, *args, **options):
        self.stdout.write("=== Profile Data Health Check ===")
        
        # Check for problematic NINs
        problematic = Profile.objects.filter(
            Q(nin_number='') | 
            Q(nin_number__isnull=True) |
            Q(nin_number__startswith='TEMP_')
        )  # Fixed missing parenthesis
        
        count = problematic.count()
        if count:
            self.stdout.write(
                self.style.WARNING(f"Found {count} profiles needing attention:"))
            for p in problematic:
                self.stdout.write(f"ID {p.id}: {p.user.username} - NIN: '{p.nin_number}'")
            
            # Additional statistics
            empty = Profile.objects.filter(nin_number='').count()
            null = Profile.objects.filter(nin_number__isnull=True).count()
            temp = Profile.objects.filter(nin_number__startswith='TEMP_').count()
            
            self.stdout.write("\nBreakdown:")
            self.stdout.write(f"- Empty NINs: {empty}")
            self.stdout.write(f"- NULL NINs: {null}")
            self.stdout.write(f"- Temporary NINs: {temp}")
        else:
            self.stdout.write(
                self.style.SUCCESS("All profiles have valid NINs"))
        
        # Show summary of all profiles
        self.stdout.write("\n=== All Profiles ===")
        for p in Profile.objects.all().order_by('id'):
            status = "✓" if p.nin_number and not p.nin_number.startswith('TEMP_') else "✗"
            self.stdout.write(
                f"{status} ID: {p.id} | User: {p.user.username:20} | NIN: '{p.nin_number or 'NULL'}'"
            )
