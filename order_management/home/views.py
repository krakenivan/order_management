from datetime import date

from django.views.generic import TemplateView

from common.services.analytics_services import analytics
from common.services.order_services import exclude_order, filter_order
from common.services.table_services import filter_table


class HomeViews(TemplateView):
    """Главная страница"""

    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = exclude_order(status__in=["paid", "completed"])
        tables = filter_table(status="free")
        today = date.today()
        today_orders = filter_order(datetime__gte=today)
        dict_analytics = analytics(orders=today_orders, home=True)
        context["orders"] = orders
        context["tables"] = tables
        return context | dict_analytics
