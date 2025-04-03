from rest_framework import serializers
from common.models import Order, Table, Dishes, Product


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ("number", "places", "status")


class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
