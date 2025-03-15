from django import forms
from django.db.models import F
from common.models import Table

class UpdateTableForms(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'places', 'status']
        labels = {'number':"Номер стола:", 'places':"Количество мест:", 'status':"Статус"}

class CreateTableForms(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'places']
        labels = {'number':"Номер стола:", 'places':"Количество мест:"}