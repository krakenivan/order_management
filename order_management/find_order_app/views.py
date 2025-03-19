from django.views.generic import FormView

from common.services.form_services import get_object_form
from common.services.order_services import filter_order

from . import forms


class FindOrderViews(FormView):
    """Поиск заказов"""

    form_class = forms.FindOrderForm
    template_name = "find_order_app/find_order.html"

    def form_valid(self, form):
        message = "Найденные заказы"
        found = None
        select = get_object_form(form, "select")
        # поиск по id
        if select == "id":
            id = get_object_form(form, "order_id_field")
            orders = filter_order(id=id)
            if orders:
                found = orders
            else:
                message = f"Заказа с номером:{id} не найдено"
        # поиск по номеру стола
        if select == "table_number":
            table_number = get_object_form(form, "order_table_number_field")
            orders = filter_order(table_number=table_number)
            if orders:
                found = orders
            else:
                message = f"Заказов за столом {table_number} не найдено"
        # поиск по статусу
        if select == "status":
            status = get_object_form(form, "order_status_field")
            orders = filter_order(status=status)
            if orders:
                found = orders
            else:
                message = "Заказов с таким статусом не найдено"

        context = self.get_context_data(
            found=found,
            message=message,
        )
        return self.render_to_response(context)
