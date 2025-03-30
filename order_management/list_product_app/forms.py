import logging
from django import forms
from common.models import Product

from common.services.product_services import all_product

logger = logging.getLogger("warning_app")


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        labels = {
            "name": "Название блюда",
            "ingredients": "Ингредиенты блюда",
            "price": "Цена блюда",
        }


class DeleteProductForm(forms.Form):
    select_product = forms.ModelMultipleChoiceField(
        queryset=all_product(),
        widget=forms.CheckboxSelectMultiple(),
        label="Выберите блюдо:",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настраиваем отображение label для каждого выбора
        self.fields["select_product"].label_from_instance = (
            lambda obj: f"Блюдо: {obj.name}. Цена: {obj.price}"
        )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            error_message = "Нужно выбрать блюда для удаления."
            logger.error(error_message)
            raise forms.ValidationError(error_message)
        return cleaned_data
