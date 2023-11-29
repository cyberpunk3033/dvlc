# FORMS
from .models import Client, Calculation
from django import forms
from searchableselect.widgets import SearchableSelect

class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['name', 'note', 'unp', 'email', 'phone', 'address']




class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        exclude=('user',)
        widgets = {
        "client": SearchableSelect(model="app_name.Client", search_field="name", many=False),
        "type_delivery": SearchableSelect(model="app_name.TypeDelivery", search_field="name", many=False),
        "base_chain": SearchableSelect(model="app_name.BaseChain", search_field="name", many=False),
        "brand": SearchableSelect(model="app_name.BrandChain", search_field="name", many=False),
        "type_processing": SearchableSelect(model="app_name.OtherVariant", search_field="name", many=False),
        }