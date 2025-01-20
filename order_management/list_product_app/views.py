from django.shortcuts import render
from common.models import Product

# Create your views here.
def product(request):
    products = get_product()
    return render(request, "list_product_app/product.html", context={'products':products})

def add_product(request):
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

def delete_product(request):
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
    return Product.objects.all()
