from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from core.models import Object


class RegisterForm(UserCreationForm):
    is_admin = forms.BooleanField(
        required=False,
        label="Администратор",
        help_text="Отметьте, если пользователь должен быть администратором."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_admin']
        if commit:
            user.save()
        return user


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['id_g', 'name', 'description']
        widgets = {
            'id_g': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
