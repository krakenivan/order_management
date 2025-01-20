from django.shortcuts import render
from common.models import Dishes, Order, Product


# Create your views here.
def creating_order(request):
    products = Product.objects.all()
    return render(request, "add_order_app/creating.html", context={'products':products})


def add_order(request):
    if request.method == "POST":
        # Получаем данные из формы
        post_data = request.POST.dict()
        data = {
            key: val
            for key, val in post_data.items()
            if key != "csrfmiddlewaretoken" and val
        }
        if int(data["table"]) in Order.objects.exclude(status="paid").values_list("table_number", flat=True):
            order = Order.objects.exclude(status="paid").get(table_number=data["table"])
            return render(request, "add_order_app/there_is_order.html", context={'order':order})
        order = Order.objects.create(table_number=data["table"])
        for key, value in data.items():
            if key != "table":
                Dishes.objects.create(name=key, price=value, order_id=order)
        order.fill()
        return render(request, "add_order_app/add_order.html")
