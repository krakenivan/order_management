"""Сервисы работающие с объектами модели Order"""

from .model_services import create_objects, filter_objects
from ..models import Order


def create_order(table):
    """добавление нового заказа"""
    order = create_objects(Order.objects, table_number=table)
    return order

def filter_order(**kwargs):
    """получение заказов по фильтру"""
    orders = filter_objects(Order.objects, **kwargs)
    return orders
