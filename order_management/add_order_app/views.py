from django.shortcuts import render
from common.models import Dishes, Order, Product, Table
from django.views.generic import FormView, TemplateView
from . import forms
from django.urls import reverse_lazy


class CreateOrderViews(FormView):
    form_class = forms.OrderForm
    template_name = "add_order_app/creating.html"
    success_url = reverse_lazy("completing_add_order")

    def form_valid(self, form):
        table = form.cleaned_data.get("table_number")
        if table.status == "busy":
            ordering_at_the_table = table.order_set.exclude(status="completed")
            return render(
                self.request,
                "add_order_app/table_is_locked.html",
                context={"orders": ordering_at_the_table},
            )
        order = Order.objects.create(table_number=table)
        for product in Product.objects.all():
            field_name = f"product_{product.id}"
            quantity_name = f"quantity_{product.id}"
            if form.cleaned_data.get(field_name):
                quantity = form.cleaned_data.get(quantity_name, 1)
                dishes = Dishes.objects.create(
                    product=product, quantity=quantity, order_id=order
                )
        order.calculation_total_price()
        table.status = Table.Status.BUSY
        table.save()
        self.success_url = f"{reverse_lazy('completing_add_order')}?order_id={order.id}"
        return super().form_valid(form)


class TableLockedViews(TemplateView):
    template_name = "add_order_app/table_is_locked.html"


class CompletingAddOrderViews(TemplateView):
    template_name = "add_order_app/completing_add_order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get("order_id")
        orders = Order.objects.filter(id=order_id)
        context["orders"] = orders
        return context
