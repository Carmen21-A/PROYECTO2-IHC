"""
Pruebas del Saldo Disponible
La app empieza en 0 Bs y el saldo nunca puede quedar negativo: sin dinero, no se paga.
"""

from datetime import date
import models
from saldo import calcular_resumen, validar_pago_con_saldo, validar_quitar_ingreso

HOY = date(2026, 10, 15)


def mov(tipo, monto, fecha, estado="pagado"):
    return {"tipo": tipo, "monto": monto, "estado": estado, "fecha": fecha}


# ===================== Parte 1: reglas puras =====================

def test_01_la_app_empieza_en_cero():
    assert calcular_resumen([], HOY)["saldo_disponible"] == 0.0


def test_02_saldo_es_ingresos_recibidos_menos_gastos_pagados_de_todos_los_meses():
    """Lo que sobró en septiembre sigue disponible en octubre, como en una billetera real."""
    historial = [
        mov("ingreso", 700, date(2026, 9, 1)),   # mesada septiembre
        mov("gasto", 500, date(2026, 9, 20)),
        mov("ingreso", 700, date(2026, 10, 1)),  # mesada octubre
        mov("gasto", 300, date(2026, 10, 10)),
    ]
    resumen = calcular_resumen(historial, HOY)
    assert resumen["saldo_disponible"] == 600.0          # 1400 - 800
    assert resumen["ingresos_del_mes"] == 700.0          # solo octubre
    assert resumen["gastos_del_mes"] == 300.0            # solo octubre


def test_03_lo_pendiente_no_mueve_el_saldo():
    """Un ingreso pendiente no llegó y un gasto pendiente no salió; sí cuentan en los totales del mes."""
    resumen = calcular_resumen([
        mov("ingreso", 700, HOY, "pagado"),
        mov("ingreso", 200, HOY, "pendiente"),
        mov("gasto", 50, HOY, "pendiente"),
    ], HOY)
    assert resumen["saldo_disponible"] == 700.0
    assert resumen["ingresos_del_mes"] == 900.0
    assert resumen["gastos_del_mes"] == 50.0


def test_04_caso_permitido_pago_con_saldo_suficiente():
    assert validar_pago_con_saldo(100, saldo=100) is None   # queda en 0, no negativo
    assert validar_pago_con_saldo(30, saldo=100) is None


def test_05_caso_rechazado_pago_sin_saldo_suficiente():
    motivo = validar_pago_con_saldo(150, saldo=100)
    assert "Saldo insuficiente" in motivo
    assert "150.00 Bs" in motivo and "100.00 Bs" in motivo


def test_06_caso_rechazado_quitar_ingreso_ya_gastado():
    assert validar_quitar_ingreso(700, saldo=200) is not None
    assert validar_quitar_ingreso(100, saldo=200) is None


# ===================== Parte 2: flujo por la API =====================

def crear(client, tipo, monto, estado="pendiente", descripcion="Movimiento"):
    return client.post("/movimientos", json={
        "descripcion": descripcion, "monto": monto, "tipo": tipo,
        "fecha": date.today().isoformat(), "estado": estado
    })


def saldo_api(client):
    return client.get("/movimientos").json()["resumen_mes"]["saldo_disponible"]


def test_07_api_no_permite_pagar_sin_dinero(client, db_session):
    gasto = crear(client, "gasto", 50).json()
    res = client.patch(f"/movimientos/{gasto['id']}/pagar")
    assert res.status_code == 409
    assert "Saldo insuficiente" in res.json()["detail"]
    # El gasto sigue pendiente y el saldo sigue en 0
    assert db_session.get(models.Movimiento, gasto["id"]).estado == "pendiente"
    assert saldo_api(client) == 0.0


def test_08_api_permite_pagar_despues_de_recibir_un_ingreso(client):
    ingreso = crear(client, "ingreso", 700, descripcion="Mesada").json()
    gasto = crear(client, "gasto", 50).json()
    assert client.patch(f"/movimientos/{gasto['id']}/pagar").status_code == 409   # la mesada aún no llegó

    assert client.patch(f"/movimientos/{ingreso['id']}/pagar").status_code == 200  # marcar como recibido
    assert client.patch(f"/movimientos/{gasto['id']}/pagar").status_code == 200
    assert saldo_api(client) == 650.0


def test_09_api_no_crea_un_gasto_ya_pagado_sin_dinero(client):
    res = crear(client, "gasto", 80, estado="pagado")
    assert res.status_code == 409
    assert client.get("/movimientos").json()["movimientos"] == []


def test_10_api_no_elimina_un_ingreso_que_ya_se_gasto(client):
    ingreso = crear(client, "ingreso", 100, estado="pagado").json()
    crear(client, "gasto", 60, estado="pagado")
    res = client.delete(f"/movimientos/{ingreso['id']}")
    assert res.status_code == 409
    assert saldo_api(client) == 40.0
