from django.urls import path
from . import views

urlpatterns = [
    path("product/", views.product, name="product"),
    path("add-prod/", views.add_product, name="add_product"),
    path("del-prod/", views.delete_product, name="delete_product"),
]
