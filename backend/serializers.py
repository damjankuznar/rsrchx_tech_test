from rest_framework import serializers

from backend import models


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = "__all__"


class ItemSerializer(serializers.Serializer):
    food = serializers.PrimaryKeyRelatedField(queryset=models.Food.objects.all())
    quantity = serializers.DecimalField(decimal_places=2, max_digits=18)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        exclude = ("cart",)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = models.Cart
        fields = ("id", "status", "created_at", "updated_at", "items")
        read_only_fields = ("id", "created_at", "updated_at", "items")
        depth = 1

