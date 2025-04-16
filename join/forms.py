from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.fields['signature'].required = False  # Make signature optional
