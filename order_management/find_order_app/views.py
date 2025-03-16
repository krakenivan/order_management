from django.http import HttpResponse
from django.shortcuts import render
from common.models import Order
from django.views.generic import FormView
from . import forms
from django.core.exceptions import ObjectDoesNotExist


class FindOrderViews(FormView):
    form_class = forms.FindOrderForm
    template_name = "find_order_app/find_order.html"

    def form_valid(self, form):
        message = "Найденные заказы"
        found = None
        select = form.cleaned_data["select"]
        if select == "id":
            id = form.cleaned_data["order_id_field"]
            orders = Order.objects.filter(id=id)
            if orders:
                found = orders
            else:
                message = f"Заказа с номером:{id} не найдено"
        if select == "table_number":
            table_number = form.cleaned_data["order_table_number_field"]
            orders = Order.objects.filter(table_number=table_number)
            if orders:
                found = orders
            else:
                message = f"Заказов за столом {table_number} не найдено"
        if select == "status":
            status = form.cleaned_data["order_status_field"]
            orders = Order.objects.filter(status=status)
            if orders:
                found = orders
            else:
                message = "Заказов с таким статусом не найдено"

        context = self.get_context_data(
            found=found,
            message=message,
        )
        return self.render_to_response(context)


