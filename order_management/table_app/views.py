from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django.urls import reverse_lazy

from common.models import Table
from common.services.table_services import work_orders_at_table

from . import forms


class TableViews(ListView):
    """Список столов"""

    template_name = "table_app/table.html"
    model = Table
    context_object_name = "tables"


class EditTableViews(UpdateView):
    """Изменение столов"""

    model = Table
    form_class = forms.UpdateTableForms
    template_name = "table_app/edit_table.html"
    success_url = reverse_lazy("table")

    def get_object(self, queryset=None):
        self.order = work_orders_at_table(table_id=self.kwargs["pk"])
        return super().get_object(queryset)

    def get_template_names(self):
        # Если есть заказы в работе за столом блокируем изменение стола
        if self.order:
            return ["table_app/table_locked.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_table"] = True
        context["orders"] = self.order
        return context


class AddTableViews(CreateView):
    """Добавление стола"""

    model = Table
    form_class = forms.CreateTableForms
    template_name = "table_app/add_table.html"
    success_url = reverse_lazy("table")


class DeleteTableViews(DeleteView):
    """Удаление стола"""

    template_name = "table_app/delete_table.html"
    model = Table
    success_url = reverse_lazy("table")

    def get_object(self, queryset=None):
        self.order = work_orders_at_table(table_id=self.kwargs["pk"])
        return super().get_object(queryset)

    def get_template_names(self):
        if self.order:
            return ["table_app/table_locked.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_table"] = True
        context["orders"] = self.order
        return context
