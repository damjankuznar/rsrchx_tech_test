from django.db import models

from backend import value_objects


class Food(models.Model):
    title = models.CharField(max_length=64, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=18)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    statuses = [(status.name, status.value) for status in value_objects.CartStatus]
    statuses_max_length = max(len(status.name) for status in value_objects.CartStatus)

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(
        choices=statuses, default=value_objects.CartStatus.OPEN.name, max_length=statuses_max_length
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(null=False, default=1, decimal_places=2, max_digits=18)
