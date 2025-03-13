from django.urls import path
from . import views

urlpatterns = [
    path(
        "change-status/", views.ChangeOrderStatusViews.as_view(), name="change_status"
    ),
    path(
        "one-status/<pk>",
        views.ChangeOneOrderStatusViews.as_view(),
        name="change_one_status",
    ),
]
