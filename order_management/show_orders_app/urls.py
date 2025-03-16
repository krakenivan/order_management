from django.urls import path
from . import views

urlpatterns = [
    path("show-orders/", views.ShowOrdersViews.as_view(), name="show_orders"),
    path("no-orders/", views.Ord.as_view()),
]
