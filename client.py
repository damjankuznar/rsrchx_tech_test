#!/usr/bin/env python

import argparse
import decimal
import json

import requests

BASE_URL = "http://127.0.0.1:8000"


class APIError(BaseException):
    pass


def _get_credentials():
    try:
        with open(".credentials") as f:
            data = json.load(f)
            return data["username"], data["password"]
    except FileNotFoundError:
        raise APIError("You need to login in first")


def _authenticated_backend_request(endpoint, method="POST", data=None):
    auth = _get_credentials()
    response = requests.request(method, f"{BASE_URL}{endpoint}", json=data, auth=auth)
    if response.status_code != 200:
        message = []
        for key, value in response.json().items():
            message.append(f"{key}: {value}")
        raise APIError("Error processing request:\n{}".format("\n".join(message)))
    return response.json()


def _backend_request(endpoint, method="GET", data=None):
    response = requests.request(method, f"{BASE_URL}{endpoint}", json=data)
    return response.json()


def _print_cart(cart):
    if cart["items"]:
        print("Your shopping cart:")
        for item in cart["items"]:
            print(f"{item['id']} {item['quantity']} {item['food']}")
    else:
        print("Your shopping cart is empty")


def food_list(args):
    data = _backend_request("/api/foods/")
    for food in data:
        print(f"{food['id']} {food['title']}")


def food_detail(args):
    data = _backend_request(f"/api/foods/{args.food_id}/")
    for key, value in data.items():
        print(f"{key}: {value}")


def cart_add(args):
    data = _authenticated_backend_request(
        "/api/cart/add/", method="POST", data={"food": args.food_id, "quantity": "{:.2f}".format(args.quantity)}
    )
    _print_cart(data)


def cart_remove(args):
    data = _authenticated_backend_request(f"/api/cart/{args.item_id}/", method="DELETE")
    _print_cart(data)


def cart_view(args):
    data = _authenticated_backend_request("/api/cart/", method="GET")
    _print_cart(data)


def cart_checkout(args):
    data = _authenticated_backend_request("/api/cart/checkout/")
    if data["status"] == "PENDING":
        print("Order submitted")


def orders_list(args):
    data = _authenticated_backend_request("/api/orders/", method="GET")
    print("Your orders")
    for order in data:
        print(f" - {order['id']} {order['updated_at']}")


def order_details(args):
    data = _authenticated_backend_request(f"/api/orders/{args.order_id}", method="GET")
    _print_order(data)


def _print_order(data):
    print("Orders details:")
    items = data["items"]
    del data["items"]
    for key, value in data.items():
        print(f" - {key}: {value}")
    print(" - items:")
    for item in items:
        print(f"    - {item['id']} {item['food']} {item['quantity']}")


def admin_orders_list(args):
    data = _authenticated_backend_request("/admin/api/orders/", method="GET")
    print("Pending customer orders")
    for order in data:
        print(f" - {order['id']} {order['updated_at']}")


def admin_orders_details(args):
    data = _authenticated_backend_request(f"/admin/api/orders/{args.order_id}", method="GET")
    _print_order(data)


def admin_orders_completed(args):
    data = _authenticated_backend_request(
        f"/admin/api/orders/{args.order_id}/", method="PUT", data={"status": "COMPLETED"}
    )
    _print_order(data)


def login(args):
    password = input("Enter password:")
    with open(".credentials", "w") as f:
        json.dump({"username": args.username, "password": password}, f)


def main():
    parser = argparse.ArgumentParser(description="Shopping interface")
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers()

    login_parser = subparsers.add_parser("login")
    login_parser.add_argument("username")
    login_parser.set_defaults(func=login)

    cart_parser = subparsers.add_parser("cart")
    cart_parser.set_defaults(func=lambda args: cart_parser.print_help())
    cart_subparsers = cart_parser.add_subparsers()
    cart_view_parser = cart_subparsers.add_parser("view")
    cart_view_parser.set_defaults(func=cart_view)
    cart_add_parser = cart_subparsers.add_parser("add")
    cart_add_parser.add_argument("food_id", type=int)
    cart_add_parser.add_argument("quantity", type=decimal.Decimal)
    cart_add_parser.set_defaults(func=cart_add)
    cart_remove_parser = cart_subparsers.add_parser("remove")
    cart_remove_parser.add_argument("item_id", type=int)
    cart_remove_parser.set_defaults(func=cart_remove)
    cart_checkout_parser = cart_subparsers.add_parser("checkout")
    cart_checkout_parser.set_defaults(func=cart_checkout)

    orders_parser = subparsers.add_parser("orders")
    orders_parser.set_defaults(func=lambda args: orders_parser.print_help())
    orders_subparsers = orders_parser.add_subparsers()
    orders_list_parser = orders_subparsers.add_parser("list")
    orders_list_parser.set_defaults(func=orders_list)
    orders_details_parser = orders_subparsers.add_parser("details")
    orders_details_parser.add_argument("order_id", type=int)
    orders_details_parser.set_defaults(func=order_details)

    food_parser = subparsers.add_parser("foods")
    food_parser.set_defaults(func=lambda args: food_parser.print_help())
    food_subparsers = food_parser.add_subparsers()
    food_list_parser = food_subparsers.add_parser("list")
    food_list_parser.set_defaults(func=food_list)
    food_detail_parser = food_subparsers.add_parser("detail")
    food_detail_parser.add_argument("food_id")
    food_detail_parser.set_defaults(func=food_detail)

    admin_parser = subparsers.add_parser("admin")
    admin_parser.set_defaults(func=lambda args: admin_parser.print_help())
    admin_subparsers = admin_parser.add_subparsers()
    admin_orders_parser = admin_subparsers.add_parser("orders")
    admin_orders_parser.set_defaults(func=lambda args: admin_orders_parser.print_help())
    admin_orders_subparsers = admin_orders_parser.add_subparsers()
    admin_orders_list_parser = admin_orders_subparsers.add_parser("list")
    admin_orders_list_parser.set_defaults(func=admin_orders_list)
    admin_orders_details_parser = admin_orders_subparsers.add_parser("details")
    admin_orders_details_parser.add_argument("order_id", type=int)
    admin_orders_details_parser.set_defaults(func=admin_orders_details)
    admin_orders_completed_parser = admin_orders_subparsers.add_parser("completed")
    admin_orders_completed_parser.add_argument("order_id", type=int)
    admin_orders_completed_parser.set_defaults(func=admin_orders_completed)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    try:
        main()
    except APIError as e:
        print(e)
