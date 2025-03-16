from django.shortcuts import render
from django.urls import reverse_lazy
from common.models import Order, Dishes, Table
from django.views.generic import UpdateView, ListView
from . import forms
from django.core.exceptions import ObjectDoesNotExist


class ChoiceOfEditingOrderViews(ListView):
    model = Order
    template_name = "edit_order_app/choice_edit.html"
    context_object_name = "orders"


class EditOrderViews(UpdateView):
    model = Order
    form_class = forms.EditOrderForm
    template_name = "edit_order_app/edit_order.html"
    success_url = reverse_lazy("choice_edit")

    def get_object(self, queryset=None):
        # Сохраняем объект до изменений
        old_order = super().get_object(queryset)
        self.old_table = old_order.table_number
        return old_order

    def form_valid(self, form):
        order = form.instance
        new_table = form.cleaned_data.get("table_number")
        if new_table.status == "busy":
            ordering_at_the_table = new_table.order_set.exclude(status="completed")
            return render(
                self.request,
                "table_app/table_locked.html",
                context={"orders": ordering_at_the_table},
            )
        if self.old_table != new_table:
            self.old_table.status = Table.Status.FREE
            self.old_table.save()
            new_table.status = Table.Status.BUSY
            new_table.save()
        dishes = order.dishes_set.all()
        for field_name, value in form.cleaned_data.items():
            if field_name.startswith("product_"):
                product_id = int(field_name.split("_")[1])
                quantity_field = f"quantity_{product_id}"
                quantity = form.cleaned_data.get(quantity_field)
                try:
                    dish = dishes.get(product_id=product_id)
                except ObjectDoesNotExist:
                    dish = Dishes.objects.create(
                        product_id=product_id, quantity=quantity, order_id=order
                    )
                finally:
                    if value:
                        dish.quantity = quantity
                        dish.save()
                    else:
                        dish.delete()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Форма не прошла валидацию:", form.errors)
        return super().form_invalid(form)
