from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    class Meta:

        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:

        model = PurchaseOrder
        fields = ['id', 'vendor', 'items', 'quantity', 'status']


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:

        model = Vendor
        fields = ['name', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
