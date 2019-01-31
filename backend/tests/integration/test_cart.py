from rest_framework import reverse, test, response


def test_add_item(client: test.APIClient, user, foods):
    client.force_authenticate(user)
    res: response.Response = client.post(reverse.reverse("cart-add"), data=dict(food=1, quantity=1))
    assert res.status_code == 200
    cart = res.json()
    assert len(cart["items"]) == 1
    assert cart["items"][0]["food"] == 1


def test_add_item_invalid(client: test.APIClient, user, foods):
    client.force_authenticate(user)
    res: response.Response = client.post(reverse.reverse("cart-add"), data=dict(food=1, quantity="1kg"))
    assert res.status_code == 400
    errors = res.json()
    assert "quantity" in errors


def test_remove_item(client: test.APIClient, user, foods):
    client.force_authenticate(user)
    res: response.Response = client.post(reverse.reverse("cart-add"), data=dict(food=1, quantity=1))
    assert res.status_code == 200

    res: response.Response = client.delete(reverse.reverse("cart-remove", kwargs={"id": 1}))
    assert res.status_code == 200
    cart = res.json()
    assert len(cart["items"]) == 0


def test_view(client: test.APIClient, user):
    client.force_authenticate(user)
    res: response.Response = client.get(reverse.reverse("cart-view"))
    assert res.status_code == 200
    cart = res.json()
    assert len(cart["items"]) == 0
    assert cart["status"] == "OPEN"


def test_checkout(client: test.APIClient, user, foods):
    client.force_authenticate(user)
    res: response.Response = client.post(reverse.reverse("cart-add"), data=dict(food=1, quantity=1))
    assert res.status_code == 200

    res: response.Response = client.post(reverse.reverse("cart-checkout"))
    assert res.status_code == 200
    cart = res.json()
    assert len(cart["items"]) == 1
    assert cart["status"] == "PENDING"


def test_orders(client: test.APIClient, user, foods):
    client.force_authenticate(user)
    res: response.Response = client.post(reverse.reverse("cart-add"), data=dict(food=1, quantity=1))
    assert res.status_code == 200

    res: response.Response = client.post(reverse.reverse("cart-checkout"))
    assert res.status_code == 200

    res: response.Response = client.get(reverse.reverse("orders-list"))
    assert res.status_code == 200
    orders = res.json()
    assert len(orders) == 1
    assert orders[0]["status"] == "PENDING"

    res: response.Response = client.get(reverse.reverse("orders-detail", args=(1,)))
    assert res.status_code == 200
    orders = res.json()
    assert orders["status"] == "PENDING"
