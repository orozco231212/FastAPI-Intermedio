"""Punto de entrada de la API REST device_systems."""

from fastapi import FastAPI, Request
from app.routes.user_routes import router as users_router

app = FastAPI(
    title="device_systems API",
    description="API REST intermedia para gestionar usuarios con CRUD completo, errores controlados y Dependency Injection.",
    version="2.0.0",
    contact={"name": "Equipo device_systems", "email": "soporte@device-systems.example"},
    openapi_tags=[{"name": "users", "description": "Operaciones CRUD del recurso usuarios."}],
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(users_router)


@app.get("/", summary="Información de la API")
async def root() -> dict[str, str]:
    return {
        "message": "Bienvenido a device_systems API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", summary="Comprobar disponibilidad")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "device_systems"}


@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return response



