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
        model = GroupModel
        fields = '__all__'

class UserObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['id_g', 'название']

class UserTestsForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ['id_o', 'испытание', 'метрика', 'рекомендация']

class UserStandardsForm(forms.ModelForm):
    class Meta:
        model = Standards
        fields = ['id_o', 'стандарт', 'требование']