from django.contrib import admin
from .models import (BaseChain, OtherVariant,ContactClient,Calculation,BrandChain,TypeDelivery,DeliveryRate,Client)
from import_export.admin import ImportExportModelAdmin
from import_export import resources

#region БАЗОВЫЕ ФУНКЦИИ И КЛАССЫ

def views_admin_panel(models_:tuple):

    for model in models_:
        admin.site.register(model)

def imp_exp_model_data(models_:tuple):
    #list_filter_=('',)

    for model_ in models_:

        class Base_Resource(resources.ModelResource):
            class Meta:
                model = model_

        @admin.register(model_)
        class Base_Admin(ImportExportModelAdmin):
            resource_class = Base_Resource

# endregion


tuple_models_imp_exp=(BaseChain,BrandChain,OtherVariant,DeliveryRate,TypeDelivery)
imp_exp_model_data(tuple_models_imp_exp)


tuple_models_adm_pnl=(Calculation,Client,ContactClient)
views_admin_panel(tuple_models_adm_pnl)




'''
class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        exclude = ()
        widgets = {
            'cities_visited': SearchableSelect(model='cities.City', search_field='name', limit=10)
        }


class CalculationAdmin(admin.ModelAdmin):
    form = CalculationForm

admin.site.register(Calculation, CalculationAdmin)
'''