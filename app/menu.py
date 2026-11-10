from dataclasses import dataclass


@dataclass(frozen=True)
class Producto:
    codigo: str
    nombre: str
    precio: int  # pesos colombianos, sin decimales


PRODUCTOS = {
    p.codigo: p
    for p in [
        Producto("TINTO", "Tinto", 3_000),
        Producto("CAPUCHINO", "Capuchino", 7_500),
        Producto("PANDEBONO", "Pandebono", 3_500),
        Producto("CAFE_CASA", "Café de la casa, libra", 32_000),
    ]
}


def todos() -> list[Producto]:
    return list(PRODUCTOS.values())


def buscar(codigo: str) -> Producto | None:
    return PRODUCTOS.get(codigo)
