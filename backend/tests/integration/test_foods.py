from rest_framework import reverse, test, response


def test_food_list(client: test.APIClient, user, foods):
    client.force_authenticate(user)
    res: response.Response = client.get(reverse.reverse("foods-list"))
    assert res.status_code == 200
    for index in range(len(foods)):
        assert res.data[index]["title"] == foods[index].title
