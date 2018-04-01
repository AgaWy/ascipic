
from django import forms
from .models import Image
from django.contrib.auth import authenticate



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField()


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('name', 'path', )
