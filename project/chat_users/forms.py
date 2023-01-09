from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']



