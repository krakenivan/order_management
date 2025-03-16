"""Сервисы для работы объектами форм"""

def get_object_form(form, key):
    """получение объекта из формы по ключу"""
    return form.cleaned_data.get(key)
