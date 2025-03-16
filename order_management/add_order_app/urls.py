from django.urls import path
from . import views

urlpatterns = [
    path("order/", views.CreateOrderViews.as_view(), name="creating_order"),
    path(
        "completing_add_order/",
        views.CompletingAddOrderViews.as_view(),
        name="completing_add_order",
    ),
]
