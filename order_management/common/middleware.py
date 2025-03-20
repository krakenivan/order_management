from django.shortcuts import redirect
from django.urls import reverse


class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # # Логируем ошибку
            # logger.error(f"Произошла ошибка: {e}\n{traceback.format_exc()}")

            # Перенаправляем на страницу ошибки
            return redirect(
                reverse("error")
            )
        return response
