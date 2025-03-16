"""Сервисы работающие с объектами модели Dishes"""

from .model_services import create_objects
from ..models import Dishes


def create_dishes(order_id, product, quantity):
    """добавление новых блюд в заказ"""
    dishes = create_objects(
        Dishes.objects, order_id=order_id, product=product, quantity=quantity
    )
    return dishes
