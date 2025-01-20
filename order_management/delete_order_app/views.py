from django.shortcuts import render
from common.models import Order, Dishes


# Create your views here.
def choosing_delete(request):
    data = Order.objects.all()
    if not data:
        return render(request, "delete_order_app/no_order.html")
    return render(
        request, "delete_order_app/choosing_delete.html", context={"orders": data}
    )

def delete(request):
    if request.method == "POST":
        # Получаем данные из формы
        order_id = request.POST['delete']
        order_del = Order.objects.get(id=order_id)
        dishes_del = Dishes.objects.filter(order_id=order_id)
        dishes_del.delete()
        order_del.delete()
    return render(
        request, "delete_order_app/delete.html"
    )
