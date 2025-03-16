"""Сервисы работающие с объектами модели Table"""

from .model_services import exclude_objects
from ..models import Table

def current_table_order(table):
    """получение действующего заказа за переданным столом"""
    return exclude_objects(table.order_set, status="completed")

def switch_table_status(table, status):
    """переключение статуса стола"""
    if status == 'busy':
        table.status = Table.Status.BUSY
    elif status == "free":
        table.status = Table.Status.FREE

def check_table_status(table, status):
    """проверка статуса стола"""
    return table.status == status