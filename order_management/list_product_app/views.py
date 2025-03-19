from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView
from django.contrib import messages

from common.models import Product
from common.services.form_services import get_object_form
from common.services.model_services import delete_objects

from . import forms


class ProductViews(ListView):
    """отображение всех продуктов"""
    template_name = "list_product_app/product.html"
    model = Product
    context_object_name = "products"


class AddProductViews(CreateView, ListView):
    """Добавление продуктов"""
    model = Product
    form_class = forms.AddProductForm
    template_name = "list_product_app/add_product.html"
    context_object_name = "products"

    def form_valid(self, form):
        response = super().form_valid(form)
        # Добавляем сообщение об успешном добавлении
        messages.success(self.request, "Блюдо успешно добавлено!")
        return response

    def get_success_url(self):
        # Возвращаем URL текущей страницы
        return self.request.path


class DeleteProductViews(FormView):
    """Удаление продуктов"""
    form_class = forms.DeleteProductForm
    template_name = "list_product_app/delete_product.html"
    success_url = reverse_lazy("delete_product")

    def form_valid(self, form):
        # Получаем выбранные записи и удаляем их
        select_product = get_object_form(form, "select_product")
        delete_objects(select_product)
        messages.success(self.request, "Блюдо успешно удалено!")
        return super().form_valid(form)
