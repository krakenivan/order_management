import logging
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages


from common.models import Order
from common.services.form_services import (
    save_modelform_with_prefix,
    creating_modelform_with_prefix,
    comparison_with_object_from_form,
)
from common.services.order_services import get_order, current_order_table
from common.services.table_services import switch_table_status
from common.services.model_services import save_objects

from . import forms

logger = logging.getLogger("info")


class ChangeOrderStatusViews(ListView):
    """Изменение статусов заказов"""

    model = Order
    template_name = "change_status_app/change_status.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = [
            {
                "order": order,
                "status_form": creating_modelform_with_prefix(
                    forms.StatusOrderForm, order
                ),
            }
            for order in context["orders"]
        ]
        return context

    def post(self, request, *args, **kwargs):
        for order in self.get_queryset():
            form = save_modelform_with_prefix(request, forms.StatusOrderForm, order)
            table = current_order_table(order)
            if comparison_with_object_from_form(
                form, key="status", check_data="completed"
            ):
                switch_table_status(table, "free")
                save_objects(table)
                messages.success(self.request, "Статус изменен!")
        logger.info("Выбранные статусы успешно изменены!")
        return redirect("change_status")


class ChangeOneOrderStatusViews(DetailView):
    """Изменение статуса одного заказа"""

    template_name = "change_status_app/one_order.html"
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = context["order"]
        context["status_form"] = creating_modelform_with_prefix(
            forms.StatusOrderForm, order
        )
        return context

    def post(self, request, *args, **kwargs):
        order = get_order(pk=kwargs["pk"])
        form = save_modelform_with_prefix(request, forms.StatusOrderForm, order)
        table = current_order_table(order)
        if comparison_with_object_from_form(form, key="status", check_data="completed"):
            switch_table_status(table, "free")
            save_objects(table)
            messages.success(self.request, "Статус изменен!")
        logger.info(f"Статус заказа номер {order.id} успешно изменен!")
        messages.success(self.request, "Статус изменен!")
        return redirect(f"/one-status/{order.id}")
