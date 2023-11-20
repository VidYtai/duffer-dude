from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class ChangeUserDetailsForm(UserChangeForm):
    class Meta:
        model = User  # or your custom user model
        fields = ['username', 'first_name', 'last_name', 'email']