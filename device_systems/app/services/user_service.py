"""Reglas de negocio y operaciones CRUD de usuarios."""

from fastapi import HTTPException, status

from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate, UserPatch, UserRole, UserUpdate


def list_users(role: UserRole | None = None, is_active: bool | None = None) -> list[dict]:
    result = users_db.copy()
    if role is not None:
        result = [user for user in result if user["role"] == role.value]
    if is_active is not None:
        result = [user for user in result if user["is_active"] == is_active]
    return result


def create_user(user: UserCreate) -> dict:
    global_next_id = max((item["id"] for item in users_db), default=0) + 1
    ensure_email_available(str(user.email))
    new_user = {"id": global_next_id, **user.model_dump()}
    new_user["email"] = str(user.email)
    new_user["role"] = user.role.value
    users_db.append(new_user)
    return new_user


def update_user(user_id: int, user: UserUpdate, current_user: dict) -> dict:
    ensure_email_available(str(user.email), user_id)
    current_user.update(user.model_dump())
    current_user["email"] = str(user.email)
    current_user["role"] = user.role.value
    return current_user


def patch_user(user: UserPatch | None, current_user: dict) -> dict:
    changes = user.model_dump(exclude_unset=True) if user is not None else {}
    if not changes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar",
        )
    if "email" in changes:
        ensure_email_available(str(changes["email"]), current_user["id"])
        changes["email"] = str(changes["email"])
    if "role" in changes:
        changes["role"] = changes["role"].value
    current_user.update(changes)
    return current_user


def delete_user(current_user: dict) -> None:
    users_db.remove(current_user)


def ensure_email_available(email: str, excluded_user_id: int | None = None) -> None:
    duplicate = any(
        user["email"] == email and user["id"] != excluded_user_id
        for user in users_db
    )
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado en el sistema",
        )
