from django.urls import path
from .views import error_views

urlpatterns = [
    path('error/', error_views, name='error'),  # URL для страницы ошибки
]