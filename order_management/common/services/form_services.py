"""
Сервисы для работы объектами форм
"""

import logging

logger = logging.getLogger("info")


def get_object_form(form, key: str):
    """получение объекта из формы по ключу"""
    object = form.cleaned_data.get(key)
    logger.info("Объект из формы получен!")
    return object


def save_modelform_with_prefix(request, forms, object):
    """сохранение формы с префиксом"""
    form = forms(request.POST, prefix=str(object.id), instance=object)
    if form.is_valid():
        form.save()
        logger.info("Форма с префиксом сохранена!")
    return form


def creating_modelform_with_prefix(forms, object):
    """создание формы с префиксом"""
    form = forms(prefix=str(object.id), instance=object)
    logger.info("Форма с префиксом создана!")
    return form


def comparison_with_object_from_form(form, key: str, check_data):
    """сравнение объекта полученного из формы по ключу с переданными данными"""
    return get_object_form(form, key) == check_data


def is_selected_product(data):
    """проверка выбора блюд в очищенных данных формы"""
    products_selected = any(
        field_name.startswith("product_") and value
        for field_name, value in data.items()
    )
    return products_selected
