from django.urls import path
from . import views

urlpatterns = [
    path("order/", views.CreateOrderViews.as_view(), name="creating_order"),
    path("table_is_locked/", views.TableLockedViews.as_view(), name="table_is_locked"),
    path(
        "completing_add_order/",
        views.CompletingAddOrderViews.as_view(),
        name="completing_add_order",
    ),
]
