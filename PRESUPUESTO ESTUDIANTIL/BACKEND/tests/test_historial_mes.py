"""
Pruebas del historial del mes
Issue #12: ¿Qué movimientos tuvo el mes?

Parte 1: reglas puras (mes pedido, agrupación por día y resumen).
Parte 2: consulta a la base de datos (mes correcto, orden y usuario correcto).
Parte 3: flujo completo por la API (una acción genera el evento, mes vacío, mes inválido).
"""

from datetime import date
import pytest
import models
from historial_mes import mes_desde_texto, consultar_historial, agrupar_por_dia, resumen_del_mes

HOY = date(2026, 10, 19)
OCTUBRE = date(2026, 10, 1)


def agregar(db, descripcion, fecha, monto=10, tipo="gasto", estado="pendiente", usuario_id=1):
    mov = models.Movimiento(usuario_id=usuario_id, descripcion=descripcion, fecha=fecha,
                            monto=monto, tipo=tipo, estado=estado)
    db.add(mov)
    db.commit()
    return mov


# ===================== Parte 1: reglas puras =====================

def test_01_sin_mes_usa_el_mes_actual():
    assert mes_desde_texto(None, HOY) == OCTUBRE
    assert mes_desde_texto("", HOY) == OCTUBRE


def test_02_mes_pedido_devuelve_su_primer_dia():
    assert mes_desde_texto("2026-09", HOY) == date(2026, 9, 1)


@pytest.mark.parametrize("texto", ["2026-13", "octubre", "2026-10-05", "2026/10"])
def test_03_mes_invalido_se_rechaza(texto):
    with pytest.raises(ValueError):
        mes_desde_texto(texto, HOY)


def test_04_agrupa_por_dia_sin_perder_el_orden():
    movimientos = [
        {"fecha": "2026-10-19", "descripcion": "Almuerzo"},
        {"fecha": "2026-10-19", "descripcion": "Pasaje"},
        {"fecha": "2026-10-04", "descripcion": "Salida"},
    ]
    dias = agrupar_por_dia(movimientos)
    assert [d["fecha"] for d in dias] == ["2026-10-19", "2026-10-04"]
    assert [m["descripcion"] for m in dias[0]["movimientos"]] == ["Almuerzo", "Pasaje"]


def test_05_resumen_calcula_ingresos_gastos_y_balance():
    movimientos = [
        {"tipo": "ingreso", "monto": 700},
        {"tipo": "gasto", "monto": 25.5},
        {"tipo": "gasto", "monto": 30},
    ]
    assert resumen_del_mes(movimientos) == {"cantidad": 3, "ingresos": 700.0, "gastos": 55.5, "balance": 644.5}


def test_06_mes_sin_movimientos_resumen_en_cero():
    assert agrupar_por_dia([]) == []
    assert resumen_del_mes([]) == {"cantidad": 0, "ingresos": 0.0, "gastos": 0.0, "balance": 0.0}


# ===================== Parte 2: consulta a la base de datos =====================

def test_07_solo_trae_el_mes_pedido_incluyendo_primer_y_ultimo_dia(db_session):
    agregar(db_session, "Fin de septiembre", date(2026, 9, 30))
    agregar(db_session, "Primer día", date(2026, 10, 1))
    agregar(db_session, "Último día", date(2026, 10, 31))
    agregar(db_session, "Inicio de noviembre", date(2026, 11, 1))

    descripciones = [m.descripcion for m in consultar_historial(db_session, 1, OCTUBRE)]
    assert descripciones == ["Último día", "Primer día"]


def test_08_ordena_del_mas_reciente_al_mas_antiguo(db_session):
    agregar(db_session, "Salida", date(2026, 10, 4))
    agregar(db_session, "Almuerzo", date(2026, 10, 19))
    agregar(db_session, "Pasaje", date(2026, 10, 19))  # mismo día: el último registrado va primero

    descripciones = [m.descripcion for m in consultar_historial(db_session, 1, OCTUBRE)]
    assert descripciones == ["Pasaje", "Almuerzo", "Salida"]


def test_09_no_muestra_movimientos_de_otro_usuario(db_session):
    db_session.add(models.Usuario(id=2, nombre="Otra Persona", email="otra@universidad.edu", password_hash="x"))
    db_session.commit()
    agregar(db_session, "Mío", date(2026, 10, 5))
    agregar(db_session, "De otra persona", date(2026, 10, 6), usuario_id=2)

    descripciones = [m.descripcion for m in consultar_historial(db_session, 1, OCTUBRE)]
    assert descripciones == ["Mío"]


# ===================== Parte 3: API =====================

def test_10_registrar_un_movimiento_aparece_en_el_historial_de_su_mes(client):
    nuevo = {"descripcion": "Fotocopias", "monto": 12, "tipo": "gasto", "fecha": "2026-10-08"}
    assert client.post("/movimientos", json=nuevo).status_code == 200

    data = client.get("/movimientos/historial?mes=2026-10").json()
    assert data["mes"] == "2026-10"
    assert data["mes_texto"] == "Octubre 2026"
    assert data["resumen"] == {"cantidad": 1, "ingresos": 0.0, "gastos": 12.0, "balance": -12.0}
    assert data["dias"][0]["fecha"] == "2026-10-08"
    assert data["dias"][0]["movimientos"][0]["descripcion"] == "Fotocopias"


def test_11_mes_sin_movimientos_devuelve_lista_vacia(client):
    data = client.get("/movimientos/historial?mes=2026-02").json()
    assert data["dias"] == []
    assert data["resumen"]["cantidad"] == 0


def test_12_mes_invalido_responde_400_con_motivo(client):
    res = client.get("/movimientos/historial?mes=2026-13")
    assert res.status_code == 400
    assert "AAAA-MM" in res.json()["detail"]
