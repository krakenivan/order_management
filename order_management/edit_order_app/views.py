from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView

from common.models import Order
from common.services.form_services import get_object_form
from common.services.model_services import save_objects
from common.services.dishes_services import (
    current_dishes_of_order,
    create_dishes,
    get_dish_by_product_id,
    check_product_id_in_dishes,
)












from common.services.table_services import (
    check_table_status,
    current_table_order,
    switch_table_status,
)

from . import forms


class ChoiceOfEditingOrderViews(ListView):
    """Выбор заказа для изменения"""

    model = Order
    template_name = "edit_order_app/choice_edit.html"
    context_object_name = "orders"


class EditOrderViews(UpdateView):
    """Изменение заказа"""

    model = Order
    form_class = forms.EditOrderForm
    template_name = "edit_order_app/edit_order.html"
    success_url = reverse_lazy("choice_edit")

    def get_object(self, queryset=None):
        # Сохраняем стол до изменений
        old_order = super().get_object(queryset)
        self.old_table = old_order.table_number
        return old_order

    def form_valid(self, form):
        order = form.instance
        new_table = get_object_form(form, key="table_number")
        if self.old_table != new_table:
            if check_table_status(new_table, "busy"):
                ordering_at_the_table = current_table_order(new_table)
                return render(
                    self.request,
                    "table_app/table_locked.html",
                    context={"orders": ordering_at_the_table},
                )
            switch_table_status(table=self.old_table, status="free")
            save_objects(self.old_table)
            switch_table_status(table=new_table, status="busy")
            save_objects(new_table)
        dishes = current_dishes_of_order(order)
        for field_name, value in form.cleaned_data.items():
            if field_name.startswith("product_"):
                product_id = int(field_name.split("_")[1])
                if value:
                    quantity_field = f"quantity_{product_id}"
                    quantity = get_object_form(form, quantity_field)
                    if check_product_id_in_dishes(dishes, product_id=product_id):
                        dish = get_dish_by_product_id(dishes, product_id=product_id)
                        dish.quantity = quantity
                        save_objects(dish)
                    else:
                        dish = create_dishes(
                            order_id=order, product_id=product_id, quantity=quantity
                        )
                else:
                    if product_id in dishes.values("product_id"):
                        dish = get_dish_by_product_id(dishes, product_id=product_id)
                        dish.delete()
                    else:
                        continue
        order.calculation_total_price()
        return super().form_valid(form)
