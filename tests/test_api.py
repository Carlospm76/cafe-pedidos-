from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_calcula_el_total_de_un_pedido():
    respuesta = cliente.post("/api/pedidos/total", json=[
        {"codigo": "TINTO", "cantidad": 2},
        {"codigo": "PANDEBONO", "cantidad": 1},
    ])

    assert respuesta.status_code == 200
    assert respuesta.json()["total"] == 9500


def test_pedido_vacio_responde_400():
    respuesta = cliente.post("/api/pedidos/total", json=[])

    assert respuesta.status_code == 400
    assert respuesta.json() == {"detail": "El pedido no tiene productos"}
