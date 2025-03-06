from django.db import models
from django.db.models import Sum

# Create your models here.


class Dishes(models.Model):
    """модель с блюдами"""

    name = models.CharField(max_length=40)
    price = models.FloatField()
    order_id = models.ForeignKey("Order", on_delete=models.PROTECT)


class Order(models.Model):
    """модель заказа"""

    class Status(models.TextChoices):
        """класс перечисляемого поля"""

        EXPECTATION = "expectation", "В ожидание"
        DONE = "done", "Готово"
        PAID = "paid", "Оплачено"

    table_number = models.PositiveSmallIntegerField()
    items = models.ManyToManyField(Dishes)
    total_price = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=11, choices=Status.choices, default=Status.EXPECTATION
    )

    def calculation(self):
        """метод вычисления суммы заказа"""
        dishes_table = Dishes.objects.filter(order_id=self.id)
        sum_table = dishes_table.aggregate(Sum("price"))
        self.total_price = sum_table["price__sum"]

    def add_dishes(self):
        """метод добавления списка заказа"""
        self.items.set(Dishes.objects.filter(order_id=self.id))

    def fill(self):
        """метод для перерасчета заказа"""
        self.add_dishes()
        self.calculation()
        self.save()


class Product(models.Model):
    """Меню"""

    name = models.CharField(max_length=50)
    ingredients = models.TextField(null=True, blank=True)
    price = models.FloatField()
