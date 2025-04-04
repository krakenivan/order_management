import logging
from django import forms
from django.core.exceptions import ValidationError
from common.models import Order
from common.services.product_services import all_product
from common.services.form_services import is_selected_product

logger = logging.getLogger("warning_app")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table_number"]
        labels = {"table_number": "Номер стола"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        products = all_product()

        # Динамически создаем поля для каждого продукта
        for product in products:
            field_name = f"product_{product.id}"
            quantity_name = f"quantity_{product.id}"

            # Поле для выбора продукта (чекбокс)
            self.fields[field_name] = forms.BooleanField(
                required=False,
                label=product.name,
            )

            # Поле для ввода количества (числовое поле)
            self.fields[quantity_name] = forms.IntegerField(
                required=False,
                min_value=1,
                initial=1,
                label=f"Количество: {product.name}",
            )

    def clean(self):
        cleaned_data = super().clean()
        table_number = cleaned_data.get("table_number")

        if table_number and not is_selected_product(cleaned_data):
            error_message = "Если выбран стол, необходимо выбрать хотя бы один продукт."
            logger.error(error_message)  # Логируем ошибку
            raise ValidationError(error_message)

        return cleaned_data
