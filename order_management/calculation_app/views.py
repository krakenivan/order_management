from django.http import HttpResponse
from django.shortcuts import render
from common.models import Order
from django.db.models import Sum
from . import forms
from datetime import timedelta


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
    count_all: int = len(orders)  # всего заказов

    calculat_all = orders.aggregate(Sum("total_price"))["total_price__sum"]
    calculat_paid = orders.filter(status="paid").aggregate(Sum("total_price"))[
        "total_price__sum"
    ]
    calculat_unpaid = orders.exclude(status__in=["paid", "completed"]).aggregate(
        Sum("total_price")
    )["total_price__sum"]
    more_to_be_paid = orders.filter(
        status__in=["expectation", "done"]
    ).count()  # суммы неоплаченных заказов
    unpaid = orders.filter(
        status__in=["expectation", "done"]
    )  # список неоплаченных заказов
    count_unpaid: int = len(unpaid)  # количество неоплаченных
    data = {
        "name": name,
        "filter": filter,
        "form": form,
        "count_all": count_all,
        "calculat_all": calculat_all,
        "calculat_paid": calculat_paid,
        "calculat_unpaid": calculat_unpaid,
        "more_to_be_paid": more_to_be_paid,
        "count_unpaid": count_unpaid,
        "orders": unpaid,
    }
    return render(request, "calculation_app/calculation.html", context=data)
