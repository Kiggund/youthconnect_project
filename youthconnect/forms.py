# youthconnect/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator, RegexValidator
from .models import CustomUser  # Replace with your User model if needed

class UserRegistrationForm(UserCreationForm):
    # Add fields from your original question
    full_name = forms.CharField(max_length=100)
    nin_number = forms.CharField(
        max_length=14,
        validators=[
            MinLengthValidator(14, "NIN must be 14 digits"),
            RegexValidator(r'^\d+$', "NIN must contain only digits")
        ]
    )
    GENDER_CHOICES = [('Female', 'Female'), ('Male', 'Male')]  # Update with your choices
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    place_of_birth = forms.CharField(max_length=100)
    current_address = forms.CharField(widget=forms.Textarea)
    profession = forms.CharField(max_length=100)
    place_of_work = forms.CharField(max_length=100)
    next_of_kin_name = forms.CharField(max_length=100)
    next_of_kin_email = forms.EmailField()
    next_of_kin_phone = forms.CharField(
        max_length=13,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Invalid phone format")]
    )
    next_of_kin_professional = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser  # Replace with your User model
        fields = [
            'username', 'email', 'password1', 'password2', 'full_name', 'nin_number',
            'gender', 'dob', 'place_of_birth', 'current_address', 'profession',
            'place_of_work', 'next_of_kin_name', 'next_of_kin_email', 'next_of_kin_phone',
            'next_of_kin_professional'
        ]
