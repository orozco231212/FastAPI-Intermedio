"""Endpoints REST para la gestión de usuarios."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status

from app.dependencies.user_dependencies import get_user_or_404
from app.schemas.user_schema import UserCreate, UserPatch, UserResponse, UserRole, UserUpdate
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Usuario no encontrado"}},
)

@router.get(
    "",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Devuelve usuarios y permite filtrar por rol y estado.",
    response_description="Lista de usuarios encontrados",
)
async def get_users(
    role: Annotated[UserRole | None, Query(description="Filtrar por rol")] = None,
    is_active: Annotated[bool | None, Query(description="Filtrar por estado")] = None,
) -> list[dict]:
    return user_service.list_users(role, is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario por ID",
    description="Busca un usuario mediante un parámetro de ruta.",
    response_description="Usuario solicitado",
)
async def get_user(user: Annotated[dict, Depends(get_user_or_404)]) -> dict:
    return user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un usuario validado con Pydantic y evita correos duplicados.",
    response_description="Usuario creado",
)
async def create_user(user: UserCreate) -> dict:
    return user_service.create_user(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completamente",
    description="Reemplaza todos los campos editables de un usuario existente.",
    response_description="Usuario actualizado",
)
async def update_user(
    user: UserUpdate,
    current_user: Annotated[dict, Depends(get_user_or_404)],
) -> dict:
    return user_service.update_user(current_user["id"], user, current_user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Modifica únicamente los campos enviados por el cliente.",
    response_description="Usuario actualizado parcialmente",
)
async def patch_user(
    current_user: Annotated[dict, Depends(get_user_or_404)],
    user: UserPatch | None = None,
) -> dict:
    return user_service.patch_user(user, current_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente y no devuelve contenido.",
    response_description="Usuario eliminado correctamente",
)
async def delete_user(
    current_user: Annotated[dict, Depends(get_user_or_404)],
) -> Response:
    user_service.delete_user(current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
