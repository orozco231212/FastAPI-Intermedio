"""Base de datos temporal en memoria para la demostración."""

users_db: list[dict] = [
    {
        "id": 1,
        "name": "Juan Pérez",
        "email": "juan@example.com",
        "role": "admin",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "María García",
        "email": "maria@example.com",
        "role": "user",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Carlos López",
        "email": "carlos@example.com",
        "role": "support",
        "is_active": False,
    },
]

next_id = 4
