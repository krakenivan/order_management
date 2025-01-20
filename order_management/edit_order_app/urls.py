from django.urls import path
from . import views

urlpatterns = [
    path("edit/", views.edit_order, name="edit_order"),
    path("one-edit/<int:order_id>", views.edit_one_order, name="edit_one_order"),
]
