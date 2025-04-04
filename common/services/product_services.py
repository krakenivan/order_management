"""
Сервисы работающие с объектами модели Product
"""

import logging
from ..models import Product
from .model_services import all_objects, exclude_objects

logger = logging.getLogger("info")


def all_product(**kwargs):
    """получение всех продуктов"""
    products = all_objects(Product.objects, **kwargs)
    logger.info("Все продукты получены из БД!")
    return products


def exclude_product(**kwargs):
    """исключение продуктов"""
    product = exclude_objects(Product.objects, **kwargs)
    logger.info("Продукты с исключением получены из БД!")
    return product
