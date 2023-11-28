
from rest_framework.serializers import ModelSerializer
from .models import Calculation

class CalculationSerializer(ModelSerializer):
    class Meta:
        model = Calculation
        fields = ['client', 'type_delivery', 'contact_client', 'base_chain',
                  'brand', 'type_processing', 'weight', 'days', 'created', 'data_delivery']


