from common.models import Table, Order
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView,
)
from . import forms
from django.urls import reverse_lazy


class TableViews(ListView):
    template_name = "table_app/table.html"
    model = Table
    context_object_name = "tables"


class EditTableViews(UpdateView):
    model = Table
    form_class = forms.UpdateTableForms
    template_name = "table_app/edit_table.html"
    success_url = reverse_lazy("table")

    def get_object(self, queryset=None):
        # Сохраняем объект до изменений
        self.order = Order.objects.exclude(status__in=["paid", "completed"]).filter(
            table_number=self.kwargs["pk"]
        )
        return super().get_object(queryset)

    def get_template_names(self):
        # Проверяем, есть ли записи в таблице Order
        if self.order:
            return ["table_app/table_locked.html"]
        return [self.template_name]  # Стандартный шаблон

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_table"] = True
        context["orders"] = self.order
        return context


class AddTableViews(CreateView):
    model = Table
    form_class = forms.CreateTableForms
    template_name = "table_app/add_table.html"
    success_url = reverse_lazy("table")


class DeleteTableViews(DeleteView):
    template_name = "table_app/delete_table.html"
    model = Table
    success_url = reverse_lazy("table")

    def get_object(self, queryset=None):
        # Сохраняем объект до изменений
        self.order = Order.objects.exclude(status__in=["paid", "completed"]).filter(
            table_number=self.kwargs["pk"]
        )
        return super().get_object(queryset)

    def get_template_names(self):
        # Проверяем, есть ли записи в таблице Order
        if self.order:
            return ["table_app/table_locked.html"]
        return [self.template_name]  # Стандартный шаблон

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_table"] = True
        context["orders"] = self.order
        return context
