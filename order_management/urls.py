"""
URL configuration for order_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from common.views import error_404_views

handler404 = error_404_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("", include("add_order_app.urls")),
    path("", include("delete_order_app.urls")),
    path("", include("find_order_app.urls")),
    path("", include("show_orders_app.urls")),
    path("", include("change_status_app.urls")),
    path("", include("calculation_app.urls")),
    path("", include("list_product_app.urls")),
    path("", include("edit_order_app.urls")),
    path("", include("table_app.urls")),
    path("", include("common.urls")),
    path("api/v1/", include("api.urls")),
]
