from django.shortcuts import render
from common.models import Order, Dishes


# Create your views here.
def find_order(request):
    if request.method == "POST":
        # Получаем данные из формы
        select = request.POST['select']
        find = request.POST["find"]
        if select == 'table_number':
            orders = Order.objects.filter(table_number=find)
        elif select == 'status':  # TODO доработать передачу find при поиске
            orders = Order.objects.filter(status=find)
        return render(request, "find_order_app/find_order.html", context={'orders':orders})
    return render(request, "find_order_app/find_order.html")
