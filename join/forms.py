from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'current_address': forms.Textarea(attrs={'rows': 3}),
            'signature': forms.HiddenInput()  # Example of field-specific customization
        }

    def __init__(self, *args, **kwargs):
        # Remove custom kwargs before parent initialization
        self.for_registration = kwargs.pop('for_registration', False)
        super().__init__(*args, **kwargs)
        
        # Registration-specific customizations
        if self.for_registration:
            self.fields['email'].required = True
            self.fields['nin_number'].help_text = "Enter your 14-digit NIN"
            # Remove fields not needed during registration if any
            # self.fields.pop('some_field')

    def clean(self):
        cleaned_data = super().clean()
        if self.for_registration:
            # Add registration-specific validation
            if not cleaned_data.get('email'):
                raise forms.ValidationError("Email is required for registration")
        return cleaned_data

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit OTP',
            'pattern': '\d{6}',
            'inputmode': 'numeric'
        })
    )
