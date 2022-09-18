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

prices_json: list = [
    {
        "id": 1,
        "price": 11111.11,
        "datetime": "2022-11-11T11:11:11",
        "product_id": 1,
        "warehouse_id": 1
    },
    {
        "id": 2,
        "price": 100.10,
        "datetime": "2022-09-17T10:10:00",
        "product_id": 1,
        "warehouse_id": 2
    },
    {
        "id": 3,
        "price": 2500.50,
        "datetime": "2022-09-17T10:10:00",
        "product_id": 2,
        "warehouse_id": 2
    },
    {
        "id": 4,
        "price": 4500.15,
        "datetime": "2022-09-20T10:10:00",
        "product_id": 2,
        "warehouse_id": 2
    },
    {
        "id": 5,
        "price": 1500,
        "datetime": "2022-09-17T10:10:00",
        "product_id": 2,
        "warehouse_id": 3
    },
    {
        "id": 6,
        "price": 500,
        "datetime": "2022-09-17T10:10:00",
        "product_id": 3,
        "warehouse_id": 3
    },
    {
        "id": 7,
        "price": 600,
        "datetime": "2022-09-17T10:10:00",
        "product_id": 3,
        "warehouse_id": 1
    },
    {
        "id": 8,
        "price": 700,
        "datetime": "2022-09-17T10:10:00",
        "product_id": 3,
        "warehouse_id": 2
    },
    {
        "id": 9,
        "price": 1500,
        "datetime": "2022-09-20T10:10:00",
        "product_id": 3,
        "warehouse_id": 3
    },
]

product_count_json: list = [
    {
        "id": 1,
        "count": 1000,
        "datetime": "2022-11-11T11:11:11",
        "product_id": 1,
        "warehouse_group_id": 1
    },
    {
        "id": 2,
        "count": 100,
        "datetime": "2022-11-12T11:11:11",
        "product_id": 1,
        "warehouse_group_id": 1
    },
    {
        "id": 3,
        "count": 10000,
        "datetime": "2022-11-11T11:11:11",
        "product_id": 1,
        "warehouse_group_id": 2
    },
    {
        "id": 4,
        "count": 2000,
        "datetime": "2022-11-12T11:11:11",
        "product_id": 1,
        "warehouse_group_id": 2
    },
    {
        "id": 5,
        "count": 7500,
        "datetime": "2022-11-11T11:11:11",
        "product_id": 2,
        "warehouse_group_id": 2
    },
    {
        "id": 6,
        "count": 75,
        "datetime": "2022-11-13T11:11:11",
        "product_id": 2,
        "warehouse_group_id": 2
    },
    {
        "id": 7,
        "count": 14000,
        "datetime": "2022-11-13T11:11:11",
        "product_id": 2,
        "warehouse_group_id": 3
    },
    {
        "id": 8,
        "count": 100000,
        "datetime": "2022-11-11T11:11:11",
        "product_id": 3,
        "warehouse_group_id": 1
    },
    {
        "id": 9,
        "count": 1000,
        "datetime": "2022-11-11T11:11:11",
        "product_id": 3,
        "warehouse_group_id": 2
    },
    {
        "id": 10,
        "count": 15000,
        "datetime": "2022-11-11T11:11:11",
        "product_id": 3,
        "warehouse_group_id": 3
    },
    {
        "id": 11,
        "count": 1,
        "datetime": "2022-11-12T11:11:11",
        "product_id": 3,
        "warehouse_group_id": 1
    },
    {
        "id": 12,
        "count": 999,
        "datetime": "2022-11-12T11:11:11",
        "product_id": 3,
        "warehouse_group_id": 2
    },
    {
        "id": 13,
        "count": 150,
        "datetime": "2022-11-12T11:11:11",
        "product_id": 3,
        "warehouse_group_id": 3
    },
]
