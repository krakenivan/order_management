from django.db import models
from django.db.models import Sum

# Create your models here.


class Dishes(models.Model):
    """блюда в заказе"""

    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(null=True, blank=True)
    order_id = models.ForeignKey("Order", on_delete=models.PROTECT)

    def save(self, *args, **kwargs) -> None:
        self.total_price = self.product.price * self.quantity
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

    def calculation_total_price(self):
        """метод вычисления суммы заказа"""
        dishes = self.dishes_set.all()
        self.total_price = dishes.aggregate(Sum("total_price"))["total_price__sum"]
        self.save()

    # def add_dishes(self):
    #     """метод добавления списка заказа"""
    #     self.items.set(Dishes.objects.filter(order_id=self.id))

    # def fill(self):
    #     """метод для перерасчета заказа"""
    #     self.add_dishes()
    #     self.calculation()
    #     self.save()


class Product(models.Model):
    """Меню"""

    name = models.CharField(max_length=50)
    ingredients = models.TextField(null=True, blank=True)
    price = models.FloatField()


class Table(models.Model):
    """Столы"""

    class Status(models.TextChoices):
        """класс перечисляемого поля"""

        BUSY = "busy", "Занято"
        FREE = "free", "Свободно"

    number = models.PositiveSmallIntegerField()
    places = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.FREE)

    def __str__(self):
        return str(self.number)
