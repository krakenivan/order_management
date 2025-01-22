from django.http import HttpResponse
from django.shortcuts import render
from common.models import Order, Dishes, Product

# Create your views here.
def edit_order(request) -> HttpResponse:
    """Изменение заказа"""
    edit_id = None
    if request.method == "POST":
        # Получаем данные из формы
        data = request.POST.dict()
        data_item = {
            key: val
            for key, val in data.items()
            if key not in ["csrfmiddlewaretoken", "table_number", "id"] and val
        }
        order: Order = Order.objects.get(id=data['id'])
        edit_id = int(order.id)  # id изменяемого заказа
        if order.table_number != data['table_number']:  # при изменение стола
            order.table_number = data["table_number"]
            order.save(update_fields=["table_number"])
        order.items.exclude(name__in=data_item).delete()  # удаление блюд при изменение
        items = order.items.all()
        for dish in items:  # изменение цены блюда
            if items.get(name=dish.name).price != data[dish.name]:
                dish.price = data[dish.name]
                dish.save(update_fields=["price"])
        for item in data_item.keys():  # добавление блюда в заказ
            if item not in items.values_list("name", flat=True):
                Dishes.objects.create(name=item, price=data[item], order_id=order)
        order.fill()
    orders = Order.objects.exclude(status="paid")
    list_table: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # список столов
    # формирование списка словарей с нужными данными по заказу
    orders_data: list[dict] = []
    for order in orders:
        dishes = Dishes.objects.filter(order=order)  # блюда в заказе
        ordered_names = dishes.values_list("name", flat=True)
        remaining_products = Product.objects.exclude(name__in=ordered_names)  # блюда вне заказа
        orders_data.append(
            {"order": order, "dishes": dishes, "remaining_products": remaining_products}
        )
    return render(
        request,
        "edit_order_app/edit_order.html",
        context={"orders_data": orders_data, "list_table": list_table, "edit_id":edit_id},
    )


def edit_one_order(request, order_id) -> HttpResponse:
    """Изменение одного переданного заказа

    :param order_id: id переданного заказа
    :return: HttpResponse
    """
    edit_id = None
    order: Order = Order.objects.get(id=order_id)
    list_table: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    dishes = Dishes.objects.filter(order=order)
    ordered_names = dishes.values_list("name", flat=True)
    remaining_products = Product.objects.exclude(name__in=ordered_names)
    dishes_data = {"dishes": dishes, "remaining_products": remaining_products}
    if request.method == "POST":
        # Получаем данные из формы
        data = request.POST.dict()
        data_item = {
            key: val
            for key, val in data.items()
            if key not in ["csrfmiddlewaretoken", "table_number", "id"] and val
        }
        edit_id = int(order.id)
        if order.table_number != data["table_number"]:
            order.table_number = data["table_number"]
            order.save(update_fields=["table_number"])
        order.items.exclude(name__in=data_item).delete()
        items = order.items.all()
        for dish in items:
            if items.get(name=dish.name).price != data[dish.name]:
                dish.price = data[dish.name]
                dish.save(update_fields=["price"])
        for item in data_item.keys():
            if item not in items.values_list("name", flat=True):
                Dishes.objects.create(name=item, price=data[item], order_id=order)
        order.fill()
    return render(
        request,
        "edit_order_app/one_order.html",
        context={
            "dishes_data": dishes_data,
            "list_table": list_table,
            "edit_id": edit_id,
            "order": order,
        },
    )
