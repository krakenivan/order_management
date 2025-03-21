import logging
import traceback
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger("warning")


class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Логируем ошибку
        tb = traceback.extract_tb(exception.__traceback__)[-1]
        logger.error(f"{tb.filename} - {tb.name} - {exception}")
        return redirect(reverse("error"))
