from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render

from common.services.analytics_services import analytics
from common.services.form_services import get_object_form
from common.services.order_services import all_order, filter_order, exclude_order_query


from . import forms


# Create your views here.
def calculation(request) -> HttpResponse:
    """Расчет текущих показателей выручки и тд"""
    filter = True
    orders = all_order()
    form = forms.DateFilterForm(request.GET or None)
    name = "Расчет за все время"
    if form.is_valid():
        start_date = get_object_form(form, "start_date")
        end_date = get_object_form(form, "end_date")
        if start_date and end_date:
            if start_date == end_date:
                orders = exclude_order_query(
                    filter_order(datetime__gte=start_date),
                    datetime__gte=end_date + timedelta(days=1),
                )
            else:
                orders = filter_order(datetime__range=[start_date, end_date])
        elif start_date:
            orders = filter_order(datetime__gte=start_date)
        elif end_date:
            orders = filter_order(datetime__lte=end_date)
        name = "Расчет за указанный период"
    if not orders:
        filter = False
    dict_analytics = analytics(orders=orders)
    data = {
        "name": name,
        "filter": filter,
        "form": form,
    } | dict_analytics
    return render(request, "calculation_app/calculation.html", context=data)
