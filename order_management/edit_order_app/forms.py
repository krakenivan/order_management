from django import forms
from django.utils.safestring import mark_safe
from common.models import Order
from common.services.dishes_services import current_dishes_of_order, get_id_product_of_dish
from common.services.product_services import exclude_product


class CustomTextWidget(forms.TextInput):
    def __init__(self, custom_text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_text = custom_text  # Сохраняем переданный текст

    def render(self, name, value, attrs=None, renderer=None):
        # Рендерим стандартное поле ввода
        super().render(name, value, attrs, renderer)
        # Добавляем кастомный текст перед полем
        return mark_safe(f"<div class='info' >{self.custom_text}</div>")


class EditOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ["total_price"]
        labels = {"table_number": "Стол №", "status": "Статус заказа:"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "instance" not in kwargs:
            return
        order = kwargs["instance"]
        # dishes = order.dishes_set.all()
        dishes = current_dishes_of_order(order)
        # products = Product.objects.exclude(id__in=dishes.values("product_id"))
        products = exclude_product(id__in=dishes.values("product_id"))

        self.fields["dishes_in_order"] = forms.CharField(
            required=False,
            label="",
            widget=CustomTextWidget(custom_text="Блюда в заказе:"),
        )
        # формы для блюд в заказе
        for dish in dishes:
            # field_name = f"product_{dish.product.id}"
            field_name = f"product_{get_id_product_of_dish(dish)}"
            # quantity_name = f"quantity_{dish.product.id}"
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

        self.fields["dishes_not_in_order"] = forms.CharField(
            required=False,
            label="",
            widget=CustomTextWidget(custom_text="Добавить блюда:"),
        )
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
