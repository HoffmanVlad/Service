from products.models import Product
from rest_framework import serializers
from rest_framework import permissions

class ProductSerializerView(serializers.Serializer):
    class Meta:
        model = Product
        fields = ['first_name', 'last_name', 'image', 'email', 'company_name']


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['first_name', 'last_name', 'image', 'email', 'company_name']

