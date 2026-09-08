from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from app.data.users_db import users_db
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_users_db() -> None:
    original_users = deepcopy(users_db)
    yield
    users_db[:] = original_users


def test_list_users_returns_custom_headers() -> None:
    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) >= 3
    assert response.headers["X-App-Name"] == "device_systems"
    assert response.headers["X-API-Version"] == "1.0"


def test_filters_users_by_role_and_status() -> None:
    response = client.get("/users", params={"role": "admin", "is_active": "true"})

    assert response.status_code == 200
    assert all(user["role"] == "admin" and user["is_active"] for user in response.json())


def test_get_user_by_id_returns_404_when_missing() -> None:
    response = client.get("/users/999")

    assert response.status_code == 404


def test_create_user_validates_and_rejects_duplicate_email() -> None:
    payload = {
        "name": "Ana Torres",
        "email": "ana.torres@example.com",
        "role": "support",
        "is_active": True,
    }

    created_response = client.post("/users", json=payload)
    duplicate_response = client.post("/users", json=payload)

    assert created_response.status_code == 201
    assert created_response.json()["name"] == "Ana Torres"
    assert duplicate_response.status_code == 400


def test_create_user_rejects_short_name() -> None:
    response = client.post(
        "/users",
        json={"name": "AB", "email": "valid@example.com", "role": "user"},
    )

    assert response.status_code == 422


def test_put_replaces_complete_user() -> None:
    response = client.put(
        "/users/1",
        json={
            "name": "Juan Actualizado",
            "email": "juan.actualizado@example.com",
            "role": "support",
            "is_active": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["role"] == "support"
    assert response.json()["is_active"] is False


def test_put_rejects_duplicate_email_and_missing_user() -> None:
    duplicate = client.put(
        "/users/1",
        json={
            "name": "Juan Actualizado",
            "email": "maria@example.com",
            "role": "user",
            "is_active": True,
        },
    )
    missing = client.put(
        "/users/999",
        json={
            "name": "Usuario Nuevo",
            "email": "nuevo@example.com",
            "role": "user",
            "is_active": True,
        },
    )

    assert duplicate.status_code == 400
    assert missing.status_code == 404


def test_patch_updates_only_sent_fields_and_rejects_empty_body() -> None:
    response = client.patch("/users/1", json={"role": "support"})
    empty = client.patch("/users/1", json={})
    missing = client.patch("/users/999", json={"role": "user"})

    assert response.status_code == 200
    assert response.json()["role"] == "support"
    assert response.json()["name"] == "Juan Pérez"
    assert empty.status_code == 400
    assert missing.status_code == 404


def test_delete_removes_user_and_returns_no_content() -> None:
    response = client.delete("/users/1")
    missing = client.delete("/users/1")

    assert response.status_code == 204
    assert response.content == b""
    assert missing.status_code == 404
