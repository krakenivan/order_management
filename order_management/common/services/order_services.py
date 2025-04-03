"""
Сервисы работающие с объектами модели Order
"""

import logging
from django.db.models import QuerySet
from .model_services import (
    create_objects,
    filter_objects,
    get_object,
    exclude_objects,
    all_objects,
)

from ..models import Order, Table

logger = logging.getLogger("info")


def create_order(table: Table):
    """добавление нового заказа"""
    order = create_objects(Order.objects, table_number=table)
    logger.info("Заказ добавлен в БД!")
    return order


def all_order(**kwargs):
    """получение всех заказов"""
    orders = all_objects(Order.objects, **kwargs)
    logger.info("Все заказы получены из БД!")
    return orders


def filter_order(**kwargs):
    """получение заказов по фильтру"""
    orders = filter_objects(Order.objects, **kwargs)
    logger.info("Заказы по фильтру получены из БД!")
    return orders


def exclude_order(**kwargs):
    """исключение заказов"""
    orders = exclude_objects(Order.objects, **kwargs)
    logger.info("Заказы с исключением получены из БД!")
    return orders


def exclude_order_query(query: QuerySet, **kwargs):
    """исключение заказов из выборки"""
    orders = exclude_objects(query, **kwargs)
    return orders


def get_order(**kwargs):
    """получение заказа"""
    order = get_object(Order.objects, **kwargs)
    logger.info("Заказ получен из БД!")
    return order


def current_order_table(order: Order):
    """получение стола заказа"""
    table = order.table_number
    logger.info("Стол для заказа получен из БД!")
    return table
