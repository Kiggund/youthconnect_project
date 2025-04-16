from django.db import models

class Member(models.Model):
    full_name = models.CharField(max_length=255)
    nin_number = models.CharField(max_length=14, unique=True)
    
    gender = models.CharField(max_length=20, choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Non-binary', 'Non-binary'), ('Prefer not to say', 'Prefer not to say')
    ])
    
    age = models.IntegerField()
    
    marital_status = models.CharField(max_length=20, choices=[
        ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')
    ])
    
    dob = models.DateField(null=True, blank=True)  # Allow optional DOB
    place_of_birth = models.CharField(max_length=255)
    current_address = models.TextField()  # For detailed location input
    
    email = models.EmailField(unique=True)
    
    signature = models.ImageField(
        upload_to='signatures/',  # Where uploaded signatures will be stored
        blank=True,  # Makes the field optional in forms
        null=True,   # Allows NULL in the database
        verbose_name="Signature (Optional)"  # Optional: Changes label text
    )
    
    professional = models.CharField(max_length=255)
    place_of_work = models.CharField(max_length=255)
    
    time_joined = models.DateTimeField(
        auto_now_add=True,  # Automatically set on creation
        verbose_name="Registration Timestamp",
        null=True,
        blank=True
    )
    
    next_of_kin_name = models.CharField(max_length=255)
    next_of_kin_email = models.EmailField()
    next_of_kin_phone = models.CharField(max_length=20)
    next_of_kin_professional = models.CharField(max_length=255)

    class Meta:
        ordering = ['-time_joined']  # Newest first by default

    def __str__(self):
        return f"{self.full_name} - {self.time_joined}"
