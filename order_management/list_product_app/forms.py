from django import forms
from common.models import Product


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
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Выберите блюдо:",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настраиваем отображение label для каждого выбора
        self.fields["select_product"].label_from_instance = (
            lambda obj: f"Блюдо: {obj.name}. Цена: {obj.price}"
        )
