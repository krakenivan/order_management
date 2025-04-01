from django.test import TestCase
from django.urls import reverse

from common.models import Table, Order

from .forms import UpdateTableForms, CreateTableForms


class TableViewsTest(TestCase):
    def test_table_get(self):
        """тест get запроса"""
        response = self.client.get(reverse("table"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table_app/table.html")
        self.assertIn("tables", response.context)


class EditTableViewsTest(TestCase):
    def setUp(self):
        self.table_free = Table.objects.create(number=1, places=2, status="free")
        self.table_busy = Table.objects.create(number=2, places=2, status="busy")
        self.order_busy_table = Order.objects.create(
            table_number=self.table_busy, status=Order.Status.EXPECTATION
        )

    def test_edit_table_get_busy_table(self):
        """тест get запроса с занятым столом"""
        url = f"/edit-table/{self.table_busy.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table_app/table_locked.html")
        self.assertIn("orders", response.context)
        self.assertIn("is_table", response.context)

    def test_edit_table_get_free_table(self):
        """тест get запроса со свободным столом"""
        url = f"/edit-table/{self.table_free.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table_app/edit_table.html")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], UpdateTableForms)
        self.assertIn("orders", response.context)
        self.assertIn("is_table", response.context)

    def test_edit_table_post_valid(self):
        """тест post запроса с валидными данными и проверка изменения стола"""
        url = f"/edit-table/{self.table_free.id}"
        data = {"number": 3, "places": 4, "status": "busy"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("table"))
        table = Table.objects.get(pk=self.table_free.id)
        self.assertEqual(table.number, 3)
        self.assertEqual(table.places, 4)
        self.assertEqual(table.status, "busy")

    def test_edit_table_post_invalid(self):
        """тест post запроса с не валидными данными"""
        url = f"/edit-table/{self.table_free.id}"
        data = {"number": "", "places": "", "status": ""}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("warning_message", response.context)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)


class AddTableViewsTest(TestCase):
    def setUp(self):
        self.url = reverse("add_table")

    def test_add_table_get(self):
        """тест get запроса"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table_app/add_table.html")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], CreateTableForms)

    def test_add_table_post_valid(self):
        """тест post запроса с валидными данными"""
        data = {"number": 3, "places": 4}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("table"))
        table = Table.objects.get(pk=1)
        self.assertEqual(table.number, 3)
        self.assertEqual(table.places, 4)

    def test_add_table_post_invalid(self):
        """тест post запроса с не валидными данными"""
        data = {"number": "", "places": ""}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("warning_message", response.context)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)


class DeleteTableViewsTest(TestCase):
    def setUp(self):
        self.table_1 = Table.objects.create(number=1, places=2, status="free")
        self.table_busy = Table.objects.create(number=2, places=2, status="busy")
        self.order_busy_table = Order.objects.create(
            table_number=self.table_busy, status=Order.Status.EXPECTATION
        )

    def test_delete_table_get_free_table(self):
        """тест get запроса со свободным столом"""
        url = f"/delete-table/{self.table_1.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("table", response.context)
        self.assertTemplateUsed(response, "table_app/delete_table.html")

    def test_delete_table_get_busy_table(self):
        """тест get запроса с занятым столом"""
        url = f"/delete-table/{self.table_busy.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table_app/table_locked.html")
        self.assertIn("orders", response.context)
        self.assertIn("is_table", response.context)

    def test_delete_table_post_valid(self):
        """тест post запроса с валидными данными (существующий стол)"""
        url = f"/delete-table/{self.table_1.id}"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("table"))
        tables = Table.objects.all()
        self.assertEqual(len(tables), 1)

    def test_delete_table_post_invalid(self):
        """тест post запроса с не валидными данными (не существующий стол)"""
        url = f"/delete-table/3"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")


class UpdateTableFormsTest(TestCase):

    def setUp(self):
        self.table_1 = Table.objects.create(number=1, places=2, status="free")

    def test_form_fields(self):
        """тест формирования fields"""
        form = UpdateTableForms()
        form_fields = form.fields
        self.assertTrue("number" in form_fields)
        self.assertTrue("places" in form_fields)
        self.assertTrue("status" in form_fields)

    def test_form_label(self):
        """тест формирование label"""
        form = UpdateTableForms()
        self.assertTrue(form.fields["number"].label == "Номер стола:")
        self.assertTrue(form.fields["places"].label == "Количество мест:")
        self.assertTrue(form.fields["status"].label == "Статус")

    def test_form_valid(self):
        """тест с валидными данными и проверка изменения стола"""
        data = {"number": 3, "places": 4, "status": "busy"}
        form = UpdateTableForms(data=data, instance=self.table_1)
        self.assertTrue(form.is_valid())
        form.save()
        table = Table.objects.get(pk=self.table_1.id)
        self.assertEqual(table.number, 3)
        self.assertEqual(table.places, 4)
        self.assertEqual(table.status, "busy")

    def test_form_invalid(self):
        """тест с не валидными данными"""
        data = {"number": "", "places": "", "status": ""}
        form = UpdateTableForms(data=data, instance=self.table_1)
        self.assertFalse(form.is_valid())
        self.assertIn("number", form.errors)
        self.assertIn("places", form.errors)
        self.assertIn("status", form.errors)
        table = Table.objects.get(pk=self.table_1.id)
        self.assertEqual(table.number, 1)
        self.assertEqual(table.places, 2)
        self.assertEqual(table.status, "free")


class CreateTableFormsTest(TestCase):

    def test_form_fields(self):
        """тест формирования fields"""
        form = CreateTableForms()
        form_fields = form.fields
        self.assertTrue("number" in form_fields)
        self.assertTrue("places" in form_fields)

    def test_form_label(self):
        """тест формирование label"""
        form = CreateTableForms()
        self.assertTrue(form.fields["number"].label == "Номер стола:")
        self.assertTrue(form.fields["places"].label == "Количество мест:")

    def test_form_valid(self):
        """тест с валидными данными и проверка добавления стола"""
        data = {"number": 3, "places": 4}
        form = CreateTableForms(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        table = Table.objects.get(pk=1)
        self.assertEqual(table.number, 3)
        self.assertEqual(table.places, 4)

    def test_form_invalid(self):
        """тест с невалидными данными"""
        data = {"number": "", "places": ""}
        form = CreateTableForms(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("number", form.errors)
        self.assertIn("places", form.errors)
        tables = Table.objects.all()
        self.assertFalse(tables)
