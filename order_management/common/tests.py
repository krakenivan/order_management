from datetime import date
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from .models import Table, Order, Dishes, Product


class DishesModelsTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=1, places=2, status="busy")
        self.product = Product.objects.create(name="Test Product", price=100)
        self.order = Order.objects.create(
            table_number=self.table, status=Order.Status.EXPECTATION
        )

    def test_dishes_creation(self):
        """Тест создания объекта Dishes"""
        dish = Dishes.objects.create(
            product=self.product, quantity=2, order_id=self.order
        )
        self.assertEqual(dish.product, self.product)
        self.assertEqual(dish.quantity, 2)
        self.assertEqual(dish.order_id, self.order)
        self.assertEqual(dish.total_price, 200)

    def test_quantity_validation(self):
        """Тест валидации quantity"""
        with self.assertRaises(ValidationError):
            dish = Dishes(product=self.product, quantity=0, order_id=self.order)
            dish.full_clean()
        with self.assertRaises(ValidationError):
            dish = Dishes(product=self.product, quantity=-1, order_id=self.order)
            dish.full_clean()

    def test_foreign_key(self):
        """Тест связей с Product и Order"""
        dish = Dishes.objects.create(
            product=self.product, quantity=1, order_id=self.order
        )
        self.assertEqual(dish.product.pk, self.product.pk)
        self.assertEqual(dish.order_id.pk, self.order.pk)


class OrderModelsTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=1, places=2, status="busy")
        self.product_1 = Product.objects.create(name="Test Product", price=100)
        self.product_2 = Product.objects.create(name="Test Product", price=300)
        self.order = Order.objects.create(
            table_number=self.table, status=Order.Status.EXPECTATION
        )
        self.dish_1 = Dishes.objects.create(
            product=self.product_1, quantity=2, order_id=self.order
        )
        self.dish_2 = Dishes.objects.create(
            product=self.product_2, quantity=1, order_id=self.order
        )

    def test_order_creation(self):
        """Тест создания заказа"""
        self.assertEqual(self.order.table_number, self.table)
        self.assertEqual(self.order.status, Order.Status.EXPECTATION)
        self.assertIsNotNone(self.order.datetime)
        self.assertIsNone(self.order.total_price)

    def test_table_number_required(self):
        """Тест что table_number обязательное поле"""
        with self.assertRaises(IntegrityError):
            Order.objects.create(status=Order.Status.EXPECTATION)

    def test_datetime_auto_now_add(self):
        """Тест автоматического добавления даты/времени"""
        today = date.today()
        self.assertEqual(today, self.order.datetime.date())

    def test_calculation_total_price(self):
        """Тест расчета общей суммы заказа"""
        self.assertIsNone(self.order.total_price)
        self.order.calculation_total_price()
        order = Order.objects.get(pk=self.order.id)
        self.assertEqual(order.total_price, 500)

    def test_relation_with_dishes(self):
        """Тест связи с моделью Dishes"""
        dishes = self.order.dishes_set.all()
        self.assertEqual(dishes.count(), 2)
        self.assertIn(self.dish_1, dishes)
        self.assertIn(self.dish_2, dishes)


class ProductModelsTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product", ingredients="Test ingredients", price=100
        )

    def test_product_creation(self):
        """Тест создания продукта"""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.ingredients, "Test ingredients")
        self.assertEqual(self.product.price, 100)
        self.assertIsNotNone(self.product.id)

    def test_field_required(self):
        """Тест обязательных полей"""
        with self.assertRaises(ValidationError):
            product = Product.objects.create(price=10.0)
            product.full_clean()

        with self.assertRaises(IntegrityError):
            Product.objects.create(name="Test Product")

    def test_price_validation(self):
        """Тест валидации цены"""

        with self.assertRaises(ValidationError):
            product = Product(name="Test", price=-1.0)
            product.full_clean()

        with self.assertRaises(ValidationError):
            product = Product(name="Test", price=0.0)
            product.full_clean()

    def test_ingredients_optional(self):
        """Тест что ingredients необязательное поле"""
        product = Product.objects.create(name="Test Product 2", price=10.0)
        self.assertIsNone(product.ingredients)


class TableModelsTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=1, places=4)

    def test_table_creation(self):
        """Тест создания стола"""
        self.assertEqual(self.table.number, 1)
        self.assertEqual(self.table.places, 4)
        self.assertEqual(self.table.status, Table.Status.FREE)
        self.assertIsNotNone(self.table.id)

    def test_number_uniqueness(self):
        """Тест уникальности номера стола"""
        with self.assertRaises(IntegrityError):
            Table.objects.create(number=1, places=4)

    def test_number_positive(self):
        """Тест что номер стола должен быть положительным"""
        with self.assertRaises(ValidationError):
            table = Table(number=0, places=4)
            table.full_clean()

        with self.assertRaises(ValidationError):
            table = Table(number=-1, places=4)
            table.full_clean()

    def test_places_positive(self):
        """Тест что количество мест должно быть положительным"""
        with self.assertRaises(ValidationError):
            table = Table(number=3, places=0)
            table.full_clean()

        with self.assertRaises(ValidationError):
            table = Table(number=3, places=-1)
            table.full_clean()

    def test_places_max(self):
        with self.assertRaises(ValidationError):
            table = Table(number=3, places=21)
            table.full_clean()
