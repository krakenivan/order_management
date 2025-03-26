import logging
from django import forms
from django.core.exceptions import ValidationError
from common.models import Order

logger = logging.getLogger("warning_app")


class StatusOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
        labels = {"status": "Статус заказа:"}

    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.pop("prefix", None)
        super().__init__(*args, **kwargs)

        # Проверка, что префикс соответствует ID существующего заказа
        if self.prefix:
            try:
                self.order = Order.objects.get(id=self.prefix)
            except Order.DoesNotExist:
                error_message = "Заказ с указанным ID не существует"
                logger.error(error_message)
                raise ValidationError(error_message)

    def clean(self):
        cleaned_data = super().clean()
        if not self.prefix:
            error_message = "Не указан префикс формы (ID заказа)"
            logger.error(error_message)
            raise ValidationError(error_message)
        return cleaned_data
