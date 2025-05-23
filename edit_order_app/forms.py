import logging
from django import forms
from django.utils.safestring import mark_safe

from common.models import Order
from common.services.dishes_services import (
    current_dishes_of_order,
    get_id_product_of_dish,
)
from common.services.product_services import exclude_product
from common.services.form_services import is_selected_product

logger = logging.getLogger("info")
logger_app = logging.getLogger("warning_app")


class CustomTextWidget(forms.TextInput):
    """виджет для формы для отображения текста"""

    def __init__(self, custom_text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_text = custom_text  # Сохраняем переданный текст

    def render(self, name, value, attrs=None, renderer=None):
        super().render(name, value, attrs, renderer)
        # Добавляем кастомный текст перед полем
        return mark_safe(f"<div class='info' >{self.custom_text}</div>")


class EditOrderForm(forms.ModelForm):
    """Форма изменения заказа"""

    class Meta:
        model = Order
        exclude = ["total_price"]
        labels = {"table_number": "Стол №", "status": "Статус заказа:"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "instance" not in kwargs:
            return
        order = kwargs["instance"]
        dishes = current_dishes_of_order(order)
        products = exclude_product(id__in=dishes.values("product_id"))

        self.fields["dishes_in_order"] = forms.CharField(
            required=False,
            label="",
            widget=CustomTextWidget(custom_text="Блюда в заказе:"),
        )  # поле для отображения инфо текста
        # формы для блюд в заказе
        for dish in dishes:
            field_name = f"product_{get_id_product_of_dish(dish)}"
            quantity_name = f"quantity_{get_id_product_of_dish(dish)}"

            # Поле для выбора продукта (чекбокс)
            self.fields[field_name] = forms.BooleanField(
                required=False,
                initial=True,
                label=dish.product.name,
            )

            # Поле для ввода количества (числовое поле)
            self.fields[quantity_name] = forms.IntegerField(
                required=False,
                min_value=1,
                initial=dish.quantity,
                label=f"Количество: {dish.product.name}",
            )
        logger.info("Формы для блюд из заказа успешно сформированы.")
        self.fields["dishes_not_in_order"] = forms.CharField(
            required=False,
            label="",
            widget=CustomTextWidget(custom_text="Добавить блюда:"),
        )  # поле для отображения инфо текста
        # формы для блюд вне заказа
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
        logger.info("Формы для блюд вне заказа успешно сформированы.")

    def clean(self):
        cleaned_data = super().clean()
        if not is_selected_product(cleaned_data):
            error_message = "Необходимо выбрать хотя бы один продукт."
            logger_app.error(error_message)
            raise forms.ValidationError(error_message)

        return cleaned_data
