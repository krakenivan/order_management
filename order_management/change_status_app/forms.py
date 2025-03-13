from django import forms
from common.models import Order


class StatusOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
        labels = {"status": "Статус заказа:"}
