from django.shortcuts import render


def error_views(request):
    """представление страницы ошибки 500"""
    return render(request, "error_500.html", status=500)


def error_404_views(request, exception):
    """представление страницы ошибки 404"""
    return render(request, "error_404.html", status=404)
