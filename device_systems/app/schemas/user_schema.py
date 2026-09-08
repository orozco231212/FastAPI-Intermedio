"""Modelos Pydantic para validar usuarios de la API."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRole(str, Enum):
    ADMIN = "admin"
    SUPPORT = "support"
    USER = "user"


class UserCreate(BaseModel):
    """Datos recibidos al registrar un usuario."""

    name: str = Field(min_length=3, description="Nombre del usuario")
    email: EmailStr = Field(description="Correo electrónico válido")
    role: UserRole = Field(description="Rol permitido del usuario")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")

    @field_validator("name")
    @classmethod
    def name_must_have_text(cls, value: str) -> str:
        normalized_name = " ".join(value.split())
        if len(normalized_name) < 3:
            raise ValueError("El nombre debe contener al menos 3 caracteres")
        return normalized_name


class UserUpdate(UserCreate):
    """Datos completos requeridos por PUT."""


class UserPatch(BaseModel):
    """Campos opcionales permitidos por PATCH."""

    name: str | None = Field(default=None, min_length=3)
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized_name = " ".join(value.split())
        if len(normalized_name) < 3:
            raise ValueError("El nombre debe contener al menos 3 caracteres")
        return normalized_name


class UserResponse(BaseModel):
    """Representación pública de un usuario."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
