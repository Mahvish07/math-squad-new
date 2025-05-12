from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['contest']  # Only include fields that exist in the model
        widgets = {
            'contest': forms.HiddenInput()
        }