from django import forms
from django.contrib.auth.models import User
from .models import *

class TokenRequestForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['symptoms']
        widgets = {
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control w-full p-4 border rounded-xl focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Please describe your symptoms in detail (e.g., I have sharp chest pain and difficulty breathing)...',
                'rows': 4
            }),
        }
class PatientUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['phone', 'address', 'profile_pic']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Home Address', 'rows': 3}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }