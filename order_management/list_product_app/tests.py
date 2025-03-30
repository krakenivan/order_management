from django.test import TestCase
from django.urls import reverse

from common.models import Product

from .forms import AddProductForm, DeleteProductForm


class ProductViewsTest(TestCase):
    def test_product_get(self):
        """проверка get запроса"""
        response = self.client.get(reverse("product"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_product_app/product.html")
        self.assertIn("products", response.context)


class AddProductViewsTest(TestCase):

    def setUp(self):
        self.url = reverse("add_product")

    def test_add_product_get(self):
        """проверка get запроса"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_product_app/add_product.html")
        self.assertIn("products", response.context)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], AddProductForm)

    def test_add_product_post(self):
        """проверка post запроса и добавление блюда"""
        data = {"name": "Test product", "ingredients": "Test ingredients", "price": 999}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
        new_product = Product.objects.all()[0]
        self.assertEqual(new_product.name, "Test product")
        self.assertEqual(new_product.ingredients, "Test ingredients")
        self.assertEqual(new_product.price, 999)

    def test_add_product_post_invalid(self):
        """проверка post с невалидными данными"""
        data = {"name": "", "ingredients": "", "price": -100}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")
        new_product = Product.objects.all()
        self.assertFalse(new_product)


class DeleteProductViewsTest(TestCase):
    def setUp(self):
        self.product_1 = Product.objects.create(name="Test Product", price=100)
        self.product_2 = Product.objects.create(name="Test Product 2", price=500)
        self.product_3 = Product.objects.create(name="Test Product 3", price=999)
        self.url = reverse("delete_product")

    def test_delete_product_get(self):
        """проверка get запроса"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_product_app/delete_product.html")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], DeleteProductForm)

    def test_delete_product_post(self):
        """проверка post запроса и удаления блюд"""
        data = {"select_product": ["2", "3"]}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)
        products = Product.objects.all()
        self.assertTrue(len(products), 1)
        del_product_2 = Product.objects.filter(pk=2)
        del_product_3 = Product.objects.filter(pk=3)
        self.assertFalse(del_product_2)
        self.assertFalse(del_product_3)

    def test_delete_product_post_invalid(self):
        """проверка post запроса с невалидными данными"""
        data = {"select_product": ["4"]}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("select_product", form.errors)
        data = {"select_product": [""]}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("select_product", form.errors)


class AddProductFormTest(TestCase):
    def test_form_fields(self):
        """проверка формирования fields"""
        form = AddProductForm()
        form_fields = form.fields
        self.assertTrue("name" in form_fields)
        self.assertTrue("ingredients" in form_fields)
        self.assertTrue("price" in form_fields)

    def test_form_label(self):
        """проверка формирование label"""
        form = AddProductForm()
        self.assertTrue(form.fields["name"].label == "Название блюда")
        self.assertTrue(form.fields["ingredients"].label == "Ингредиенты блюда")
        self.assertTrue(form.fields["price"].label == "Цена блюда")

    def test_form_valid(self):
        """проверка валидации формы"""
        data = {"name": "Test product", "ingredients": "Test ingredients", "price": 999}
        form = AddProductForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        """проверка валидации формы"""
        data = {"name": "", "ingredients": "", "price": ""}
        form = AddProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(form.errors["name"], ["This field is required."])
        self.assertIn("price", form.errors)
        self.assertEqual(form.errors["price"], ["This field is required."])
        self.assertNotIn("ingredients", form.errors)


class DeleteProductFormTest(TestCase):
    def setUp(self):
        self.product_1 = Product.objects.create(name="Test Product", price=100)
        self.product_2 = Product.objects.create(name="Test Product 2", price=500)
        self.product_3 = Product.objects.create(name="Test Product 3", price=999)

    def test_form_fields(self):
        """проверка формирования fields"""
        form = DeleteProductForm()
        form_fields = form.fields
        self.assertTrue("select_product" in form_fields)

    def test_form_label(self):
        """проверка формирование label"""
        form = DeleteProductForm()
        products = form.fields["select_product"].queryset

        for product in products:
            expected_label = f"Блюдо: {product.name}. Цена: {product.price}"
            actual_label = form.fields["select_product"].label_from_instance(product)
            self.assertEqual(expected_label, actual_label)

    def test_form_valid(self):
        """проверка валидной формы"""
        data = {"select_product": ["2", "3"]}
        form = DeleteProductForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        """проверка невалидной формы"""
        data = {"select_product": []}
        form = DeleteProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("select_product", form.errors)
        self.assertEqual(form.errors["select_product"], ["This field is required."])
        data = {"select_product": ["4"]}
        form = DeleteProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("select_product", form.errors)
        self.assertEqual(
            form.errors["select_product"],
            ["Select a valid choice. 4 is not one of the available choices."],
        )
