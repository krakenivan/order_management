from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeViews.as_view(), name="index"),
]
