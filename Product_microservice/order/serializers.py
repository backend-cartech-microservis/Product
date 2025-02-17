from rest_framework import serializers

class OrderAddSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()