from django.db import models
from django.utils import timezone
from datetime import timedelta

"""
Models for Youth Connect Project
This file defines database models for handling user registration, authentication,
and message storage, including OTP-based email verification.

Each model includes detailed field descriptions and helper methods to 
ensure proper validation and data integrity.
"""

# =============================== #
#           Member Model          #
# =============================== #

class Member(models.Model):
    """
    Represents a registered member in the system.
    
    Fields:
        - Personal details (name, NIN, email, etc.)
        - Professional details (workplace, occupation)
        - Next-of-kin information
        - OTP handling for email verification
        - Account locking for security
    
    Methods:
        - generate_otp(): Creates a random 6-digit OTP
        - is_otp_expired(): Checks if OTP is valid within a 5-minute window
        - increment_otp_attempts(): Tracks failed OTP entry attempts
        - reset_otp_security(): Clears OTP data after successful verification
        - is_account_locked(): Determines if an account should be locked
    """
    
    # Personal Information
    full_name = models.CharField(max_length=255, help_text="Full name of the member")
    nin_number = models.CharField(max_length=14, unique=True, help_text="National Identification Number")
    gender = models.CharField(max_length=20, help_text="Gender of the member")
    age = models.IntegerField(help_text="Age of the member")
    marital_status = models.CharField(max_length=20, help_text="Marital status")
    dob = models.DateField(null=True, blank=True, help_text="Date of birth")
    place_of_birth = models.CharField(max_length=255, help_text="Place of birth")
    current_address = models.TextField(help_text="Current residential address")
    email = models.EmailField(unique=True, help_text="Email for communication and authentication")
    signature = models.CharField(max_length=100, null=True, blank=True, help_text="Optional signature data")

    # Professional Information
    professional = models.CharField(max_length=255, help_text="Professional field of the member")
    place_of_work = models.CharField(max_length=255, help_text="Workplace name")
    time_joined = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the member joined")

    # Next of Kin Information
    next_of_kin_name = models.CharField(max_length=255, help_text="Full name of next-of-kin")
    next_of_kin_email = models.EmailField(help_text="Email of next-of-kin")
    next_of_kin_phone = models.CharField(max_length=20, help_text="Phone number of next-of-kin")
    next_of_kin_professional = models.CharField(max_length=255, help_text="Profession of next-of-kin")

    # OTP Information for Authentication
    otp = models.CharField(max_length=6, null=True, blank=True, help_text="Generated OTP for verification")
    otp_created_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when OTP was generated")
    is_verified = models.BooleanField(default=False, help_text="Verification status of the member")
    is_locked = models.BooleanField(default=False, help_text="Whether the account is temporarily locked")
    lock_until = models.DateTimeField(null=True, blank=True, help_text="Time until the lock is lifted")

    def generate_otp(self):
        """Generates a random 6-digit OTP and sets expiration (5 minutes)."""
        import random
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp

    def is_otp_expired(self):
        """Returns True if OTP has expired (after 5 minutes)."""
        if not self.otp_created_at:
            return True
        return timezone.now() > self.otp_created_at + timedelta(minutes=5)

    def increment_otp_attempts(self):
        """Tracks failed OTP attempts and locks the account after multiple failures."""
        self.otp_attempts += 1
        if self.otp_attempts >= 3:
            self.is_locked = True
            self.lock_until = timezone.now() + timedelta(minutes=15)
        self.save()

    def reset_otp_security(self):
        """Clears OTP-related data after successful verification."""
        self.otp = None
        self.otp_created_at = None
        self.otp_attempts = 0
        self.save()

    def is_account_locked(self):
        """Checks if the account is temporarily locked based on failed attempts."""
        if self.lock_until and timezone.now() < self.lock_until:
            return True
        self.is_locked = False
        self.save()
        return False

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name']

