from django.test import TestCase
from django.urls import reverse

from common.models import Order, Product, Table
from .forms import FindOrderForm


class FindOrderViewsTest(TestCase):
    def setUp(self):
        self.url = reverse("find_order")
        self.table_1 = Table.objects.create(number=1, places=2, status="busy")
        self.table_2 = Table.objects.create(number=2, places=2, status="busy")
        self.product_1 = Product.objects.create(name="Test Product", price=100)
        self.product_2 = Product.objects.create(name="Test Product 2", price=200)
        self.order_1 = Order.objects.create(
            table_number=self.table_1, status=Order.Status.EXPECTATION
        )
        self.order_2 = Order.objects.create(
            table_number=self.table_2, status=Order.Status.PAID
        )

    def test_find_order_get(self):
        """проверка get запроса"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "find_order_app/find_order.html")
        self.assertIsInstance(response.context["form"], FindOrderForm)

    def test_find_order_post_id(self):
        """проверка успешного поиска по ID"""

        data = {"select": "id", "order_id_field": 1}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["found"][0], self.order_1)
        self.assertEqual(response.context["message"], "Найденные заказы")

    def test_find_order_post_not_id(self):
        """проверка поиска по несуществующему ID"""

        data = {"select": "id", "order_id_field": 3}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["found"], None)
        self.assertEqual(response.context["message"], "Заказа с номером:3 не найдено")

    def test_find_order_post_table(self):
        """проверка успешного поиска по номеру стола"""

        data = {"select": "table_number", "order_table_number_field": 1}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["found"][0], self.order_1)
        self.assertEqual(response.context["message"], "Найденные заказы")

    def test_find_order_post_not_table(self):
        """проверка поиска по несуществующему столу"""
        data = {"select": "table_number", "order_table_number_field": 3}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["found"], None)
        self.assertEqual(response.context["message"], "Заказов за столом 3 не найдено")

    def test_find_order_post_status(self):
        """проверка успешного поиска по статусу"""

        data = {"select": "status", "order_status_field": "paid"}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["found"][0], self.order_2)
        self.assertEqual(response.context["message"], "Найденные заказы")

    def test_find_order_post_not_status(self):
        """проверка поиска по несуществующему статусу"""

        data = {"select": "status", "order_status_field": "done"}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["found"], None)
        self.assertEqual(
            response.context["message"], "Заказов с таким статусом не найдено"
        )

    def test_find_order_post_invalid_form(self):
        """проверка невалидной формы"""
        data = {"select": "", "order_id_field": ""}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertFalse(response.context["form"].is_valid())


class FindOrderFormTest(TestCase):

    def test_form_fields(self):
        """проверка формирования fields"""
        form = FindOrderForm()
        self.assertIn("select", form.fields)
        self.assertIn("order_id_field", form.fields)
        self.assertIn("order_table_number_field", form.fields)
        self.assertIn("order_status_field", form.fields)

    def test_form_label(self):
        """проверка формирование label"""
        form = FindOrderForm()
        self.assertTrue(form.fields["select"].label == "Искать по:")
        self.assertTrue(form.fields["order_id_field"].label == "Введите номер заказа:")
        self.assertTrue(
            form.fields["order_table_number_field"].label == "Введите номер стола:"
        )
        self.assertTrue(
            form.fields["order_status_field"].label == "Выберите статус заказа:"
        )

    def test_form_validation(self):
        """проверка валидации формы"""
        # 1. Не выбран тип поиска
        form = FindOrderForm(data={"select": None})
        self.assertFalse(form.is_valid())
        self.assertIn("select", form.errors)

        # 2. Поиск по ID - валидный
        form = FindOrderForm(data={"select": "id", "order_id_field": 1})
        self.assertTrue(form.is_valid())

        # 3. Поиск по ID - невалидный
        form = FindOrderForm(data={"select": "id", "order_id_field": -1})
        self.assertFalse(form.is_valid())
        self.assertIn("order_id_field", form.errors)

        # 4. Поиск по номеру стола - валидный
        form = FindOrderForm(
            data={"select": "table_number", "order_table_number_field": 2}
        )
        self.assertTrue(form.is_valid())

        # 5. Поиск по статусу - валидный
        form = FindOrderForm(data={"select": "status", "order_status_field": "paid"})
        self.assertTrue(form.is_valid())

        # 6. Поиск по статусу - невалидный статус
        form = FindOrderForm(data={"select": "status", "order_status_field": "new"})
        self.assertFalse(form.is_valid())
        self.assertIn("order_status_field", form.errors)

    def test_unrequired_fields_not_shown(self):
        """проверка что поля, не соответствующие выбранному типу поиска, не требуются"""
        # При поиске по ID другие поля не требуются
        form = FindOrderForm(
            data={
                "select": "id",
                "order_id_field": 1,
                "order_table_number_field": "",
                "order_status_field": "",
            }
        )
        self.assertTrue(form.is_valid())

        # При поиске по столу другие поля не требуются
        form = FindOrderForm(
            data={
                "select": "table_number",
                "order_id_field": "",
                "order_table_number_field": 2,
                "order_status_field": "",
            }
        )
        self.assertTrue(form.is_valid())

        # При поиске по статусу другие поля не требуются
        form = FindOrderForm(
            data={
                "select": "status",
                "order_id_field": "",
                "order_table_number_field": "",
                "order_status_field": "paid",
            }
        )
        self.assertTrue(form.is_valid())
