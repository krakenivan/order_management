from django.views.generic import ListView, TemplateView

from common.models import Order


class ShowOrdersViews(ListView):
    """отображение всех заказов"""
    template_name = "show_orders_app/orders.html"
    model = Order
    context_object_name = "orders"


class NoOrdersViews(TemplateView):
    """отображение шаблона при отсутствии заказа"""
    template_name = "show_orders_app/no_orders.html"
