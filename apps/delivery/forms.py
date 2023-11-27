# FORMS
from .models import Client
from django import forms
class ClientForm(forms.ModelForm):
# определяем класс Meta, в котором указываем модель и поля, которые хотим отобразить в форме
    class Meta:
        model = Client
        fields = ['user', 'name', 'note', 'unp', 'email', 'phone', 'address']