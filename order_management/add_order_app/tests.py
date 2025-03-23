from django.test import TestCase
from django.urls import reverse

from .forms import OrderForm


class TestAddOrder(TestCase):
    def test_creating_order_get(self):
        response = self.client.get(reverse("creating_order"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], OrderForm)

    def test_creating_order_post(self):
        data = {
            "table_number":'1',
            "product_1":'on',
            "quantity_1":'1'    
            }
        response = self.client.post(reverse("creating_order"),data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], OrderForm)

    def test_completing_add_order(self):
        response = self.client.get("/completing_add_order/")
        self.assertEqual(response.status_code, 200)
