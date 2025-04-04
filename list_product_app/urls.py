from django.urls import path
from . import views

urlpatterns = [
    path("product/", views.ProductViews.as_view(), name="product"),
    path("add-prod/", views.AddProductViews.as_view(), name="add_product"),
    path("del-prod/", views.DeleteProductViews.as_view(), name="delete_product"),
]
