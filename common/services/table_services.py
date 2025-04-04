"""
Сервисы работающие с объектами модели Table
"""

import logging
from .model_services import exclude_objects, get_object, filter_objects
from .order_services import exclude_order
from ..models import Table

logger = logging.getLogger("info")


def current_table_order(table: Table):
    """получение действующего заказа за переданным столом"""
    order = exclude_objects(table.order_set, status__in=["paid", "completed"])
    logger.info("Действующий заказ за столом получен из БД!")
    return order


def work_orders_at_table(table_id):
    """получение рабочих заказов за переданным столом по id"""
    orders = filter_objects(
        exclude_order(status__in=["paid", "completed"]), table_number=table_id
    )
    logger.info("Рабочие заказы за столом получены из БД!")
    return orders


def switch_table_status(table: Table, status: str):
    """переключение статуса стола"""
    if status == "busy":
        table.status = Table.Status.BUSY
    elif status == "free":
        table.status = Table.Status.FREE
    logger.info("Статус стола изменен в БД!")


def check_table_status(table: Table, status):
    """проверка статуса стола"""
    return table.status == status


def get_table(**kwargs):
    """получение стола"""
    table = get_object(Table.objects, **kwargs)
    logger.info("Стол получен из БД!")
    return table


def filter_table(**kwargs):
    """получение столов по фильтру"""
    tables = filter_objects(Table.objects, **kwargs)
    logger.info("Столы по фильтру получены из БД!")
    return tables
