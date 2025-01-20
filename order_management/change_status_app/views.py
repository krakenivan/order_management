from django.shortcuts import render
from common.models import Order
# Create your views here.

def change_status(request):
    list_status = Order.Status.values
    orders = Order.objects.all()
    if request.method == "POST":
        # Получаем данные из формы
        post_data = request.POST.dict()
        data = {
            key: val
            for key, val in post_data.items()
            if key != "csrfmiddlewaretoken" and val
        }
        changes = '-'
        for id, value in data.items():
            order = Order.objects.get(id=id)
            if order.status == value:
                continue
            else:
                new_status = None
                if value == "expectation":
                    new_status = Order.Status.EXPECTATION
                if value == "done":
                    new_status = Order.Status.DONE
                if value == "paid":
                    new_status = Order.Status.PAID
                order.status = new_status
                order.save()
                changes = '+'
        return render(
            request,
            "change_status_app/change_status.html",
            context={"orders": orders, "stat": list_status, "changes": changes},
        )
    return render(request, "change_status_app/change_status.html", context={'orders':orders, 'stat':list_status})

def change_one_status(request, order_id):
    list_status = Order.Status.values
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        # Получаем данные из формы
        post_data = request.POST.dict()
        data = {
            key: val
            for key, val in post_data.items()
            if key != "csrfmiddlewaretoken" and val
        }
        changes = "-"
        for id, value in data.items():
            order = Order.objects.get(id=id)
            if order.status == value:
                continue
            else:
                new_status = None
                if value == "expectation":
                    new_status = Order.Status.EXPECTATION
                if value == "done":
                    new_status = Order.Status.DONE
                if value == "paid":
                    new_status = Order.Status.PAID
                order.status = new_status
                order.save()
                changes = "+"
        return render(
            request,
            "change_status_app/one_order.html",
            context={"order": order, "stat": list_status, "changes": changes},
        )
    return render(
        request,
        "change_status_app/one_order.html",
        context={"order": order, "stat": list_status},
    )
