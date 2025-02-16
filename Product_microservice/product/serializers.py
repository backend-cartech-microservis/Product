from rest_framework import serializers


class ProductAddSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.CharField()

# class 