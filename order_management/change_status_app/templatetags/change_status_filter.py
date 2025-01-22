from django import template
from common.models import Order

register = template.Library()


@register.filter(name="statedit")
def status_editor(value:list, status) -> list:
    """фильтр для ротация списка статусов

    :param value: список статусов
    :param status: текущий статус
    :return: результирующий список статусов
    """
    ind = value.index(status)
    res = [value[(i + ind) % len(value)] for i in range(len(value))]
    return res


@register.filter(name="statdisplay")
def status_display(value) -> str:
    """ тег отображения статуса"""
    stat_val = Order.Status.values
    stat_label = Order.Status.labels

    return stat_label[stat_val.index(value)]
