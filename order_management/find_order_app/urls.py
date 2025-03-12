from django.urls import path
from . import views

urlpatterns = [
    path("find/", views.FindOrderViews.as_view(), name="find_order"),
]
