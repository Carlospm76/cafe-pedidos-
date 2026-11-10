# Café La Montaña · API de pedidos

Proyecto de ejemplo de la clase **Automatización de pruebas y despliegue continuo**.
Una API en Python (FastAPI) que calcula el total de los pedidos de una cafetería,
con pruebas automáticas (pytest), integración continua (GitHub Actions) y
despliegue continuo en Render.

Esta es la **versión inicial**: incluye las reglas R1 a R3 con sus pruebas.
La regla R4 está pendiente: es la historia de usuario que se desarrolla en la
Parte 5 de la clase (ver «Tu tarea» al final).

## Reglas de negocio

| Regla | Descripción | Ejemplo |
| --- | --- | --- |
| R1 | El total es la suma de precio × cantidad | 2 tintos + 1 pandebono = $9.500 |
| R2 | Un pedido vacío o con cantidad menor que 1 es inválido | HTTP 400 |
| R3 | 10% de descuento desde $50.000 | $60.000 → $54.000 |
| R4 | *Pendiente:* los martes, el café de la casa cuesta la mitad | $32.000 → $16.000 |

## Estructura

```text
cafe-pedidos/
├── app/
│   ├── __init__.py
│   ├── menu.py            productos y precios
│   ├── calculadora.py     reglas de negocio R1 a R3
│   └── main.py            API HTTP con FastAPI
├── tests/
│   ├── test_calculadora.py   6 pruebas unitarias
│   └── test_api.py           2 pruebas de integración
├── .github/workflows/
│   ├── ci.yml             pruebas en cada pull request
│   └── cd.yml             pruebas + despliegue en Render tras cada merge a main
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pyproject.toml         configuración de pytest
├── requirements.txt       dependencias de producción
└── requirements-dev.txt   dependencias para desarrollo y pruebas
```

## Ejecutar en local

Requisitos: Python 3.12 o superior (probado con 3.13).

```bash
python -m venv .venv
source .venv/bin/activate          # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt

pytest                             # 8 passed
uvicorn app.main:app --reload      # http://localhost:8000/docs
```

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/api/menu` | Lista de productos |
| POST | `/api/pedidos/total` | Total de un pedido; cuerpo: `[{"codigo":"TINTO","cantidad":2}]` |
| GET | `/health` | `{"status":"UP"}`; lo usan Render y el pipeline |
| GET | `/info` | Commit desplegado (`RENDER_GIT_COMMIT`), o `local` |

```bash
curl -X POST http://localhost:8000/api/pedidos/total \
  -H "Content-Type: application/json" \
  -d '[{"codigo":"TINTO","cantidad":2},{"codigo":"PANDEBONO","cantidad":1}]'
# {"subtotal":9500,"descuento":0,"total":9500}
```

## Docker

```bash
docker build -t cafe-pedidos .
docker run --rm -p 8000:8000 cafe-pedidos
```

## Configurar CI/CD (resumen)

1. Sube el proyecto a un repositorio de GitHub y abre un primer pull request para que corra `ci.yml`.
2. **Settings → Branches**: protege `main` exigiendo pull request y el check `Pruebas`.
3. En **Render**: New → Web Service → este repositorio, Docker, plan Free,
   Health Check Path `/health`. Luego **Settings → Auto-Deploy: Off** y copia el **Deploy Hook**.
4. En GitHub, **Settings → Secrets and variables → Actions**:
   - Secret `RENDER_DEPLOY_HOOK_URL` = la URL del deploy hook (es un secreto).
   - Variable `APP_URL` = la URL pública del servicio, sin `/` al final.
5. Cada merge a `main` corre las pruebas y, si pasan, despliega ese mismo commit y
   verifica con una prueba de humo que `/info` muestre el commit nuevo.

El paso a paso completo está en el documento de la clase.

## Notas

- Al correr `pytest` puede aparecer un aviso de deprecación del `TestClient`; no afecta el resultado.
- En el plan Free de Render el servicio se duerme tras 15 minutos sin tráfico y tarda
  cerca de un minuto en despertar.

## Tu tarea: HU-R4

> Como cliente, quiero que los martes el café de la casa cueste la mitad,
> para aprovechar la promoción.

Criterios de aceptación:

- El martes (hora de Bogotá) una libra de `CAFE_CASA` cuesta $16.000.
- Los demás productos no cambian de precio.
- El descuento de R3 se calcula sobre el subtotal ya rebajado.

Cómo trabajarla:

1. Crea la rama `feature/R4-martes`.
2. **Primero las pruebas (rojo):** en `tests/test_calculadora.py` crea una
   calculadora con una fecha fija de martes, por ejemplo
   `CalculadoraPedido(hoy=lambda: date(2026, 11, 3))`, y escribe al menos una
   prueba por criterio. Ejecuta `pytest` y comprueba que fallan.
3. **Luego el código (verde):** en `app/calculadora.py` usa `self.hoy()` para
   saber qué día es (`date.weekday()` devuelve 0 el lunes y 1 el martes) y
   aplica el precio del día. Ejecuta `pytest` hasta que todo pase.
4. Haz commit, push y abre un pull request. Deja que CI lo pruebe, pide revisión
   e intégralo: CD lo desplegará.
