from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r"order", views.OrderViewSet)
router.register(r"table", views.TableViewSet)
router.register(r"dishes", views.DishesViewSet)
router.register(r"product", views.ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
