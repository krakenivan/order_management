from django.urls import reverse_lazy
from common.models import Product
from django.views.generic import ListView, CreateView, FormView
from . import forms
from django.contrib import messages


class ProductViews(ListView):
    template_name = "list_product_app/product.html"
    model = Product
    context_object_name = "products"


class AddProductViews(CreateView, ListView):
    model = Product
    form_class = forms.AddProductForm
    template_name = "list_product_app/add_product.html"
    context_object_name = "products"

    def form_valid(self, form):
        # Сохраняем форму
        response = super().form_valid(form)
        # Добавляем сообщение об успешном добавлении
        messages.success(self.request, "Блюдо успешно добавлено!")
        # Возвращаем ответ
        return response

    def get_success_url(self):
        # Возвращаем URL текущей страницы
        return self.request.path


class DeleteProductViews(FormView):
    form_class = forms.DeleteProductForm
    template_name = "list_product_app/delete_product.html"
    success_url = reverse_lazy("delete_product")

    def form_valid(self, form):
        # Получаем выбранные записи и удаляем их
        select_product = form.cleaned_data["select_product"]
        select_product.delete()
        messages.success(self.request, "Блюдо успешно удалено!")
        return super().form_valid(form)
