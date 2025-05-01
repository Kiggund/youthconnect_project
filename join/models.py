from django.db import models
from django.utils import timezone
from datetime import timedelta

"""
Models for the Youth Connect Project

This file contains the database model definitions for handling user registration,
authentication, and OTP-based email verification. Each model includes comprehensive
documentation, validations, and helper methods to maintain data integrity.
"""

class Member(models.Model):
    """
    Represents a registered member in the Youth Connect system.

    Fields:
        - Personal details (e.g., name, email, NIN, etc.)
        - Professional details (e.g., workplace, occupation)
        - Next-of-kin information
        - OTP handling for email verification
        - Account locking for security

    Methods:
        - generate_otp(): Creates a random 6-digit OTP and enforces a 60-second cooldown.
        - is_otp_expired(): Checks if the OTP is still valid (within 5 minutes).
        - increment_otp_attempts(): Tracks failed OTP attempts and locks the account if necessary.
        - reset_otp_security(): Resets OTP-related fields after successful verification.
        - is_account_locked(): Determines if the account is locked based on failed attempts.
    """

    # -------------------------------------- #
    #        Personal Information Fields     #
    # -------------------------------------- #
    full_name = models.CharField(
        max_length=255,
        help_text="Full name of the member"
    )
    nin_number = models.CharField(
        max_length=14,
        unique=True,
        help_text="National Identification Number (must be 14 characters)"
    )
    gender = models.CharField(
        max_length=20,
        help_text="Gender of the member"
    )
    age = models.IntegerField(
        help_text="Age of the member"
    )
    marital_status = models.CharField(
        max_length=20,
        help_text="Marital status of the member"
    )
    dob = models.DateField(
        null=True,
        blank=True,
        help_text="Date of birth"
    )
    place_of_birth = models.CharField(
        max_length=255,
        help_text="Place of birth"
    )
    current_address = models.TextField(
        help_text="Current residential address"
    )
    email = models.EmailField(
        unique=True,
        help_text="Email address for communication and authentication"
    )
    signature = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Optional signature data"
    )

    # -------------------------------------- #
    #      Professional Information Fields   #
    # -------------------------------------- #
    professional = models.CharField(
        max_length=255,
        help_text="Professional field of the member"
    )
    place_of_work = models.CharField(
        max_length=255,
        help_text="Workplace name"
    )
    time_joined = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the member joined the system"
    )

    # -------------------------------------- #
    #      Next-of-Kin Information Fields    #
    # -------------------------------------- #
    next_of_kin_name = models.CharField(
        max_length=255,
        help_text="Full name of the next-of-kin"
    )
    next_of_kin_email = models.EmailField(
        help_text="Email address of the next-of-kin"
    )
    next_of_kin_phone = models.CharField(
        max_length=20,
        help_text="Phone number of the next-of-kin"
    )
    next_of_kin_professional = models.CharField(
        max_length=255,
        help_text="Profession of the next-of-kin"
    )

    # -------------------------------------- #
    #         OTP Information Fields         #
    # -------------------------------------- #
    otp = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        help_text="Generated OTP for email verification"
    )
    otp_created_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the OTP was created"
    )
    otp_attempts = models.PositiveIntegerField(
        default=0,
        help_text="Tracks the number of failed OTP attempts"
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Indicates whether the member's email is verified"
    )
    is_locked = models.BooleanField(
        default=False,
        help_text="Indicates if the account is temporarily locked"
    )
    lock_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The timestamp until the account remains locked"
    )

    # -------------------------------------- #
    #               Methods                  #
    # -------------------------------------- #

    def generate_otp(self):
        """
        Generates a random 6-digit OTP if cooldown has passed,
        saves it along with the current timestamp, and returns the OTP.

        :return: The generated OTP as a string
        """
        if self.otp_created_at and timezone.now() < self.otp_created_at + timedelta(seconds=60):
            # Enforce 60-second cooldown before generating another OTP
            raise ValueError("You must wait 60 seconds before requesting another OTP.")

        import random
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp

    def is_otp_expired(self):
        """
        Checks if the OTP has expired. The OTP is considered expired if more
        than 5 minutes have passed since it was created.

        :return: True if the OTP has expired, False otherwise
        """
        if not self.otp_created_at:
            return True
        return timezone.now() > self.otp_created_at + timedelta(minutes=5)

    def increment_otp_attempts(self):
        """
        Tracks failed OTP attempts. Locks the account if attempts reach the limit.
        Ensures remaining attempts are calculated correctly (3, 2, 1, and locked).
        """
        if self.is_account_locked():
            # Prevent increment if account is already locked
            return

        self.otp_attempts += 1

        if self.otp_attempts >= 3:  # Lock account after 3 attempts
            self.is_locked = True
            self.lock_until = timezone.now() + timedelta(minutes=15)
        self.save()

    def reset_otp_security(self):
        """
        Resets all OTP-related fields, including the OTP itself, its creation
        timestamp, and the count of failed OTP attempts.
        """
        self.otp = None
        self.otp_created_at = None
        self.otp_attempts = 0
        self.save()

    def is_account_locked(self):
        """
        Checks if the account is currently locked due to too many failed OTP
        attempts. If the lock period has expired, the account is unlocked.

        :return: True if the account is locked, False otherwise
        """
        if self.lock_until and timezone.now() < self.lock_until:
            return True

        # Reset lock state if lock duration has expired
        self.is_locked = False
        self.save()
        return False

    def __str__(self):
        """
        Returns a string representation of the Member instance,
        using the member's full name.

        :return: The full name of the member
        """
        return self.full_name

    class Meta:
        ordering = ['full_name']
