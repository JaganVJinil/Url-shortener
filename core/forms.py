from django import forms
from .models import ShortURL
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class URLForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['title', 'original_url']

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
