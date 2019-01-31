from backend import value_objects, models


class CartService:
    @classmethod
    def get_cart(cls, user_id):
        try:
            cart = models.Cart.objects.get(user_id=user_id, status=value_objects.CartStatus.OPEN.name)
        except models.Cart.DoesNotExist:
            cart = models.Cart.objects.create(user_id=user_id, status=value_objects.CartStatus.OPEN.name)
        return cart

    @classmethod
    def add_item(cls, user_id, food_id, quantity):
        cart = cls.get_cart(user_id)
        models.CartItem.objects.create(cart=cart, food_id=food_id, quantity=quantity)
        cart.refresh_from_db()
        return cart

    @classmethod
    def remove_item(cls, user_id, item_id):
        cart = cls.get_cart(user_id)
        models.CartItem.objects.filter(cart=cart, id=item_id).delete()
        cart.refresh_from_db()
        return cart

    @classmethod
    def checkout(cls, user_id):
        cart = cls.get_cart(user_id)
        cart.status = value_objects.CartStatus.PENDING.name
        cart.save(update_fields=["status"])
        return cart
