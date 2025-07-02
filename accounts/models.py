from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from datetime import date

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Disable UUID filename for now to test image saving
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        default='default.jpg'
    )
    updated_at = models.DateTimeField(auto_now=True)

    # Personal Information
    full_name = models.CharField(max_length=100)
    nin_number = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="National Identification Number",
        help_text="Enter your 14-digit National ID Number",
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]{14}$',
                message="NIN must be exactly 14 characters, consisting of letters and numbers."
            )
        ]
    )
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
    )
    age = models.IntegerField(blank=True, null=True)
    marital_status = models.CharField(
        max_length=15,
        choices=[('Single', 'Single'), ('Married', 'Married')]
    )
    dob = models.DateField(
        verbose_name="Date of Birth",
        validators=[MinValueValidator(date(1900, 1, 1))],
        null=True,
        blank=True
    )
    place_of_birth = models.CharField(max_length=100)
    current_address = models.CharField(max_length=200)

    # Professional Information
    profession = models.CharField(max_length=100)
    place_of_work = models.CharField(max_length=100)

    # Next of Kin Details
    next_of_kin_name = models.CharField(max_length=100)
    next_of_kin_email = models.EmailField()
    next_of_kin_phone = models.CharField(max_length=15)
    next_of_kin_professional = models.CharField(max_length=100)

    # Bio and audit timestamps
    bio = models.TextField(blank=True, max_length=500)
    time_joined = models.DateTimeField(auto_now_add=True)

    # ID Uploads
    id_front = models.ImageField(upload_to='ids/user/front/', null=True, blank=True)
    id_back = models.ImageField(upload_to='ids/user/back/', null=True, blank=True)
    kin_id_front = models.ImageField(upload_to='ids/kin/front/', null=True, blank=True)
    kin_id_back = models.ImageField(upload_to='ids/kin/back/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        if not self.age and self.dob:
            today = timezone.now().date()
            self.age = today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )
        super().save(*args, **kwargs)
