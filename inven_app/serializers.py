from rest_framework import serializers
from .models import *

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = '__all__'
