from common.models import Order
from django.views.generic import ListView, TemplateView


class ShowOrdersViews(ListView):
    template_name = "show_orders_app/orders.html"
    model = Order
    context_object_name = "orders"


class Ord(TemplateView):
    template_name = "show_orders_app/no_orders.html"
