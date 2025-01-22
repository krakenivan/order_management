from django import template

register = template.Library()


@register.filter(name="tabedit")
def table_number_editor(value: list, table) -> list:
    """тег для ротация списка столов"""
    ind = value.index(table)
    res = [value[(i + ind) % len(value)] for i in range(len(value))]
    return res
