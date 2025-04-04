from django.urls import path
from . import views

urlpatterns = [
    path("table/", views.TableViews.as_view(), name="table"),
    path("edit-table/<pk>", views.EditTableViews.as_view(), name="edit_table"),
    path("add-table/", views.AddTableViews.as_view(), name="add_table"),
    path("delete-table/<pk>", views.DeleteTableViews.as_view(), name="delete_table"),
]
