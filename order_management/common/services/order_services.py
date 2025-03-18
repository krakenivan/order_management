"""Сервисы работающие с объектами модели Order"""

from .model_services import create_objects, filter_objects, get_object, exclude_objects
from ..models import Order


def create_order(table):
    """добавление нового заказа"""
    order = create_objects(Order.objects, table_number=table)
    return order


def filter_order(**kwargs):
    """получение заказов по фильтру"""
    orders = filter_objects(Order.objects, **kwargs)
    return orders


def exclude_order(**kwargs):
    """исключение заказов"""
    orders = exclude_objects(Order.objects, **kwargs)
    return orders


def get_order(**kwargs):
    """получение заказа"""
    order = get_object(Order.objects, **kwargs)
    return order


def current_order_table(order):
    """получение стола заказа"""
    table = order.table_number
    return table
