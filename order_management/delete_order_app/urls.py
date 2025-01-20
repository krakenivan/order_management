from django.urls import path
from . import views

urlpatterns = [
    path("delete/", views.choosing_delete, name="choosing_delete"),
    path("delete_order/", views.delete, name="delete"),
]
