"""Dependencias reutilizables para las rutas de usuarios."""

from fastapi import HTTPException, status

from app.data.users_db import users_db


def get_user_or_404(user_id: int) -> dict:
    user = next((item for item in users_db if item["id"] == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return user


def get_api_config() -> dict[str, str]:
    return {"name": "device_systems", "version": "2.0.0"}
