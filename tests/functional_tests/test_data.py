users_json: list = [
    {
        "username": "admin",
        "email": "admin@example.com",
        "phone": "0123456789",
        "role": "admin",
        "id": 1,
        "status": "confirmed",
        "password": "123456789"
    },
    {
        "username": "client1",
        "email": "client1@example.com",
        "phone": "147852369",
        "role": "user",
        "id": 2,
        "status": "confirmed",
        "password": "123654789"
    },
    {
        "username": "client2",
        "email": "client2@example.com",
        "phone": "1478523690",
        "role": "user",
        "id": 3,
        "status": "unconfirmed",
        "password": "123654789"
    }
]

products_json: list = [
    {
        "id": 1,
        "name": "jacket"
    },
    {
        "id": 2,
        "name": "pants"
    },
    {
        "id": 3,
        "name": "t-shirt"
    }
]

warehouse_groups_json: list = [
    {
        "id": 1,
        "name": "ozon"
    },
    {
        "id": 2,
        "name": "wildberries"
    },
    {
        "id": 3,
        "name": "yandex-market"
    }
]

warehouses_json: list = [
    {
        "id": 1,
        "name": "number-1",
        "warehouse_group_id": 3
    },
    {
        "id": 2,
        "name": "number-2",
        "warehouse_group_id": 2
    },
    {
        "id": 3,
        "name": "number-3",
        "warehouse_group_id": 1
    }
]
