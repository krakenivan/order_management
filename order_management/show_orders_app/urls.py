from django.urls import path
from . import views

urlpatterns = [
    path("show-orders/", views.show_orders, name="show_orders"),
]
