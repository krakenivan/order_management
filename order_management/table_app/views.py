from common.models import Table
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from . import forms
from django.urls import reverse_lazy


class TableViews(ListView):
    template_name = "table_app/table.html"
    model = Table
    context_object_name = "tables"

class EditTableViews(UpdateView):
    model = Table
    form_class = forms.UpdateTableForms
    template_name = "table_app/edit_table.html"
    success_url = reverse_lazy("table")

class AddTableViews(CreateView):
    model = Table
    form_class = forms.CreateTableForms
    template_name = "table_app/add_table.html"
    success_url = reverse_lazy("table")

class DeleteTableViews(DeleteView):
    template_name = "table_app/delete_table.html"
    model = Table
    success_url = reverse_lazy("table")
