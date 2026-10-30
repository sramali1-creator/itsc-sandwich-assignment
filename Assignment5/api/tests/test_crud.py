def make_sandwich(client, name="BLT", price=6.5):
    r = client.post("/sandwiches/", json={"sandwich_name": name, "price": price})
    assert r.status_code == 201, r.text
    return r.json()


def make_resource(client, item="Bread", amount=100):
    r = client.post("/resources/", json={"item": item, "amount": amount})
    assert r.status_code == 201, r.text
    return r.json()


def make_order(client, name="John Doe"):
    r = client.post("/orders/", json={"customer_name": name, "description": "Test order"})
    assert r.status_code == 201, r.text
    return r.json()


# ---------- Sandwiches ----------
def test_sandwich_crud(client):
    s = make_sandwich(client)
    assert s["sandwich_name"] == "BLT"
    assert client.get("/sandwiches/").json()[0]["id"] == s["id"]
    assert client.get(f"/sandwiches/{s['id']}").json()["price"] == 6.5
    r = client.put(f"/sandwiches/{s['id']}", json={"price": 7.25})
    assert r.status_code == 200 and r.json()["price"] == 7.25 and r.json()["sandwich_name"] == "BLT"
    assert client.delete(f"/sandwiches/{s['id']}").status_code == 204
    assert client.get(f"/sandwiches/{s['id']}").status_code == 404


def test_sandwich_errors(client):
    make_sandwich(client)
    assert client.post("/sandwiches/", json={"sandwich_name": "BLT", "price": 5}).status_code == 400
    assert client.post("/sandwiches/", json={"sandwich_name": "X", "price": -1}).status_code == 422
    assert client.post("/sandwiches/", json={"price": 5}).status_code == 422
    assert client.put("/sandwiches/999", json={"price": 1}).status_code == 404
    assert client.delete("/sandwiches/999").status_code == 404


# ---------- Resources ----------
def test_resource_crud(client):
    r = make_resource(client)
    assert client.get("/resources/").json()[0]["item"] == "Bread"
    assert client.get(f"/resources/{r['id']}").json()["amount"] == 100
    u = client.put(f"/resources/{r['id']}", json={"amount": 50})
    assert u.status_code == 200 and u.json()["amount"] == 50
    assert client.delete(f"/resources/{r['id']}").status_code == 204
    assert client.get(f"/resources/{r['id']}").status_code == 404


def test_resource_errors(client):
    make_resource(client)
    assert client.post("/resources/", json={"item": "Bread", "amount": 1}).status_code == 400
    assert client.post("/resources/", json={"item": "Ham", "amount": -5}).status_code == 422
    assert client.get("/resources/999").status_code == 404
    assert client.put("/resources/999", json={"amount": 1}).status_code == 404
    assert client.delete("/resources/999").status_code == 404


# ---------- Recipes ----------
def test_recipe_crud(client):
    s = make_sandwich(client)
    res = make_resource(client)
    res2 = make_resource(client, "Lettuce", 20)
    r = client.post("/recipes/", json={"sandwich_id": s["id"], "resource_id": res["id"], "amount": 2})
    assert r.status_code == 201, r.text
    rid = r.json()["id"]
    assert r.json()["sandwich"]["sandwich_name"] == "BLT"
    assert r.json()["resource"]["item"] == "Bread"
    assert len(client.get("/recipes/").json()) == 1
    assert client.get(f"/recipes/{rid}").json()["amount"] == 2
    u = client.put(f"/recipes/{rid}", json={"resource_id": res2["id"], "amount": 1})
    assert u.status_code == 200 and u.json()["resource"]["item"] == "Lettuce"
    assert client.delete(f"/recipes/{rid}").status_code == 204
    assert client.get(f"/recipes/{rid}").status_code == 404


def test_recipe_errors(client):
    s = make_sandwich(client)
    res = make_resource(client)
    assert client.post("/recipes/", json={"sandwich_id": 999, "resource_id": res["id"], "amount": 1}).status_code == 404
    assert client.post("/recipes/", json={"sandwich_id": s["id"], "resource_id": 999, "amount": 1}).status_code == 404
    assert client.post("/recipes/", json={"sandwich_id": s["id"], "resource_id": res["id"], "amount": -1}).status_code == 422
    rid = client.post("/recipes/", json={"sandwich_id": s["id"], "resource_id": res["id"], "amount": 1}).json()["id"]
    assert client.put(f"/recipes/{rid}", json={"sandwich_id": 999}).status_code == 404
    # a resource used by a recipe can't be deleted
    assert client.delete(f"/resources/{res['id']}").status_code == 400
    assert client.delete("/recipes/999").status_code == 404


# ---------- Order details ----------
def test_order_detail_crud(client):
    s = make_sandwich(client)
    s2 = make_sandwich(client, "Club", 8)
    o = make_order(client)
    r = client.post("/order-details/", json={"order_id": o["id"], "sandwich_id": s["id"], "amount": 2})
    assert r.status_code == 201, r.text
    did = r.json()["id"]
    assert r.json()["sandwich"]["sandwich_name"] == "BLT"
    assert len(client.get("/order-details/").json()) == 1
    assert client.get(f"/order-details/{did}").json()["amount"] == 2
    assert client.get(f"/orders/{o['id']}").json()["order_details"][0]["id"] == did
    u = client.put(f"/order-details/{did}", json={"sandwich_id": s2["id"], "amount": 3})
    assert u.status_code == 200 and u.json()["amount"] == 3 and u.json()["sandwich"]["sandwich_name"] == "Club"
    assert client.delete(f"/order-details/{did}").status_code == 204
    assert client.get(f"/order-details/{did}").status_code == 404


def test_order_detail_errors(client):
    s = make_sandwich(client)
    o = make_order(client)
    assert client.post("/order-details/", json={"order_id": 999, "sandwich_id": s["id"], "amount": 1}).status_code == 404
    assert client.post("/order-details/", json={"order_id": o["id"], "sandwich_id": 999, "amount": 1}).status_code == 404
    assert client.post("/order-details/", json={"order_id": o["id"], "sandwich_id": s["id"], "amount": 0}).status_code == 422
    client.post("/order-details/", json={"order_id": o["id"], "sandwich_id": s["id"], "amount": 1})
    # a sandwich that has been ordered can't be deleted
    assert client.delete(f"/sandwiches/{s['id']}").status_code == 400
    assert client.put("/order-details/999", json={"amount": 1}).status_code == 404
    assert client.delete("/order-details/999").status_code == 404


# ---------- Orders ----------
def test_order_crud(client):
    o = make_order(client)
    assert o["order_date"] is not None
    assert client.get(f"/orders/{o['id']}").json()["customer_name"] == "John Doe"
    u = client.put(f"/orders/{o['id']}", json={"description": "Updated"})
    assert u.json()["description"] == "Updated"
    assert client.delete(f"/orders/{o['id']}").status_code == 204
    assert client.get(f"/orders/{o['id']}").status_code == 404
