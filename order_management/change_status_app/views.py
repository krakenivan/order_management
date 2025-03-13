from django.shortcuts import redirect
from common.models import Order
from django.views.generic import ListView, DetailView
from . import forms


class ChangeOrderStatusViews(ListView):
    model = Order
    template_name = "change_status_app/change_status.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = [
            {
                "order": order,
                "status_form": forms.StatusOrderForm(
                    prefix=str(order.id), instance=order
                ),
            }
            for order in context["orders"]
        ]
        return context

    def post(self, request, *args, **kwargs):
        for order in self.get_queryset():
            form = forms.StatusOrderForm(
                request.POST, prefix=str(order.id), instance=order
            )
            if form.is_valid():
                form.save()
        return redirect("change_status")


class ChangeOneOrderStatusViews(DetailView):
    template_name = "change_status_app/one_order.html"
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = context["order"]
        context["status_form"] = forms.StatusOrderForm(
            prefix=str(order.id), instance=order
        )
        return context

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs["pk"])
        form = forms.StatusOrderForm(request.POST, prefix=str(order.id), instance=order)
        if form.is_valid():
            form.save()
        return redirect("change_status")
