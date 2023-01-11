from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from chat_users.models import FriendRequest

User = get_user_model()


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['status']
