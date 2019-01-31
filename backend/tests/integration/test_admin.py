from rest_framework import reverse, test, response

from backend import models, value_objects


def test_list_orders(client: test.APIClient, admin, pending_order):
    client.force_authenticate(admin)
    res: response.Response = client.get(reverse.reverse("admin-orders-list"))
    assert res.status_code == 200
    orders = res.json()
    assert len(orders) == 1
    assert orders[0]["status"] == value_objects.CartStatus.PENDING.name
    assert len(orders[0]["items"]) == 1


def test_orders_detail(client: test.APIClient, admin, pending_order):
    client.force_authenticate(admin)
    res: response.Response = client.get(reverse.reverse("admin-orders-detail", args=(1,)))
    assert res.status_code == 200
    order = res.json()
    assert order["status"] == value_objects.CartStatus.PENDING.name
    assert len(order["items"]) == 1


def test_update_order_status(client: test.APIClient, admin, pending_order):
    client.force_authenticate(admin)
    res: response.Response = client.put(
        reverse.reverse("admin-orders-detail", args=(1,)), dict(status=value_objects.CartStatus.COMPLETED.name)
    )
    assert res.status_code == 200
    order = res.json()
    assert order["status"] == value_objects.CartStatus.COMPLETED.name


def test_list_orders_non_admin(client: test.APIClient, user, pending_order):
    client.force_authenticate(user)
    res: response.Response = client.get(reverse.reverse("admin-orders-list"))
    assert res.status_code == 403


def test_orders_detail_non_admin(client: test.APIClient, user, pending_order):
    client.force_authenticate(user)
    res: response.Response = client.get(reverse.reverse("admin-orders-detail", args=(1,)))
    assert res.status_code == 403


def test_update_order_status_non_admin(client: test.APIClient, user, pending_order):
    client.force_authenticate(user)
    res: response.Response = client.put(
        reverse.reverse("admin-orders-detail", args=(1,)), dict(status=value_objects.CartStatus.COMPLETED.name)
    )
    assert res.status_code == 403
