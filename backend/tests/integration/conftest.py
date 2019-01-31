import pytest
from rest_framework.test import APIClient

from backend import models, value_objects


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    username = "user1"
    password = "bar"
    email = "user@email.com"
    user = django_user_model.objects.create_user(username=username, password=password, email=email)
    return user


@pytest.fixture
def admin(django_user_model):
    username = "admin1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password, is_staff=True)
    user.save()
    return user


@pytest.fixture
def foods(db):
    foods_list = [
        dict(title="Bananas", description="Pleasure the monkey in you", price=1),
        dict(title="Bread", description="Wheaty sensation for you", price="0.30"),
        dict(title="Yogurt", description="Creamy yogurt", price="10.01"),
        dict(title="Avocado", description="Make yourself a tasty guacamole", price="5.32"),
    ]
    foods = []
    for food_dict in foods_list:
        food = models.Food.objects.create(**food_dict)
        foods.append(food)
    return foods


@pytest.fixture
def non_empty_cart(user, foods):
    cart = models.Cart.objects.create(user=user, status=value_objects.CartStatus.OPEN.name)
    models.CartItem.objects.create(cart=cart, food=foods[0], quantity=1)
    return cart


@pytest.fixture
def pending_order(non_empty_cart):
    non_empty_cart.status = value_objects.CartStatus.PENDING.name
    non_empty_cart.save(update_fields=["status"])
    return non_empty_cart
