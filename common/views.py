import logging
from django.shortcuts import render

logger = logging.getLogger("info")


def error_views(request):
    """представление страницы ошибки 500"""
    logger.info("Перенаправление на страницу ошибки 500")
    return render(request, "error_500.html", status=500)


def error_404_views(request, exception):
    """представление страницы ошибки 404"""
    logger.info("Перенаправление на страницу ошибки 404")
    return render(request, "error_404.html", status=404)
