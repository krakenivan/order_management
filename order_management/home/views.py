from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from common.models import Order, Table
from datetime import date
from common.services import analytics_services as an_serv

# Create your views here.


def index(request):
    """главная страница"""
    return render(request, "home/index.html")


class HomeViews(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        orders = Order.objects.exclude(status__in=["paid", "completed"])
        tables = Table.objects.filter(status="free")
        today = date.today()
        today_orders = Order.objects.filter(datetime__gte=today)
        analytics = an_serv.analytics(orders=today_orders, home=True)
        context["orders"] = orders
        context["tables"] = tables
        return context | analytics
