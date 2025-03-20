"""Сервисы работающие с объектами модели Table"""

from .model_services import exclude_objects, get_object, filter_objects
from .order_services import exclude_order
from ..models import Table


def current_table_order(table):
    """получение действующего заказа за переданным столом"""
    return exclude_objects(table.order_set, status="completed")


def work_orders_at_table(table_id):
    """получение рабочих заказов за переданным столом"""
    return filter_objects(exclude_order(status__in=["paid", "completed"]), table_number=table_id)


def switch_table_status(table, status):
    """переключение статуса стола"""
    if status == "busy":
        table.status = Table.Status.BUSY
    elif status == "free":
        table.status = Table.Status.FREE


def check_table_status(table, status):
    """проверка статуса стола"""
    return table.status == status


def get_table(**kwargs):
    """получение стола"""
    table = get_object(Table.objects, **kwargs)
    return table


def filter_table(**kwargs):
    """получение столов по фильтру"""
    tables = filter_objects(Table.objects, **kwargs)
    return tables
