from django import forms
from .models.business_model import Business

class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ['user']