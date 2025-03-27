from django.test import TestCase
from django.urls import reverse

from common.models import Table, Order


class DeleteOrderViewsTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse("choosing_delete")
        self.table = Table.objects.create(number=1, places=2, status="busy")
        self.order = Order.objects.create(
            table_number=self.table, status=Order.Status.EXPECTATION
        )

    def test_choosing_delete_get(self):
        """проверка get запроса"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["orders"])
        self.assertTemplateUsed(response, "delete_order_app/choosing_delete.html")

    def test_choosing_delete_no_order_get(self):
        """проверка get запроса если нет заказов"""
        Order.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_orders_app/no_orders.html")


class ConfirmationOfDeletionOrderViewsTest(TestCase):

    def setUp(self) -> None:
        self.table = Table.objects.create(number=1, places=2, status="busy")
        self.order = Order.objects.create(
            table_number=self.table, status=Order.Status.EXPECTATION
        )
        self.url = f"/delete-order/{self.order.id}"

    def test_delete_order_get(self):
        """проверка get запроса"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.order)
        self.assertTemplateUsed(response, "delete_order_app/confirm_delete.html")

    def test_delete_order_no_order_get(self):
        """проверка get запроса для несуществующего стола"""
        url = "/delete-order/2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")

    def test_delete_order_post(self):
        """проверка post запроса подтверждения удаления и смены статуса стола"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("choosing_delete"))
        table = Table.objects.get(id=self.table.id)
        self.assertEqual(table.status, "free")

    def test_delete_order_no_order_post(self):
        """проверка ошибочного post запроса подтверждения удаления и неизменности статуса стола"""
        url = "/delete-order/2"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")
        table = Table.objects.get(id=self.table.id)
        self.assertEqual(table.status, "busy")
