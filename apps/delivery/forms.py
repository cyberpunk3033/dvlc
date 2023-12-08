# FORMS
from dal import autocomplete

from .models import Client, Calculation

from django import forms
from searchableselect.widgets import SearchableSelect




class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user',)



class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation

        exclude = ('user', 'days', 'data_delivery', 'created', 'price_full', 'price_1m', 'weight', 'price_calc_weight')
        widgets = {
            'inspection_type': SearchableSelect(model='Calculation', search_field='client', many=False, limit=10),

        }
