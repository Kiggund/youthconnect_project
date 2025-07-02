# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("That username is already taken.")
        return username


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_pic',
            'full_name',
            'nin_number',
            'gender',
            'age',
            'marital_status',
            'dob',
            'place_of_birth',
            'current_address',
            'profession',
            'place_of_work',
            'next_of_kin_name',
            'next_of_kin_email',
            'next_of_kin_phone',
            'next_of_kin_professional',
            'bio',
        ]

    def clean_nin_number(self):
        nin = self.cleaned_data.get('nin_number')
        if Profile.objects.filter(nin_number=nin).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("That NIN is already in use by another user.")
        return nin
