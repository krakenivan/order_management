"""Сервисы работающие с объектами модели Product"""

from ..models import Product
from .model_services import all_objects, exclude_objects


def all_product(**kwargs):
    """получение всех продуктов"""
    return all_objects(Product.objects, **kwargs)


def exclude_product(**kwargs):
    """исключение продуктов"""
    product = exclude_objects(Product.objects, **kwargs)
    return product
