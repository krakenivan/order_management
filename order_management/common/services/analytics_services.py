"""
Сервисы для аналитики
"""

import logging
from django.db.models import Sum

logger = logging.getLogger("info")


def analytics(orders, home=False):
    """аналитический расчет"""
    count_all: int = len(orders)  # всего заказов
    logger.info("Количество заказов вычислено.")
    calculat_all = orders.aggregate(Sum("total_price"))[
        "total_price__sum"
    ]  # общая сумма
    logger.info("Общая стоимость заказов вычислена.")
    calculat_paid = orders.filter(status="paid").aggregate(Sum("total_price"))[
        "total_price__sum"
    ]  # оплаченная сумма
    logger.info("Оплаченная сумма вычислена.")
    calculat_unpaid = orders.exclude(status__in=["paid", "completed"]).aggregate(
        Sum("total_price")
    )[
        "total_price__sum"
    ]  # неоплаченная сумма
    logger.info("Не оплаченная сумма вычислена.")
    more_to_be_paid = orders.filter(
        status__in=["expectation", "done"]
    ).count()  # количество неоплаченных заказов
    logger.info("Количество оплаченных заказов вычислено.")
    unpaid = orders.filter(
        status__in=["expectation", "done"]
    )  # список неоплаченных заказов
    logger.info("Неоплаченные заказы получены")
    count_unpaid: int = len(unpaid)  # количество неоплаченных
    data = {
        "count_all": count_all,
        "calculat_all": calculat_all,
        "calculat_paid": calculat_paid,
        "calculat_unpaid": calculat_unpaid,
        "more_to_be_paid": more_to_be_paid,
        "count_unpaid": count_unpaid,
    }
    if home:
        return data
    else:
        data["orders"] = unpaid
        return data
