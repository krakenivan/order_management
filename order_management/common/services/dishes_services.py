"""Сервисы работающие с объектами модели Dishes"""

from .model_services import create_objects, all_objects, get_object, filter_objects
from ..models import Dishes


def create_dishes(**kwargs):
    """добавление новых блюд в заказ"""
    dishes = create_objects(Dishes.objects, **kwargs)
    return dishes


def current_dishes_of_order(order, **kwargs):
    """получить блюда в заказе"""
    dishes = all_objects(order.dishes_set, **kwargs)
    return dishes


def get_id_product_of_dish(dish):
    """получить id продукта из блюда"""
    return dish.product.id


def get_dish_by_product_id(objects, product_id):
    """получить блюдо по id продукта"""
    dish = objects.get(product_id=product_id)
    # dish = get_object(objects, product_id=product_id)
    return dish


def get_dish(**kwargs):
    """получение блюда"""
    dish = get_object(Dishes.objects, **kwargs)
    return dish


def check_product_id_in_dishes(objects, **kwargs):
    """проверка наличия продукта по id в блюдах заказа"""
    return filter_objects(objects=objects, exists=True, **kwargs)
