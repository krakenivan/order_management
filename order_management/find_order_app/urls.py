from django.urls import path
from . import views

urlpatterns = [
    path("find/", views.find_order, name="find_order"),
]
