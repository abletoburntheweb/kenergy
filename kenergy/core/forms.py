# core/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    is_admin = forms.BooleanField(
        required=False,
        label="Администратор",
        help_text="Отметьте, если пользователь должен быть администратором."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_admin']