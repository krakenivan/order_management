from django.http import HttpResponse
from django.shortcuts import render
from common.models import Order


# Create your views here.
def find_order(request) -> HttpResponse:
    """Поиск заказа по id или столу"""
    if request.method == "POST":
        # Получаем данные из формы
        select = request.POST['select']
        find = request.POST["find"]
        if select == 'table_number':
            orders = Order.objects.filter(table_number=find)
        elif select == 'status':
            orders = Order.objects.filter(status=find)
        return render(request, "find_order_app/find_order.html", context={'orders':orders})
    return render(request, "find_order_app/find_order.html")
