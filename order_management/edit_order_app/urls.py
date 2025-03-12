from django.urls import path
from . import views

urlpatterns = [
    path("edit/", views.ChoiceOfEditingOrderViews.as_view(), name="choice_edit"),
    path("edit-order/<pk>", views.EditOrderViews.as_view(), name="edit_order"),
]
