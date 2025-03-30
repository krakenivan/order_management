from django.test import TestCase
from django.urls import reverse


class HomeViewsTest(TestCase):
    def test_index_get(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertIn("orders", response.context)
        self.assertIn("tables", response.context)
