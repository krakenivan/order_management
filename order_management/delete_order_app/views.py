from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from common.models import Order
from common.services.table_services import switch_table_status
from common.services.model_services import save_objects
from common.services.order_services import exclude_order


class ChoiceOfDeleteOrderViews(ListView):
    model = Order
    template_name = "delete_order_app/choosing_delete.html"
    context_object_name = "orders"

    def get_template_names(self):
        order = exclude_order(status__in=["paid", "completed"])
        if not order:
            return ["show_orders_app/no_orders.html"]
        return [self.template_name]


class ConfirmationOfDeletionOrderViews(DeleteView):
    template_name = "delete_order_app/confirm_delete.html"
    model = Order
    success_url = reverse_lazy("show_orders")

    def form_valid(self, form):
        table = self.object.table_number
        switch_table_status(table, status="free")
        save_objects(table)
        return super().form_valid(form)
