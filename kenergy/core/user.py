# core/user.py
from django import forms
from .models import Inventory, Groups, Object, Tests, Standards
from .models import Groups as GroupModel

# Формы для пользователей
class UserInventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['название']

class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['id_i', 'название']

class UserObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['id_g', 'название']

class UserTestsForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ['испытание', 'рекомендация', 'метрика']

    def clean_метрика(self):
        метрика = self.cleaned_data['метрика']
        if метрика < 0:
            raise forms.ValidationError("Метрика не может быть отрицательной.")
        return метрика

class UserStandardsForm(forms.ModelForm):
    class Meta:
        model = Standards
        fields = ['id_o', 'стандарт', 'требование']