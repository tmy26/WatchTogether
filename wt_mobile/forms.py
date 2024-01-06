from django import forms
from .models import User

class MyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password',]