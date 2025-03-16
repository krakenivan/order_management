"""Сервисы для работы объектами форм"""


def get_object_form(form, key):
    """получение объекта из формы по ключу"""
    return form.cleaned_data.get(key)


def save_modelform_with_prefix(request, forms, object):
    form = forms(request.POST, prefix=str(object.id), instance=object)
    if form.is_valid():
        form.save()


def creating_modelform_with_prefix(forms, object):
    form = forms(prefix=str(object.id), instance=object)
    return form
