from django.contrib import admin

from .models import (BaseChain, OtherVariant, ContactClient, Calculation, BrandChain, TypeDelivery, DeliveryRate,
                     Client, Country)
from searchableselect.widgets import SearchableSelect
from import_export.admin import ImportExportModelAdmin
from import_export import resources


# region БАЗОВЫЕ ФУНКЦИИ И КЛАССЫ

def views_admin_panel(models_: tuple):
    for model in models_:
        admin.site.register(model)

#TODO: переписать с ипользованием ->type или не надо???(плохо читаемо)
def imp_exp_model_data(dict_mdl_flds):
    for model_, fields_ in dict_mdl_flds.items():

        class Base_Resource(resources.ModelResource):
            class Meta:
                model = model_

        @admin.register(model_)
        class Base_Admin(ImportExportModelAdmin):
            if fields_[0]:
                search_fields = fields_[0]
            if fields_[1]:
                list_filter = fields_[1]

            resource_class = Base_Resource


# endregion

# добавление в административную часть модели с возможностью експорта и импорта данных
#                        - пример: ИмяМодели:[[список полей для поиска], [список полей для фильтрации]]
# если не нужны, то пустой список: ИмяМодели:[ [], [] ]
dict_models_imp_exp = {BaseChain: [['name_chains'], ['standard']],
                       OtherVariant: [[], ['brand__name_brand']],
                       Client: [['name', 'unp'], []],
                       Country:[[], []],
                       DeliveryRate:[[], []],
                       }

imp_exp_model_data(dict_models_imp_exp)

tuple_models_adm_pnl = (ContactClient,BrandChain,TypeDelivery,Calculation)
views_admin_panel(tuple_models_adm_pnl)
