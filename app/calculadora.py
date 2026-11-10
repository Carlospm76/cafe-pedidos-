from dataclasses import dataclass
from datetime import date, datetime
from typing import Callable
from zoneinfo import ZoneInfo

from app import menu

UMBRAL_DESCUENTO = 50_000


class PedidoInvalido(Exception):
    pass


@dataclass(frozen=True)
class Item:
    codigo: str
    cantidad: int


@dataclass(frozen=True)
class Resumen:
    subtotal: int
    descuento: int
    total: int


def hoy_en_bogota() -> date:
    return datetime.now(ZoneInfo("America/Bogota")).date()


class CalculadoraPedido:
    def __init__(self, hoy: Callable[[], date] = hoy_en_bogota):
        self.hoy = hoy  # lo usaremos en la Parte 5

    def calcular(self, items: list[Item]) -> Resumen:
        if not items:
            raise PedidoInvalido("El pedido no tiene productos")
        subtotal = 0
        for item in items:
            if item.cantidad < 1:
                raise PedidoInvalido(f"Cantidad inválida para {item.codigo}")
            producto = menu.buscar(item.codigo)
            if producto is None:
                raise PedidoInvalido(f"No existe el producto {item.codigo}")
            subtotal += producto.precio * item.cantidad
        descuento = subtotal // 10 if subtotal > UMBRAL_DESCUENTO else 0
        return Resumen(subtotal, descuento, subtotal - descuento)

