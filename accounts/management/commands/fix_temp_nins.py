import csv
from django.core.management.base import BaseCommand
from django.db.models import Q
from accounts.models import Profile
from django.core.mail import mail_admins

class Command(BaseCommand):
    help = 'Replaces temporary NINs using CSV or interactive mode'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            help='Path to CSV file with user_id,nin_number mappings'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate without making changes'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        csv_path = options['csv']
        
        temp_profiles = Profile.objects.filter(nin_number__startswith='TEMP_')
        self.stdout.write(f"Found {temp_profiles.count()} profiles needing updates")

        # CSV Processing Mode
        if csv_path:
            self.process_csv(csv_path, dry_run)
        # Interactive Mode
        else:
            self.process_interactive(temp_profiles, dry_run)
        
        if not dry_run:
            self.notify_admins(temp_profiles.count())

    def process_csv(self, csv_path, dry_run):
        updates = 0
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    profile = Profile.objects.get(user__id=row['user_id'])
                    if profile.nin_number.startswith('TEMP_'):
                        if dry_run:
                            self.stdout.write(f"Would update {profile.user.username} to {row['nin_number']}")
                        else:
                            profile.nin_number = row['nin_number']
                            profile.save()
                            updates += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing {row}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS(f"\nProcessed {updates} profiles from CSV"))

    def process_interactive(self, profiles, dry_run):
        for profile in profiles:
            self.stdout.write(f"\nProfile: {profile.user.username} (ID: {profile.user.id})")
            self.stdout.write(f"Current NIN: {profile.nin_number}")
            
            if dry_run:
                continue
                
            new_nin = input("Enter new NIN (or leave blank to skip): ").strip()
            if new_nin:
                profile.nin_number = new_nin
                profile.save()
                self.stdout.write(self.style.SUCCESS("Updated!"))

    def notify_admins(self, count):
        if count > 0:
            subject = f"NIN Updates Completed: {count} profiles modified"
            message = "The temporary NIN replacement job has finished."
            mail_admins(subject, message)
            self.stdout.write(self.style.SUCCESS("Admin notification sent"))
