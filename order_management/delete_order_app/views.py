from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from common.models import Order, Dishes
from django.views.generic import ListView, DetailView, DeleteView


class ChoiceOfDeleteOrderViews(ListView):
    model = Order
    template_name = "delete_order_app/choosing_delete.html"
    context_object_name = "orders"

class ConfirmationOfDeletionOrderViews(DeleteView):
    template_name = "delete_order_app/confirm_delete.html"
    model = Order
    success_url = reverse_lazy("show_orders")


