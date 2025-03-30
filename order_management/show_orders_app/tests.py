from django.test import TestCase
from django.urls import reverse


class ShowOrdersViewsTest(TestCase):
    def test_show_orders_get(self):
        """тест get запроса"""
        response = self.client.get(reverse("show_orders"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("orders", response.context)
        self.assertTemplateUsed(response, "show_orders_app/orders.html")


class NoOrdersViewsTest(TestCase):
    def test_no_orders_get(self):
        """тест get запроса"""
        response = self.client.get("/no-orders/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_orders_app/no_orders.html")

