from django.forms import ValidationError
from django.test import TestCase
from django.urls import reverse

from common.models import Order, Table

from .forms import StatusOrderForm


class ChangeStatusViewsTest(TestCase):

    def setUp(self):
        self.url = reverse("change_status")
        self.table1 = Table.objects.create(number=1, places=2, status=Table.Status.BUSY)
        self.table2 = Table.objects.create(number=2, places=2, status=Table.Status.BUSY)
        self.order_1 = Order.objects.create(
            table_number=self.table1, status=Order.Status.EXPECTATION
        )
        self.order_2 = Order.objects.create(
            table_number=self.table2, status=Order.Status.EXPECTATION
        )

    def test_change_status_get(self):
        """проверка get запроса и формирования форм"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("orders", response.context)
        self.assertEqual(len(response.context["orders"]), 2)
        self.assertIn("order", response.context["orders"][0])
        order = response.context["orders"][0]["order"]
        order2 = response.context["orders"][1]["order"]
        self.assertIn("status_form", response.context["orders"][0])
        self.assertIsInstance(
            response.context["orders"][0]["status_form"], StatusOrderForm
        )
        self.assertEqual(response.context["orders"][0]["status_form"].instance, order)
        self.assertEqual(
            response.context["orders"][0]["status_form"].prefix, str(order.id)
        )
        self.assertEqual(response.context["orders"][1]["status_form"].instance, order2)
        self.assertEqual(
            response.context["orders"][1]["status_form"].prefix, str(order2.id)
        )
        self.assertTemplateUsed(response, "change_status_app/change_status.html")

    def test_change_status_post_form_valid(self):
        """проверка post запроса c валидными данными формы"""
        data = {
            f"{self.order_1.id}-status": ["done"],
            f"{self.order_2.id}-status": ["completed"],
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
        table1 = Table.objects.get(id=self.table1.id)
        table2 = Table.objects.get(id=self.table2.id)
        self.assertEqual(table1.status, "busy")
        self.assertEqual(table2.status, "free")

    def test_change_status_post_with_nonexistent_order(self):
        """Тест POST с несуществующим заказом"""
        response = self.client.post(
            self.url, data={"3-status": ["completed"]}
        )  # префикс = id несуществующего заказа
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
        table1 = Table.objects.get(id=self.table1.id)
        table2 = Table.objects.get(id=self.table2.id)
        self.assertEqual(table1.status, "busy")
        self.assertEqual(table2.status, "busy")

    def test_change_status_post_without_prefix(self):
        """Тест POST с данными без префикса"""
        response = self.client.post(
            self.url, data={"status": ["completed"]}
        )  # нет префикса
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
        table1 = Table.objects.get(id=self.table1.id)
        table2 = Table.objects.get(id=self.table2.id)
        self.assertEqual(table1.status, "busy")
        self.assertEqual(table2.status, "busy")


class ChangeOneStatusViewsTest(TestCase):

    def setUp(self):
        self.table = Table.objects.create(number=1, places=2, status=Table.Status.BUSY)
        self.order = Order.objects.create(
            table_number=self.table, status=Order.Status.EXPECTATION
        )
        self.url = f"/one-status/{self.order.id}"

    def test_change_one_status_get(self):
        """проверка get запроса и формирования форм"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("order", response.context)
        order = response.context["order"]
        self.assertIn("status_form", response.context)
        self.assertIsInstance(response.context["status_form"], StatusOrderForm)
        self.assertEqual(response.context["status_form"].instance, order)
        self.assertEqual(response.context["status_form"].prefix, str(order.id))
        self.assertTemplateUsed(response, "change_status_app/one_order.html")

    def test_change_one_status_no_order_get(self):
        """проверка get запроса с несуществующим заказом"""
        response = self.client.get("/one-status/3")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")

    def test_change_one_status_post_form_valid(self):
        """проверка post запроса c валидными данными формы"""
        data = {
            f"{self.order.id}-status": ["completed"],
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
        table = Table.objects.get(id=self.table.id)
        self.assertEqual(table.status, "free")

    def test_change_one_status_post_with_nonexistent_order(self):
        """Тест POST с несуществующим заказом"""
        response = self.client.post(
            self.url, data={"3-status": ["completed"]}
        )  # префикс = id несуществующего заказа
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
        table = Table.objects.get(id=self.table.id)
        self.assertEqual(table.status, "busy")

    def test_change_one_status_post_without_prefix(self):
        """Тест POST с данными без префикса"""
        response = self.client.post(
            self.url, data={"status": ["completed"]}
        )  # нет префикса
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
        table = Table.objects.get(id=self.table.id)
        self.assertEqual(table.status, "busy")


class StatusOrderFormTest(TestCase):
    def setUp(self):
        table = Table.objects.create(number=2, places=2, status=Table.Status.BUSY)
        self.order = Order.objects.create(
            table_number=table, status=Order.Status.EXPECTATION
        )

    def test_form_fields(self):
        """проверка формирования fields"""
        data = {f"{self.order.id}-status": "completed"}
        form = StatusOrderForm(data=data, prefix=str(self.order.id))
        form_fields = form.fields
        self.assertTrue("status" in form_fields)

    def test_form_label(self):
        """проверка формирование label"""
        data = {f"{self.order.id}-status": "completed"}
        form = StatusOrderForm(data=data, prefix=str(self.order.id))
        self.assertTrue(form.fields["status"].label == "Статус заказа:")

    def test_status_order_form_invalid_status_without_prefix(self):
        """Тест формы без префикса"""
        data = {"status": "completed"}  # Нет префикса с ID заказа
        form = StatusOrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertEqual(
            form.errors["__all__"][0], "Не указан префикс формы (ID заказа)"
        )

    def test_status_order_form_invalid_nonexistent_order_prefix(self):
        """Тест формы с префиксом несуществующего заказа"""
        data = {"3-status": "completed"}
        with self.assertRaises(ValidationError):
            StatusOrderForm(data=data, prefix="3")

    def test_status_order_form_valid(self):
        """Тест валидной формы"""
        data = {f"{self.order.id}-status": "completed"}
        form = StatusOrderForm(data=data, prefix=str(self.order.id))
        self.assertTrue(form.is_valid())

    def test_status_order_form_without_instance(self):
        """Тест создания формы без instance"""
        form_data = {f"{self.order.id}-status": "completed"}
        form = StatusOrderForm(data=form_data, prefix=str(self.order.id))

        self.assertTrue(form.is_valid())
        with self.assertRaises(Exception):
            form.save()  # Нельзя сохранить без instance

    def test_status_order_form_with_instance(self):
        """Тест создания формы с instance"""
        form = StatusOrderForm(instance=self.order, prefix=str(self.order.id))
        self.assertEqual(form.instance.id, self.order.id)
