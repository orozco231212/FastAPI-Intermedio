# FastAPI Intermedio - device_systems

Proyecto de la actividad GA1-220501096-01-AA1-EV08: evolución de una API REST de usuarios con FastAPI.

La documentación completa está aquí:

[Ver documentación completa de device_systems](device_systems/README.md)

## Inicio rápido

Desde esta carpeta:

```powershell
cd device_systems
.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Abre la documentación interactiva:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Incluye

- CRUD completo de usuarios.
- GET, POST, PUT, PATCH y DELETE.
- Validación con Pydantic v2.
- Manejo de errores HTTP.
- Dependency Injection con `Depends()`.
- Pruebas automatizadas.
