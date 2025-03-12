from django import forms


class FindOrderForm(forms.Form):
    select = forms.ChoiceField(
        label="Искать по:",
        initial=None,
        choices=(
            (None, "-----------"),
            ("id", "id заказа"),
            ("table_number", "Номер стола"),
            ("status", "Статус"),
        ),
        widget=forms.Select(attrs={"id": "select"}),
    )
    order_id_field = forms.IntegerField(
        initial=None,
        min_value=1,
        required=False,
        label="Введите номер заказа:",
        widget=forms.NumberInput(
            attrs={
                "id": "order-id-field",
                "style": "display:none;",
            }
        ),
    )
    order_table_number_field = forms.IntegerField(
        initial=None,
        min_value=1,
        required=False,
        label="Введите номер стола:",
        widget=forms.NumberInput(
            attrs={
                "id": "order-table-number-field",
                "style": "display:none;",
            }
        ),
    )
    order_status_field = forms.ChoiceField(
        initial=None,
        choices=[
            (None, ""),
            ("expectation", "В ожидание"),
            ("done", "Готово"),
            ("paid", "Оплачено"),
            ("completed", "Выполнен"),
        ],
        required=False,
        label="Выберите статус заказа:",
        widget=forms.Select(
            attrs={
                "id": "order-status-field",
                "style": "display:none;",
            }
        ),
    )
