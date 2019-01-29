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
    urls.path("admin/", admin.site.urls),
    urls.path("api/", urls.include(router.urls)),
    urls.path('api/auth/', urls.include('rest_framework.urls', namespace='rest_framework')),
    urls.path("api/cart/", views.CartManagementViewSet.as_view({"get": "retrieve"})),
    urls.path("api/cart/add/", views.CartManagementViewSet.as_view({"post": "add_item"})),
    urls.path("api/cart/checkout/", views.CartManagementViewSet.as_view({"post": "checkout"})),
    urls.re_path(r"api/cart/(?P<id>\d+)/", views.CartManagementViewSet.as_view({"delete": "remove_item"})),
]
