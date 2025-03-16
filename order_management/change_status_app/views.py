from django.shortcuts import redirect
from common.models import Order
from django.views.generic import ListView, DetailView
from . import forms
from common.services.form_services import save_modelform_with_prefix, creating_modelform_with_prefix
from common.services.order_services import get_order


class ChangeOrderStatusViews(ListView):
    """Изменение статусов заказов"""
    model = Order
    template_name = "change_status_app/change_status.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["orders"] = [
        #     {
        #         "order": order,
        #         "status_form": forms.StatusOrderForm(
        #             prefix=str(order.id), instance=order
        #         ),
        #     }
        #     for order in context["orders"]
        # ]
        context["orders"] = [
            {
                "order": order,
                "status_form": creating_modelform_with_prefix(
                    forms.StatusOrderForm, order
                ),
            }
            for order in context["orders"]
        ]
        return context

    def post(self, request, *args, **kwargs):
        for order in self.get_queryset():
            # form = forms.StatusOrderForm(
            #     request.POST, prefix=str(order.id), instance=order
            # )
            # if form.is_valid():
            #     form.save()
            save_modelform_with_prefix(request, forms.StatusOrderForm, order)
        return redirect("change_status")


class ChangeOneOrderStatusViews(DetailView):
    """Изменение статуса одного заказа"""
    template_name = "change_status_app/one_order.html"
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = context["order"]
        # context["status_form"] = forms.StatusOrderForm(
        #     prefix=str(order.id), instance=order
        # )
        context["status_form"] = creating_modelform_with_prefix(forms.StatusOrderForm, order)
        return context

    def post(self, request, *args, **kwargs):
        # order = Order.objects.get(pk=kwargs["pk"])
        order = get_order(pk=kwargs["pk"])
        # form = forms.StatusOrderForm(request.POST, prefix=str(order.id), instance=order)
        # if form.is_valid():
        #     form.save()
        save_modelform_with_prefix(request, forms.StatusOrderForm, order)
        return redirect("change_status")
