from django.shortcuts import render
from common.models import Order

# Create your views here.
def show_orders(request):
    orders = Order.objects.all()
    return render(request, "show_orders_app/table_orders.html", context={'orders':orders})