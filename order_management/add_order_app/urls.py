from django.urls import path
from . import views

urlpatterns = [
    path("order/", views.creating_order, name="creating_order"),
    path('add-order/', views.add_order, name='add_order'),
]
