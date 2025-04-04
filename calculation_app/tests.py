from datetime import datetime
from django.test import TestCase
from django.urls import reverse

from common.models import Table, Order

from .forms import DateFilterForm


class CalculationViewsTest(TestCase):

    def setUp(self):
        self.url = reverse("calculation")
        table = Table.objects.create(number=1, places=2, status=Table.Status.BUSY)
        order_1 = Order.objects.create(
            table_number=table, status=Order.Status.EXPECTATION
        )
        order_1.datetime = datetime(2025, 3, 20, 12, 0)
        order_1.save()
        order_2 = Order.objects.create(
            table_number=table, status=Order.Status.EXPECTATION
        )
        order_2.datetime = datetime(2025, 3, 22, 12, 0)
        order_2.save()
        order_3 = Order.objects.create(
            table_number=table, status=Order.Status.EXPECTATION
        )
        order_3.datetime = datetime(2025, 3, 23, 12, 0)
        order_3.save()

    def test_calculation_get_without_filters(self):
        """Тест запроса без фильтров"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], DateFilterForm)
        self.assertTemplateUsed(response, "calculation_app/calculation.html")
        self.assertEqual(response.context["name"], "Расчет за все время")
        self.assertTrue(response.context["filter"])

    def test_calculation_get_with_date_range(self):
        """Тест запроса с диапазоном дат"""
        data = {"start_date": ["2025-03-20"], "end_date": ["2025-03-24"]}
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculation_app/calculation.html")
        self.assertEqual(response.context["name"], "Расчет за указанный период")
        self.assertTrue(response.context["filter"])

    def test_calculation_get_with_single_date(self):
        """Тест запроса с одной датой"""
        data = {"start_date": ["2025-03-23"]}
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculation_app/calculation.html")
        self.assertEqual(response.context["name"], "Расчет за указанный период")
        self.assertTrue(response.context["filter"])

    def test_calculation_get_with_same_dates(self):
        """Тест запроса с одинаковыми датами"""
        data = {"start_date": ["2025-03-22"], "end_date": ["2025-03-22"]}
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculation_app/calculation.html")
        self.assertEqual(response.context["name"], "Расчет за указанный период")
        self.assertTrue(response.context["filter"])

    def test_no_orders_found(self):
        """Тест случая, когда нет заказов"""
        Order.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculation_app/calculation.html")
        self.assertFalse(response.context["filter"])


class DateFilterFormTest(TestCase):
    def test_form_fields(self):
        """проверка формирования fields"""
        data = {"start_date": ["2025-03-22"], "end_date": ["2025-03-22"]}
        form = DateFilterForm(data=data)
        form_fields = form.fields
        self.assertTrue("start_date" in form_fields)
        self.assertTrue("end_date" in form_fields)

    def test_form_label(self):
        """проверка формирование label"""
        data = {"start_date": ["2025-03-22"], "end_date": ["2025-03-22"]}
        form = DateFilterForm(data=data)
        self.assertTrue(form.fields["start_date"].label == "С")
        self.assertTrue(form.fields["end_date"].label == "По")
