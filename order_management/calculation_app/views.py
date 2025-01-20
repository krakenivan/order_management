from django.shortcuts import render
from common.models import Order
from django.db.models import Sum


# Create your views here.
def calculation(request):
    calculat_paid = Order.objects.filter(status="paid").aggregate(Sum("total_price"))[
        "total_price__sum"
    ]
    more_to_be_paid = Order.objects.filter(
        status__in=["expectation", "done"]
    ).aggregate(Sum("total_price"))
    unpaid = Order.objects.filter(status__in=["expectation", "done"])
    count_unpaid = len(unpaid)
    count_all = len(Order.objects.all())
    data = {
        "calculat_paid": calculat_paid,
        "more_to_be_paid": more_to_be_paid,
        "unpaid": unpaid,
        "count_unpaid": count_unpaid,
        "count_all": count_all
    }
    return render(request, "calculation_app/calculation.html", context=data)
