# forms.py
from django import forms

class InputForm(forms.Form):
    user_input = forms.CharField(
        label='Prompt here..', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'large-input'})
    )