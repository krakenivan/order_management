from django.urls import reverse_lazy
from common.models import Order
from django.views.generic import ListView, DeleteView


class ChoiceOfDeleteOrderViews(ListView):
    model = Order
    template_name = "delete_order_app/choosing_delete.html"
    context_object_name = "orders"

    def get_template_names(self):
        # Проверяем, есть ли записи в таблице Order
        order = Order.objects.exclude(
        status__in=["paid", "completed"])
        if not order:
            return ["show_orders_app/no_orders.html"]
        return [self.template_name]  # Стандартный шаблон


class ConfirmationOfDeletionOrderViews(DeleteView):
    template_name = "delete_order_app/confirm_delete.html"
    model = Order
    success_url = reverse_lazy("show_orders")
