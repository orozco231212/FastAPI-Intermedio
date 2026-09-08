# device_systems: FastAPI Intermedio

API REST para administrar usuarios con CRUD completo. Esta es la evolución de la actividad GA1-220501096-01-AA1-EV07 y corresponde a la evidencia EV08.

## Tecnologías

- Python 3.10+
- FastAPI
- Pydantic v2
- Uvicorn
- Pytest y HTTPX

## Instalación y ejecución en Windows

Desde la raíz del repositorio:

```powershell
cd device_systems
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Si PowerShell bloquea la activación:

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

La API estará en `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Para detener el servidor, presiona `Ctrl+C`.

## Estructura del proyecto

```text
device_systems/
├── app/
│   ├── main.py
│   ├── data/
│   │   └── users_db.py
│   ├── dependencies/
│   │   └── user_dependencies.py
│   ├── routes/
│   │   └── user_routes.py
│   ├── schemas/
│   │   └── user_schema.py
│   └── services/
│       └── user_service.py
├── tests/
│   └── test_users.py
├── .gitignore
├── requirements.txt
└── README.md
```

La base de datos es simulada en memoria. Los cambios se reinician al apagar el servidor.

## Endpoints

| Método | Ruta | Código | Función |
|---|---|---:|---|
| GET | `/users` | 200 | Lista usuarios y filtra por `role` o `is_active` |
| GET | `/users/{user_id}` | 200 | Consulta por ID |
| POST | `/users` | 201 | Crea un usuario |
| PUT | `/users/{user_id}` | 200 | Reemplaza todos los campos |
| PATCH | `/users/{user_id}` | 200 | Actualiza solo campos enviados |
| DELETE | `/users/{user_id}` | 204 | Elimina sin cuerpo de respuesta |
| GET | `/health` | 200 | Comprueba el estado de la API |

## Modelo de usuario

```json
{
  "name": "Ana Torres",
  "email": "ana.torres@example.com",
  "role": "support",
  "is_active": true
}
```

El nombre requiere mínimo 3 caracteres, el correo debe ser válido y único, el rol debe ser `admin`, `support` o `user`, e `is_active` es booleano y por defecto vale `true`. El `id` se genera automáticamente.

## Ejemplos con curl

```powershell
curl http://127.0.0.1:8000/users
curl "http://127.0.0.1:8000/users?role=admin&is_active=true"
curl http://127.0.0.1:8000/users/1
curl -X POST http://127.0.0.1:8000/users -H "Content-Type: application/json" -d '{"name":"Ana Torres","email":"ana@example.com","role":"support","is_active":true}'
curl -X PUT http://127.0.0.1:8000/users/1 -H "Content-Type: application/json" -d '{"name":"Juan Actualizado","email":"juan.nuevo@example.com","role":"user","is_active":true}'
curl -X PATCH http://127.0.0.1:8000/users/1 -H "Content-Type: application/json" -d '{"role":"support"}'
curl -X DELETE http://127.0.0.1:8000/users/1
```

## Códigos de error

- `400 Bad Request`: correo duplicado o PATCH sin campos.
- `404 Not Found`: usuario inexistente.
- `422 Unprocessable Entity`: nombre, correo, rol, estado o cuerpo inválido.

Todas las respuestas incluyen `X-App-Name: device_systems` y `X-API-Version: 1.0`.

## Dependency Injection

La función `get_user_or_404` está en `app/dependencies/user_dependencies.py`. Busca el usuario y lanza `HTTPException(404)` si no existe. Las rutas de consulta por ID, PUT, PATCH y DELETE la reutilizan mediante `Depends()`, evitando repetir la búsqueda y el manejo del error.

## Manejo de errores

Las reglas de negocio están en `app/services/user_service.py`. Allí se valida el correo duplicado y el PATCH vacío mediante `HTTPException`. Pydantic se encarga de validar automáticamente los datos inválidos y FastAPI los transforma en respuestas `422`.

## Pruebas automatizadas

Desde la carpeta `device_systems`:

```powershell
.venv\Scripts\python.exe -m pytest tests -q
```

La suite comprueba listado, filtros, cabeceras, consulta por ID, POST, PUT, PATCH, DELETE, duplicados, datos inválidos y usuarios inexistentes.

## Evidencias para la entrega

Captura en Swagger UI y ReDoc:

1. `GET /users` y `GET /users/{user_id}`.
2. `POST /users` exitoso y con correo repetido.
3. `PUT /users/{user_id}` completo.
4. `PATCH /users/{user_id}` con un campo y con cuerpo vacío.
5. `DELETE /users/{user_id}` exitoso y con ID inexistente.
6. Respuestas `400`, `404` y `422`.

Puedes guardar las imágenes en una carpeta `docs/images/` y enlazarlas aquí antes de presentar la evidencia:

```markdown
![Swagger UI](docs/images/swagger.png)
![ReDoc](docs/images/redoc.png)
```

## Reflexión final

La API evolucionó de una solución básica con GET y POST a una API CRUD organizada por responsabilidades. PUT, PATCH y DELETE permiten administrar el ciclo completo del usuario; los códigos HTTP comunican claramente el resultado; y `Depends()` centraliza la búsqueda de usuarios y evita duplicar errores. Swagger y ReDoc facilitan probar y documentar cada operación.
