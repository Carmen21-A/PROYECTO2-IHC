"""
Pruebas para la Regla: ¿El límite mensual es válido?
IHC Clase 14 - Del requisito al código
Proyecto: Presupuesto Estudiantil

Parte 1: pruebas unitarias de la regla (funciones puras).
Parte 2: pruebas del flujo completo API -> regla -> base de datos.
"""

from datetime import date
import pytest
import models
from reglas_presupuesto import (
    es_limite_mensual_valido,
    validar_limite_mensual,
    validar_gasto_con_limite,
)

HOY = date.today().strftime("%Y-%m-%d")


# ===================== Parte 1: regla (unitarias) =====================

def test_01_caso_permitido_limite_valido():
    """Caso permitido: ya gastó 70 Bs y define un límite de 500 Bs."""
    assert es_limite_mensual_valido(500.0, gastos_mes=70.0) is True
    assert validar_limite_mensual(500.0, gastos_mes=70.0) is None


def test_02_caso_permitido_limite_igual_a_lo_gastado():
    """Caso permitido: el límite puede ser igual a lo ya gastado."""
    assert es_limite_mensual_valido(70.0, gastos_mes=70.0) is True


def test_03_caso_rechazado_limite_cero_o_negativo():
    """Caso rechazado: 0 Bs o un número negativo."""
    assert es_limite_mensual_valido(0.0) is False
    assert es_limite_mensual_valido(-50.0) is False
    assert "mayor a 0" in validar_limite_mensual(0)


@pytest.mark.parametrize("valor", [None, "", "   ", "quinientos", "50abc", True, float("nan")])
def test_04_caso_rechazado_vacio_o_con_letras(valor):
    """Caso rechazado: vacío, con letras o que no es un número."""
    assert es_limite_mensual_valido(valor) is False


def test_05_caso_permitido_texto_numerico():
    """Caso permitido: el formulario puede enviar el número como texto ("500" o "500,50")."""
    assert es_limite_mensual_valido("500") is True
    assert es_limite_mensual_valido("500,50") is True


def test_06_caso_rechazado_limite_menor_a_gastos_actuales():
    """Caso rechazado: ya gastó 70 Bs y quiere un límite de 50 Bs."""
    assert es_limite_mensual_valido(50.0, gastos_mes=70.0) is False
    assert "menor que lo que ya gastaste" in validar_limite_mensual(50.0, gastos_mes=70.0)


def test_07_caso_permitido_gasto_dentro_del_limite():
    """Caso permitido: lleva 300 Bs, límite 500 Bs, gasto nuevo de 200 Bs (llega justo a 500)."""
    assert validar_gasto_con_limite(200.0, gastos_mes=300.0, limite=500.0) is None


def test_08_caso_rechazado_gasto_supera_el_limite():
    """Caso rechazado: lleva 450 Bs, límite 500 Bs, gasto nuevo de 80 Bs (llegaría a 530)."""
    motivo = validar_gasto_con_limite(80.0, gastos_mes=450.0, limite=500.0)
    assert motivo is not None
    assert "superarían tu límite de 500.00 Bs" in motivo
    assert "Solo te quedan 50.00 Bs" in motivo


def test_09_caso_permitido_sin_limite_definido():
    """Si el estudiante no definió límite, ningún gasto se bloquea."""
    assert validar_gasto_con_limite(10000.0, gastos_mes=0.0, limite=None) is None


# ============ Parte 2: interfaz -> regla -> base de datos ============

def crear_gasto(client, monto, fecha=HOY, descripcion="Gasto"):
    return client.post("/movimientos", json={
        "descripcion": descripcion, "monto": monto, "tipo": "gasto", "fecha": fecha
    })


def test_10_api_define_limite_y_se_guarda_en_bd(client, db_session):
    res = client.put("/limite", json={"limite": 500})
    assert res.status_code == 200
    assert res.json()["limite"] == 500.0

    # Se mantiene al "recargar": lo leemos de nuevo y está en la base de datos
    assert client.get("/limite").json()["limite"] == 500.0
    usuario = db_session.get(models.Usuario, 1)
    assert float(usuario.limite_mensual) == 500.0


@pytest.mark.parametrize("valor", ["", 0, -20, "abc", None])
def test_11_api_rechaza_limite_invalido(client, valor):
    res = client.put("/limite", json={"limite": valor})
    assert res.status_code == 400
    assert client.get("/limite").json()["limite"] is None


def test_12_api_rechaza_limite_menor_a_lo_gastado(client):
    assert crear_gasto(client, 120).status_code == 200
    res = client.put("/limite", json={"limite": 100})
    assert res.status_code == 400
    assert "120.00 Bs" in res.json()["detail"]


def test_13_api_muestra_gastado_y_disponible(client):
    client.put("/limite", json={"limite": 500})
    crear_gasto(client, 150)
    datos = client.get("/limite").json()
    assert datos["gastado_mes"] == 150.0
    assert datos["disponible"] == 350.0


def test_14_api_bloquea_gasto_que_supera_el_limite(client):
    client.put("/limite", json={"limite": 200})
    assert crear_gasto(client, 150).status_code == 200

    res = crear_gasto(client, 80)
    assert res.status_code == 409
    assert "Gasto bloqueado" in res.json()["detail"]
    # El gasto rechazado no se guardó
    assert client.get("/limite").json()["gastado_mes"] == 150.0


def test_15_api_bloquea_edicion_que_supera_el_limite(client):
    client.put("/limite", json={"limite": 200})
    mov_id = crear_gasto(client, 150).json()["id"]

    res = client.put(f"/movimientos/{mov_id}", json={"monto": 250})
    assert res.status_code == 409
    assert client.get("/limite").json()["gastado_mes"] == 150.0


def test_16_cada_usuario_ve_solo_su_limite(client, db_session):
    otro = models.Usuario(id=2, nombre="Otro", email="otro@universidad.edu",
                          password_hash="x", limite_mensual=999)
    db_session.add(otro)
    db_session.commit()

    client.put("/limite", json={"limite": 300})
    assert client.get("/limite").json()["limite"] == 300.0
    db_session.refresh(otro)
    assert float(otro.limite_mensual) == 999.0
