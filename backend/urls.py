from django import urls
from django.contrib import admin
from rest_framework import routers

from backend import views

router = routers.DefaultRouter()
router.register("foods", views.FoodViewSet, basename="foods")
router.register("orders", views.OrderViewSet, basename="orders")

admin_router = routers.DefaultRouter()
admin_router.register("orders", views.AdminOrderViewSet, basename="admin-orders")

urlpatterns = [
    urls.path("admin/api/", urls.include(admin_router.urls)),
    urls.path("api/", urls.include(router.urls)),
    urls.path("api/cart/", views.CartManagementViewSet.as_view({"get": "retrieve"}), name="cart-view"),
    urls.path("api/cart/add/", views.CartManagementViewSet.as_view({"post": "add_item"}), name="cart-add"),
    urls.path("api/cart/checkout/", views.CartManagementViewSet.as_view({"post": "checkout"}), name="cart-checkout"),
    urls.re_path(
        r"api/cart/(?P<id>\d+)/", views.CartManagementViewSet.as_view({"delete": "remove_item"}), name="cart-remove"
    ),
]
