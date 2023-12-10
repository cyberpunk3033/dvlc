# FORMS
from .models import Client, Calculation
from django import forms
from dal import autocomplete


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude=['user']


class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        exclude=('user','days','data_delivery','created','price_full','price_1m','weight','price_calc_weight')
        widgets = {
            'test': autocomplete.ModelSelect2(url='select2_fk')
        }







