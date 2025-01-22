from django.http import HttpResponse
from django.shortcuts import render
from common.models import Product

# Create your views here.
def product(request) -> HttpResponse:
    """Список меню"""
    products = get_product()
    return render(request, "list_product_app/product.html", context={'products':products})

def add_product(request) -> HttpResponse:
    """Добавление блюд в меню"""
    products = get_product()
    if request.method == "POST":
        # Получаем данные из формы
        data = request.POST.dict()
        Product.objects.create(name=data['name'], ingredients=data['ingredients'])
        return render(
            request, "list_product_app/add_product.html", context={"products": products, "addet":"+"}
        )
    return render(
        request, "list_product_app/add_product.html", context={"products": products}
    )

def delete_product(request) -> HttpResponse:
    """Удаление блюда из меню"""
    products = get_product()
    if request.method == "POST":
        # Получаем данные из формы
        data = request.POST.dict()
        Product.objects.filter(id=data['id']).delete()
        return render(
            request,
            "list_product_app/delete_product.html",
            context={"products": products, "deleted": "+"},
        )
    return render(
        request, "list_product_app/delete_product.html", context={"products": products}
    )


def get_product():
    """Функция запроса списка меню"""
    return Product.objects.all()
