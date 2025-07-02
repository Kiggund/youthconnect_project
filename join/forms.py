from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, RegexValidator
from accounts.models import Profile
from utils.ocr import extract_text
from utils.validators import validate_ocr_fields  # You need to create this file

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'name'})
    )

    nin_number = forms.CharField(
        max_length=14,
        required=True,
        validators=[
            MinLengthValidator(14),
            RegexValidator(r'^\d{14}$', 'NIN must be 14 digits')
        ],
        widget=forms.TextInput(attrs={'pattern': r'\d{14}'})
    )

    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect
    )

    dob = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    place_of_birth = forms.CharField(max_length=100)
    current_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=200
    )

    profession = forms.CharField(max_length=100)
    place_of_work = forms.CharField(max_length=100)

    next_of_kin_name = forms.CharField(max_length=100)
    next_of_kin_email = forms.EmailField()
    next_of_kin_phone = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter valid phone number')]
    )
    next_of_kin_professional = forms.CharField(max_length=100)

    id_front = forms.ImageField(required=True, label="Your ID (Front)")
    id_back = forms.ImageField(required=True, label="Your ID (Back)")
    kin_id_front = forms.ImageField(required=True, label="Next of Kin ID (Front)")
    kin_id_back = forms.ImageField(required=True, label="Next of Kin ID (Back)")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'full_name', 'nin_number', 'gender', 'dob',
            'place_of_birth', 'current_address', 'profession',
            'place_of_work', 'next_of_kin_name', 'next_of_kin_email',
            'next_of_kin_phone', 'next_of_kin_professional',
            'id_front', 'id_back', 'kin_id_front', 'kin_id_back'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nin_number'].help_text = "14-digit National Identification Number"
        self.fields['password1'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_nin_number(self):
        nin = self.cleaned_data.get('nin_number', '').strip()
        if Profile.objects.filter(nin_number__iexact=nin).exists():
            raise forms.ValidationError("This NIN is already registered.")

        # OCR Check
        id_front = self.files.get('id_front') or self.cleaned_data.get('id_front')
        if id_front:
            try:
                ocr_text = extract_text(id_front)
                ocr_results = validate_ocr_fields(
                    nin=nin,
                    full_name=self.cleaned_data.get('full_name'),
                    dob=self.cleaned_data.get('dob'),
                    gender=self.cleaned_data.get('gender'),
                    place_of_birth=self.cleaned_data.get('place_of_birth'),
                    ocr_text=ocr_text
                )
                mismatches = [field for field, match in ocr_results.items() if not match]
                if mismatches:
                    raise forms.ValidationError(f"ID verification failed: {', '.join(mismatches)} mismatch.")
            except Exception as e:
                print(f"[OCR ERROR] {e}")
                raise forms.ValidationError("Unable to verify ID content using OCR.")
        return nin

    def clean_gender(self):
        gender = self.cleaned_data.get('gender', '').strip().capitalize()
        if gender not in dict(self.GENDER_CHOICES).keys():
            raise forms.ValidationError("Invalid gender selection.")
        return gender

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()

        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                nin_number=self.cleaned_data['nin_number'],
                gender=self.cleaned_data['gender'],
                dob=self.cleaned_data['dob'],
                place_of_birth=self.cleaned_data['place_of_birth'],
                current_address=self.cleaned_data['current_address'],
                profession=self.cleaned_data['profession'],
                place_of_work=self.cleaned_data['place_of_work'],
                next_of_kin_name=self.cleaned_data['next_of_kin_name'],
                next_of_kin_email=self.cleaned_data['next_of_kin_email'],
                next_of_kin_phone=self.cleaned_data['next_of_kin_phone'],
                next_of_kin_professional=self.cleaned_data['next_of_kin_professional'],
                id_front=self.cleaned_data['id_front'],
                id_back=self.cleaned_data['id_back'],
                kin_id_front=self.cleaned_data['kin_id_front'],
                kin_id_back=self.cleaned_data['kin_id_back'],
            )
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Email/Username")
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'nin_number', 'gender', 'dob',
            'place_of_birth', 'current_address', 'profession',
            'place_of_work', 'next_of_kin_name', 'next_of_kin_email',
            'next_of_kin_phone', 'next_of_kin_professional'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'current_address': forms.Textarea(attrs={'rows': 3}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit OTP',
            'pattern': r'\d{6}',
            'inputmode': 'numeric'
        }),
        error_messages={
            'required': "OTP is required.",
            'min_length': "OTP must be exactly 6 digits.",
            'max_length': "OTP must be exactly 6 digits."
        }
    )
