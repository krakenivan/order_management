from django.http import HttpResponse
from django.shortcuts import render
from common.models import Order
from . import forms
from datetime import timedelta
from common.services import analytics_services as an_serv


# Create your views here.
def calculation(request) -> HttpResponse:
    """Расчет текущих показателей выручки и тд"""
    filter = True
    orders = Order.objects.all()
    form = forms.DateFilterForm(request.GET or None)
    name = "Расчет за все время"
    if form.is_valid():
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        if start_date and end_date:
            if start_date == end_date:
                orders = orders.filter(datetime__gte=start_date).exclude(
                    datetime__gte=end_date + timedelta(days=1)
                )
            else:
                orders = orders.filter(datetime__range=[start_date, end_date])
        elif start_date:
            orders = orders.filter(datetime__gte=start_date)
        elif end_date:
            orders = orders.filter(datetime__lte=end_date)
        name = "Расчет за указанный период"
    if not orders:
        filter = False
    analytics = an_serv.analytics(orders=orders)
    data = {
        "name": name,
        "filter": filter,
        "form": form,
    } | analytics
    return render(request, "calculation_app/calculation.html", context=data)
