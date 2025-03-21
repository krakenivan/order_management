from django.shortcuts import redirect
from django.urls import reverse


class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Логируем ошибку
        # logger.error(f"Произошла ошибка: {e}\n{traceback.format_exc()}")
        return redirect(reverse("error"))
