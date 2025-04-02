import logging
from django.db import models
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator

logger = logging.getLogger("info")


class Dishes(models.Model):
    """блюда в заказе"""

    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.PositiveIntegerField(null=True, blank=True)
    order_id = models.ForeignKey("Order", on_delete=models.CASCADE)

    def save(self, *args, **kwargs) -> None:
        self.total_price = self.product.price * self.quantity
        logger.info("Сумма вычислена!")
        return super().save(*args, **kwargs)


class Order(models.Model):
    """модель заказа"""

    class Status(models.TextChoices):
        """класс перечисляемого поля"""

        EXPECTATION = "expectation", "В ожидание"
        DONE = "done", "Готово"
        PAID = "paid", "Оплачено"
        COMPLETED = "completed", "Выполнен"

    table_number = models.ForeignKey("Table", on_delete=models.PROTECT)
    # items = models.ForeignKey("Dishes", on_delete=models.PROTECT)
    total_price = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=11, choices=Status.choices, default=Status.EXPECTATION
    )
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    def calculation_total_price(self):
        """метод вычисления суммы заказа"""
        dishes = self.dishes_set.all()
        self.total_price = dishes.aggregate(Sum("total_price"))["total_price__sum"]
        logger.info("Сумма за блюда в заказе вычислена!")
        self.save()


class Product(models.Model):
    """Меню"""

    name = models.CharField(max_length=50)
    ingredients = models.TextField(null=True, blank=True)
    price = models.FloatField(null=False, validators=[MinValueValidator(0.01)])


class Table(models.Model):
    """Столы"""

    class Status(models.TextChoices):
        """класс перечисляемого поля"""

        BUSY = "busy", "Занято"
        FREE = "free", "Свободно"

    number = models.PositiveSmallIntegerField(
        unique=True, validators=[MinValueValidator(1)]
    )
    places = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.FREE)

    def __str__(self):
        return str(self.number)
