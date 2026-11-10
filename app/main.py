import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import menu
from app.calculadora import CalculadoraPedido, Item, PedidoInvalido

app = FastAPI(title="Café La Montaña - API de pedidos")
calculadora = CalculadoraPedido()


class ItemPedido(BaseModel):
    codigo: str
    cantidad: int


@app.get("/api/menu")
def ver_menu():
    return menu.todos()


@app.post("/api/pedidos/total")
def calcular_total(items: list[ItemPedido]):
    try:
        return calculadora.calcular([Item(i.codigo, i.cantidad) for i in items])
    except PedidoInvalido as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/health")
def health():
    return {"status": "UP"}


@app.get("/info")
def info():
    # Render define RENDER_GIT_COMMIT con el commit desplegado
    return {"commit": os.getenv("RENDER_GIT_COMMIT", "local")}
