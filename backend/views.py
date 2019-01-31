from rest_framework import viewsets, permissions, response, parsers, exceptions, mixins

from backend import models, serializers, value_objects


class FoodViewSet(viewsets.ModelViewSet):
    queryset = models.Food.objects.all()
    serializer_class = serializers.FoodSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer


class CartManagementViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def _get_cart(self, user):
        try:
            cart = models.Cart.objects.get(user=user, status=value_objects.CartStatus.OPEN.name)
        except models.Cart.DoesNotExist:
            cart = models.Cart.objects.create(user=user, status=value_objects.CartStatus.OPEN.name)
        return cart

    def _serialize_cart(self, cart):
        serializer = serializers.CartSerializer(cart)
        return response.Response(serializer.data)

    def retrieve(self, request):
        cart = self._get_cart(request.user)
        return self._serialize_cart(cart)

    def add_item(self, request):
        item_serializer = serializers.ItemSerializer(data=request.data)
        if item_serializer.is_valid():
            cart = self._get_cart(request.user)
            food = item_serializer.validated_data["food"]
            quantity = item_serializer.validated_data["quantity"]
            models.CartItem.objects.create(cart=cart, food=food, quantity=quantity)
            cart.refresh_from_db()
            return self._serialize_cart(cart)
        else:
            return response.Response(item_serializer.errors, status=400)

    def remove_item(self, request, id):
        cart = self._get_cart(request.user)
        models.CartItem.objects.filter(cart=cart, id=id).delete()
        cart.refresh_from_db()
        return self._serialize_cart(cart)

    def checkout(self, request):
        cart = self._get_cart(request.user)
        cart.status = value_objects.CartStatus.PENDING.name
        cart.save(update_fields=["status"])
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
