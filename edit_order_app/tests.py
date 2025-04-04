from django.test import TestCase
from django.urls import reverse

from common.models import Order, Product, Table, Dishes

from .forms import EditOrderForm


class ChoiceOfEditingOrderViewsTest(TestCase):
    def test_choice_edit_get(self):
        """проверка get запроса"""
        table = Table.objects.create(number=1, places=2, status="busy")
        Order.objects.create(table_number=table, status=Order.Status.EXPECTATION)
        response = self.client.get("/edit/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["orders"])
        self.assertTemplateUsed(response, "edit_order_app/choice_edit.html")


class EditingOrderViewsTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=1, places=2, status="busy")
        self.table_free = Table.objects.create(number=2, places=2, status="free")
        self.table_busy = Table.objects.create(number=3, places=2, status="busy")
        self.product = Product.objects.create(name="Test Product", price=100)
        self.product_2 = Product.objects.create(name="Test Product 2", price=200)
        self.order = Order.objects.create(
            table_number=self.table, status=Order.Status.EXPECTATION
        )
        self.order_2 = Order.objects.create(
            table_number=self.table_busy, status=Order.Status.EXPECTATION
        )
        self.dish = Dishes.objects.create(
            product=self.product, quantity=1, order_id=self.order
        )
        self.url = f"/edit-order/{self.order.id}"

    def test_edit_order_get(self):
        """проверка get запроса"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], EditOrderForm)
        self.assertTrue(response.context["order"])
        self.assertTemplateUsed(response, "edit_order_app/edit_order.html")

    def test_edit_order_no_order_get(self):
        """проверка get запроса с несуществующим заказом"""
        response = self.client.get("/edit-order/3")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")

    def test_edit_order_post(self):
        """проверка post запроса"""
        data = {
            "table_number": self.table_free.id,
            "status": "done",
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 1,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/edit/")
        table = Table.objects.get(id=self.table_free.id)
        self.assertEqual(table.status, "busy")
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.status, "done")

    def test_edit_order_no_order_post(self):
        """проверка post запроса с несуществующим заказом"""
        response = self.client.post("/edit-order/3")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")

    def test_edit_order_table_locked(self):
        """проверка попытки изменить стол заказа на занятый"""
        data = {
            "table_number": self.table_busy.id,
            "status": "done",
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 1,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["orders"])
        self.assertTemplateUsed(response, "table_app/table_locked.html")

    def test_edit_order_post_dishes_updated(self):
        """проверка обновления/добавления блюд в заказе"""
        data = {
            "table_number": self.table.id,
            "status": "done",
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 2,
            f"product_{self.product_2.id}": "on",
            f"quantity_{self.product_2.id}": 1,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/edit/")
        dishes = Dishes.objects.filter(order_id=self.order)
        self.assertEqual(len(dishes), 2)
        self.assertEqual(dishes[0].quantity, 2)
        self.assertEqual(dishes[0].product, self.product)
        self.assertEqual(dishes[0].order_id, self.order)
        self.assertEqual(dishes[0].total_price, self.product.price * 2)
        self.assertEqual(dishes[1].quantity, 1)
        self.assertEqual(dishes[1].product, self.product_2)
        self.assertEqual(dishes[1].order_id, self.order)
        self.assertEqual(dishes[1].total_price, self.product_2.price * 1)

    def test_edit_order_post_total_price_recalculation(self):
        """проверка пересчета общей суммы"""
        initial_price = self.order.total_price

        data = {
            "table_number": self.table.id,
            "status": "done",
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 5,
            f"product_{self.product_2.id}": "on",
            f"quantity_{self.product_2.id}": 3,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/edit/")
        order = Order.objects.get(id=self.order.id)
        self.assertNotEqual(order.total_price, initial_price)
        self.assertEqual(
            order.total_price, 5 * self.product.price + 3 * self.product_2.price
        )

    def test_edit_order_post_invalid_form(self):
        """проверка post запроса с невалидными данными"""
        data = {
            "table_number": "",
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("warning_message", response.context)


class EditOrderFormTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=1, places=2, status="free")
        self.product = Product.objects.create(name="Test Product", price=100)
        self.order = Order.objects.create(
            table_number=self.table, status=Order.Status.EXPECTATION
        )

    def test_form_fields(self):
        """проверка формирования fields"""
        data = {
            "table_number": self.table.id,
            "status": "done",
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 1,
        }
        form = EditOrderForm(data=data, instance=self.order)
        form_fields = form.fields
        self.assertTrue("table_number" in form_fields)
        self.assertTrue("status" in form_fields)
        self.assertTrue("dishes_in_order" in form_fields)
        self.assertTrue("dishes_not_in_order" in form_fields)
        self.assertTrue(f"product_{self.product.id}" in form_fields)
        self.assertTrue(f"quantity_{self.product.id}" in form_fields)

    def test_form_label(self):
        """проверка формирование label"""
        data = {
            "table_number": self.table.id,
            "status": "done",
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 1,
        }
        form = EditOrderForm(data=data, instance=self.order)
        self.assertTrue(form.fields["table_number"].label == "Стол №")
        self.assertTrue(form.fields["status"].label == "Статус заказа:")
        self.assertTrue(form.fields["dishes_in_order"].label == "")
        self.assertTrue(form.fields["dishes_not_in_order"].label == "")
        self.assertTrue(
            form.fields[f"product_{self.product.id}"].label == self.product.name
        )
        self.assertTrue(
            form.fields[f"quantity_{self.product.id}"].label
            == f"Количество: {self.product.name}"
        )

    def test_form_valid(self):
        """проверка валидной формы"""
        data = {
            "table_number": self.table.id,
            "status": "done",
            f"product_{self.product.id}": "on",
            f"quantity_{self.product.id}": 1,
        }
        form = EditOrderForm(data=data, instance=self.order)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        """проверка не валидной формы"""
        data = {
            "table_number": "",
            "status": "done",
            f"product_{self.product.id}": "",
        }
        form = EditOrderForm(data=data, instance=self.order)
        self.assertFalse(form.is_valid())
        self.assertIn("table_number", form.errors)
        self.assertIn("__all__", form.errors)
