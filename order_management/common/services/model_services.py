"""
Общие сервисы работающие с объектами моделей
"""

import logging
from django.db.models import Manager

logger = logging.getLogger("info")


def only_objects_decorator(func):
    """декоратор получения полей через only()"""

    def wrapper(objects, only=(), *args, **kwargs):
        return func(objects, *args, **kwargs).only(*only)

    return wrapper


def exists_objects_decorator(func):
    """декоратор проверки наличия значений в поле"""

    def wrapper(objects, exists=True, *args, **kwargs):
        if exists:
            func(objects, *args, **kwargs).exists()
        return func(objects, *args, **kwargs)

    return wrapper


@only_objects_decorator
def all_objects(objects: Manager):
    """получение всех объектов"""
    return objects.all()


@exists_objects_decorator
@only_objects_decorator
def filter_objects(objects: Manager, **kwargs):
    """фильтр объектов"""
    return objects.filter(**kwargs)


@exists_objects_decorator
@only_objects_decorator
def exclude_objects(objects: Manager, **kwargs):
    """исключение объектов"""
    return objects.exclude(**kwargs)


@only_objects_decorator
def get_object(objects, **kwargs):
    """получение объекта"""
    return objects.get(**kwargs)


def create_objects(objects: Manager, **kwargs):
    """добавление объектов"""
    query = objects.create(**kwargs)
    return query


def save_objects(objects):
    """сохранение объекта"""
    objects.save()
    logger.info(f"Объект {objects} сохранен в БД!")


def delete_objects(objects):
    """удаление объекта"""
    objects.delete()
    logger.info(f"Объект {objects} удален из БД!")
