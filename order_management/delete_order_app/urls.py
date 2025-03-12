from django.urls import path
from . import views

urlpatterns = [
    path("delete/", views.ChoiceOfDeleteOrderViews.as_view(), name="choosing_delete"),
    path(
        "delete-order/<pk>",
        views.ConfirmationOfDeletionOrderViews.as_view(),
        name="delete_order",
    ),
]
