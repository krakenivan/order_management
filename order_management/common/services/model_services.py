"""Общие сервисы работающие с объектами моделей"""

from functools import wraps
from django.db.models import Manager


def only_objects_decorator(func):
    """декоратор получения полей через only()"""

    @wraps
    def wrapper(objects, only=(), *args, **kwargs):
        return func(objects, *args, **kwargs).only(*only)

    return wrapper


@only_objects_decorator
def all_objects(objects: Manager):
    """получение всех объектов"""
    return objects.all()


@only_objects_decorator
def filter_objects(objects: Manager, **kwargs):
    """фильтр объектов"""
    return objects.filter(**kwargs)


@only_objects_decorator
def exclude_objects(objects: Manager, **kwargs):
    """исключение объектов"""
    return objects.exclude(**kwargs)


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
