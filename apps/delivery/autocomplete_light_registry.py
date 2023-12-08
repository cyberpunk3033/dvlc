import autocomplete_light as al
from .models import Client, BaseChain

al.register(Client,
search_fields=['^name'],
attrs={
'placeholder': 'Название контрагента',
'data-autocomplete-minimum-characters': 1,
},
widget_attrs={
'data-widget-maximum-values': 4,
'class': 'modern-style',
},
)

al.register(BaseChain,
search_fields=['^name'],
attrs={
'placeholder': 'Название базовой цепи',
'data-autocomplete-minimum-characters': 1,
},
widget_attrs={
'data-widget-maximum-values': 4,
'class': 'modern-style',
},
)