import logging
from django import forms

from common.models import Table

logger = logging.getLogger("warning_app")


class UpdateTableForms(forms.ModelForm):
    class Meta:
        model = Table
        fields = ["number", "places", "status"]
        labels = {
            "number": "Номер стола:",
            "places": "Количество мест:",
            "status": "Статус",
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data or (
            not cleaned_data["number"]
            or not cleaned_data["places"]
            or not cleaned_data["status"]
        ):
            error_message = (
                "Для изменения нужно указать номер, количество мест и статус стола"
            )
            logger.error(error_message)
            raise forms.ValidationError(error_message)

        return cleaned_data


class CreateTableForms(forms.ModelForm):
    class Meta:
        model = Table
        fields = ["number", "places"]
        labels = {"number": "Номер стола:", "places": "Количество мест:"}

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data or not cleaned_data["number"] or not cleaned_data["places"]:
            error_message = "Для добавления нужно указать номер и количество мест стола"
            logger.error(error_message)
            raise forms.ValidationError(error_message)

        return cleaned_data
