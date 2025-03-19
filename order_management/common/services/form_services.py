"""Сервисы для работы объектами форм"""


def get_object_form(form, key):
    """получение объекта из формы по ключу"""
    return form.cleaned_data.get(key)


def save_modelform_with_prefix(request, forms, object):
    """сохранение формы с префиксом"""
    form = forms(request.POST, prefix=str(object.id), instance=object)
    if form.is_valid():
        form.save()
    return form


def creating_modelform_with_prefix(forms, object):
    """создание формы с префиксом"""
    form = forms(prefix=str(object.id), instance=object)
    return form


def comparison_with_object_from_form(form, key, check_data):
    """сравнение объекта полученного из формы по ключу с переданными данными"""
    return get_object_form(form, key) == check_data
