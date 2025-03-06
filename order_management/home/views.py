from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from common.models import Order

# Create your views here.


def index(request):
    """главная страница"""
    return render(request, "home/index.html")


class HomeViews(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        orders = Order.objects.exclude(status="paid")
        context["orders"] = orders
        return context

