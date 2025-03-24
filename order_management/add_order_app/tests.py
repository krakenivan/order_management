from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from common.models import Order, Table, Product

from .forms import OrderForm


class AddOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("creating_order")
        self.success_url = reverse_lazy("completing_add_order")
        self.table = Table.objects.create(number=1, places=2, status="free")
        self.table_busy = Table.objects.create(number=2, places=2, status="busy")
        self.product = Product.objects.create(name="Test Product", price=100)
        self.order_busy_table = Order.objects.create(
            table_number=self.table_busy, status=Order.Status.EXPECTATION
        )

    def test_creating_order_get(self):
        """проверка get запроса и наличия формы"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], OrderForm)
        self.assertTemplateUsed(response, "add_order_app/creating.html")

    def test_creating_order_post_form_valid(self):
        """проверка post запроса с валидной формой"""
        data = {
            "table_number": self.table.id,
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 2,
        }
        response = self.client.post(self.url, data)
        order = Order.objects.all()[1]
        self.assertEqual(response.status_code, 302)
        expected_url = f"{self.success_url}?order_id={order.id}"
        self.assertEqual(response.url, expected_url)

    def test_creating_order_busy_table(self):
        """проверка случая когда стол занят"""
        data = {
            "table_number": self.table_busy.id,
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 2,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table_app/table_locked.html")

        self.assertIn("orders", response.context)

    def test_creating_order_post_form_invalid(self):
        """проверка post запроса с невалидной формой"""
        data = {
            "table_number": "",  # Некорректные данные
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 0,  # Некорректное количество
        }
        response = self.client.post(self.url, data)
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertIn("table_number", form.errors)

    def test_creating_order_post_form_not_product(self):
        """проверка post запроса с невалидной формой без блюд"""
        data = {
            "table_number": self.table.id,  # Некорректные данные, стол без блюд
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("warning_message", response.context)

    def test_completing_add_order(self):
        """проверка подтверждения добавления"""
        order = Order.objects.all()[0]
        data = {"order_id": order.id}
        response = self.client.get(self.success_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("orders", response.context)


class AddOrderFormTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=1, places=2, status="free")
        self.product = Product.objects.create(name="Test Product", price=100)
        self.product_2 = Product.objects.create(name="Test Product_2", price=200)

    def test_form_fields(self):
        """проверка формирования fields"""
        data = {
            "table_number": self.table.id,
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 2,
        }
        form = OrderForm(data=data)
        form_fields = form.fields
        self.assertTrue("table_number" in form_fields)
        self.assertTrue(f"product_{self.product.id}" in form_fields)
        self.assertTrue(f"quantity_{self.product.id}" in form_fields)

    def test_form_label(self):
        """проверка формирование label"""
        data = {
            "table_number": self.table.id,
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 2,
        }
        form = OrderForm(data=data)
        self.assertTrue(form.fields["table_number"].label == "Номер стола")
        self.assertTrue(
            form.fields[f"product_{self.product.id}"].label == self.product.name
        )
        self.assertTrue(
            form.fields[f"quantity_{self.product.id}"].label
            == f"Количество: {self.product.name}"
        )

    def test_form_valid(self):
        """проверка валидации формы"""
        data = {
            "table_number": self.table.id,
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 2,
        }
        form = OrderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_with_multiple_products(self):
        """проверка валидации формы с несколькими блюдами"""
        data = {
            "table_number": self.table.id,
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 2,
            f"product_{self.product_2.id}": "on",
            f"quantity_{self.product_2.id}": 3,
        }
        form = OrderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        """проверка невалидной формы"""
        data = {
            "table_number": "",
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": "0",
        }
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("table_number", form.errors)
        self.assertEqual(form.errors["table_number"], ["This field is required."])
        self.assertIn(f"quantity_{self.product.id}", form.errors)
        self.assertEqual(
            form.errors[f"quantity_{self.product.id}"],
            ["Ensure this value is greater than or equal to 1."],
        )

    def test_form_invalid_not_product(self):
        """проверка невалидной формы без продуктов"""
        data = {
            "table_number": self.table.id,
        }
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertEqual(
            form.errors["__all__"],
            ["Если выбран стол, необходимо выбрать хотя бы один продукт."],
        )
