from datetime import date

import pytest

from app.calculadora import CalculadoraPedido, Item, PedidoInvalido

# Día fijo: lunes 2 de noviembre de 2026.
# Así la prueba da el mismo resultado cualquier día que se ejecute.
LUNES = date(2026, 11, 2)
calculadora = CalculadoraPedido(hoy=lambda: LUNES)


def test_suma_precio_por_cantidad():  # R1
    r = calculadora.calcular([Item("TINTO", 2), Item("PANDEBONO", 1)])

    assert r.subtotal == 9_500
    assert r.descuento == 0
    assert r.total == 9_500


def test_pedido_vacio_es_invalido():  # R2
    with pytest.raises(PedidoInvalido, match="no tiene productos"):
        calculadora.calcular([])


def test_cantidad_cero_es_invalida():  # R2
    with pytest.raises(PedidoInvalido):
        calculadora.calcular([Item("TINTO", 0)])


def test_producto_inexistente_es_invalido():
    with pytest.raises(PedidoInvalido, match="TE_VERDE"):
        calculadora.calcular([Item("TE_VERDE", 1)])


def test_justo_en_el_umbral_hay_descuento():  # R3: 50.000 exactos
    r = calculadora.calcular([
        Item("CAFE_CASA", 1),   # 32.000
        Item("CAPUCHINO", 2),   # 15.000
        Item("TINTO", 1),       #  3.000
    ])

    assert r.subtotal == 50_000
    assert r.descuento == 5_000
    assert r.total == 45_000


def test_poco_antes_del_umbral_no_hay_descuento():  # R3: 49.500
    r = calculadora.calcular([
        Item("CAFE_CASA", 1),   # 32.000
        Item("PANDEBONO", 5),   # 17.500
    ])

    assert r.subtotal == 49_500
    assert r.descuento == 0

