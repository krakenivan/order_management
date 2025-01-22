from django.shortcuts import render

# Create your views here.

def index(request):
    """главная страница"""
    return render(request, "home/index.html")
