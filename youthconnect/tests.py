from django.test import TestCase
from .forms import UserRegistrationForm  # 👈 Relative import (dot before "forms")

class UserRegistrationFormTest(TestCase):
    def setUp(self):
        # Valid sample data (adjust choices to match your form's requirements)
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'full_name': 'Test User',
            'nin_number': '12345678901234',  # 14 digits
            'gender': 'Female',  # Must match exact choice values
            'dob': '1990-01-01',
            'place_of_birth': 'Kampala',
            'current_address': '123 Main Street',
            'profession': 'Developer',
            'place_of_work': 'Tech Corp',
            'next_of_kin_name': 'Jane Doe',
            'next_of_kin_email': 'jane@example.com',
            'next_of_kin_phone': '+256712345678',
            'next_of_kin_professional': 'Nurse',
        }

    def test_form_validity_with_correct_data(self):
        form = UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'testuser')
        self.assertEqual(form.cleaned_data['gender'], 'Female')

    def test_nin_number_validation(self):
        # Test invalid NIN (too short)
        invalid_data = self.valid_data.copy()
        invalid_data['nin_number'] = '123'  # 3 digits (should fail)
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nin_number', form.errors)
        self.assertIn('Ensure this value has at least 14 characters', form.errors['nin_number'][0])

        # Test non-digit characters
        invalid_data['nin_number'] = 'ABCD5678901234'  # Contains letters
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('NIN must be 14 digits', form.errors['nin_number'][0])

    def test_gender_validation(self):
        # Test invalid gender choice
        invalid_data = self.valid_data.copy()
        invalid_data['gender'] = 'F'  # Invalid choice
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('gender', form.errors)
        self.assertIn('Select a valid choice', form.errors['gender'][0])

    def test_password_mismatch(self):
        # Test password validation
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'WrongPassword123!'
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn("The two password fields didn’t match", form.errors['password2'][0])
