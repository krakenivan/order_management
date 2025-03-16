from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from common.services.order_services import create_order, filter_order
from common.services.product_services import all_product
from common.services.table_services import (
    current_table_order,
    switch_table_status,
    check_table_status,
)
from common.services.dishes_services import create_dishes
from common.services.form_services import get_object_form
from common.services.model_services import save_objects

from . import forms


class CreateOrderViews(FormView):
    """Добавление заказа"""

    form_class = forms.OrderForm
    template_name = "add_order_app/creating.html"
    success_url = reverse_lazy("completing_add_order")

    def form_valid(self, form):
        table = get_object_form(form, key="table_number")
        if check_table_status(table, status="busy"):
            ordering_at_the_table = current_table_order(table)
            return render(
                self.request,
                "table_app/table_locked.html",
                context={"orders": ordering_at_the_table},
            )
        order = create_order(table)
        for product in all_product(only=("id",)):
            field_name = f"product_{product.id}"
            quantity_name = f"quantity_{product.id}"
            if get_object_form(form, key=field_name):
                quantity = form.cleaned_data.get(quantity_name, 1)
                create_dishes(order_id=order, product=product, quantity=quantity)
        order.calculation_total_price()
        switch_table_status(table, status="busy")
        save_objects(table)
        self.success_url = f"{reverse_lazy('completing_add_order')}?order_id={order.id}"
        return super().form_valid(form)


class CompletingAddOrderViews(TemplateView):
    """Отображение добавленного заказа"""

    template_name = "add_order_app/completing_add_order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get("order_id")
        orders = filter_order(id=order_id)
        context["orders"] = orders
        return context
