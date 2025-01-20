from django.urls import path
from . import views

urlpatterns = [
    path("change-status/", views.change_status, name="change_status"),
    path("one-status/<int:order_id>", views.change_one_status, name="change_one_status"),
]
