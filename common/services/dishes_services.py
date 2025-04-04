"""
Сервисы работающие с объектами модели Dishes
"""
import logging
from django.db.models import QuerySet
from .model_services import create_objects, all_objects, get_object, filter_objects
from ..models import Dishes, Order

logger = logging.getLogger('info')

def create_dishes(**kwargs):
    """добавление новых блюд в заказ"""
    dishes = create_objects(Dishes.objects, **kwargs)
    logger.info('Новое блюдо добавлено в БД!')
    return dishes


def current_dishes_of_order(order: Order, **kwargs):
    """получить блюда в заказе"""
    dishes = all_objects(order.dishes_set, **kwargs)
    logger.info("Блюда в заказе получены из БД!")
    return dishes


def get_id_product_of_dish(dish: Dishes):
    """получить id продукта из блюда"""
    return dish.product.id


def get_dish_by_product_id(objects: QuerySet[Dishes], product_id):
    """получить блюдо по id продукта"""
    dish = objects.get(product_id=product_id)
    logger.info("Блюдо по id продукта получено из БД!")
    return dish


def get_dish(**kwargs):
    """получение блюда"""
    dish = get_object(Dishes.objects, **kwargs)
    logger.info("Блюдо получено из БД!")
    return dish


def check_product_id_in_dishes(objects: QuerySet[Dishes], **kwargs):
    """проверка наличия продукта по id в блюдах заказа"""
    return filter_objects(objects=objects, exists=True, **kwargs)
