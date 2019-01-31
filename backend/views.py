from rest_framework import viewsets, permissions, response, parsers, exceptions, mixins

from backend import models, serializers, value_objects, services


class FoodViewSet(viewsets.ModelViewSet):
    queryset = models.Food.objects.all()
    serializer_class = serializers.FoodSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer


class CartManagementViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def _serialize_cart(self, cart):
        serializer = serializers.CartSerializer(cart)
        return response.Response(serializer.data)

    def retrieve(self, request):
        cart = services.CartService.get_cart(request.user.id)
        return self._serialize_cart(cart)

    def add_item(self, request):
        item_serializer = serializers.ItemSerializer(data=request.data)
        if item_serializer.is_valid():
            food = item_serializer.validated_data["food"]
            quantity = item_serializer.validated_data["quantity"]
            cart = services.CartService.add_item(request.user.id, food.id, quantity)
            return self._serialize_cart(cart)
        else:
            return response.Response(item_serializer.errors, status=400)

    def remove_item(self, request, id):
        cart = services.CartService.remove_item(request.user.id, id)
        return self._serialize_cart(cart)

    def checkout(self, request):
        cart = services.CartService.checkout(request.user.id)
        return self._serialize_cart(cart)


class OrderViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Cart.objects.exclude(status=value_objects.CartStatus.OPEN.name).filter(user=user)


class AdminOrderViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.exclude(
        status__in=(value_objects.CartStatus.OPEN.name, value_objects.CartStatus.COMPLETED.name)
    )
