from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import (
    OrderSerializer,
    TableSerializer,
    DishesSerializer,
    ProductSerializer,
)
from common.models import Order, Table, Dishes, Product


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(methods=["get"], detail=True)
    def dishes(self, request, pk=None):
        """получаем блюда в заказе"""
        order = self.get_object()
        dishes = order.dishes_set.all()
        serializer = DishesSerializer(dishes, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def paid(self, request):
        """получаем оплаченные заказы"""
        paid = Order.objects.filter(status="paid")
        serializer = OrderSerializer(paid, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def products(self, request, pk=None):
        """получаем продукты и количество из заказа"""
        order = self.get_object()
        dishes = order.dishes_set.all()
        products = {dish.product.name: dish.quantity for dish in dishes}
        return Response(products)


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(methods=["get"], detail=False)
    def busy(self, request):
        """получаем занятые столы"""
        busy = Table.objects.filter(status="busy")
        serializer = TableSerializer(busy, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def free(self, request):
        """получаем свободные столы"""
        free = Table.objects.filter(status="free")
        serializer = TableSerializer(free, many=True)
        return Response(serializer.data)


class DishesViewSet(viewsets.ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer

    @action(methods=["get"], detail=True)
    def product(self, request, pk=None):
        """получаем название продукта и количество"""
        dish = self.get_object()
        product = dish.product.name
        return Response({"product": product, "quantity": dish.quantity})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
