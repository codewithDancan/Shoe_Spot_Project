from django.forms import Form, ModelForm
from django import forms 
from django.core.validators import EmailValidator, validate_email
from .models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput)

class UserUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]



class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'

