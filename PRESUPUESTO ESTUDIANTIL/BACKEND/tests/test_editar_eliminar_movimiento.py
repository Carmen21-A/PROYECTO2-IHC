"""
=============================================================================
PRUEBAS UNITARIAS: CICLO COMPLETO DEL MOVIMIENTO - PRESUPUESTO ESTUDIANTIL (TAREA 3)
=============================================================================
Proyecto: Presupuesto Estudiantil
Entidad: Movimiento (Gasto)
Restricción según estado: un movimiento PAGADO no permite modificar su monto.

Pruebas:
1. Un movimiento pagado rechaza el cambio de monto (HTTP 409) con mensaje claro
   y el monto en BD no cambia.
2. La regla aislada (validar_edicion) bloquea el monto de un movimiento pagado.
3. Un movimiento pagado sí permite editar descripción y fecha.
4. Un movimiento pendiente sí permite editar el monto.
5. Eliminar un movimiento lo borra de la base de datos.
=============================================================================
"""

from datetime import date

import pytest
from fastapi import HTTPException

import models
import schemas
from routers.movimientos import validar_edicion, MENSAJE_MONTO_BLOQUEADO


def crear_movimiento(db_session, estado, monto=25.00):
    mov = models.Movimiento(
        usuario_id=1,
        monto=monto,
        tipo="gasto",
        descripcion="Transporte U",
        fecha=date(2026, 10, 5),
        estado=estado
    )
    db_session.add(mov)
    db_session.commit()
    db_session.refresh(mov)
    return mov


# =============================================================================
# PRUEBA 1: UN MOVIMIENTO PAGADO NO PERMITE MODIFICAR SU MONTO (API)
# =============================================================================
def test_01_pagado_rechaza_cambio_de_monto(client, db_session):
    mov = crear_movimiento(db_session, "pagado", monto=25.00)

    response = client.put(f"/movimientos/{mov.id}", json={"monto": 99.00})

    assert response.status_code == 409, f"Se esperaba HTTP 409 pero se obtuvo {response.status_code}"
    assert response.json()["detail"] == MENSAJE_MONTO_BLOQUEADO
    assert "pagado" in response.json()["detail"]

    db_session.refresh(mov)
    assert float(mov.monto) == 25.00, "El monto de un movimiento pagado no debe cambiar"
    assert mov.estado == "pagado"


# =============================================================================
# PRUEBA 2: LA REGLA AISLADA BLOQUEA EL MONTO DE UN MOVIMIENTO PAGADO
# =============================================================================
def test_02_regla_validar_edicion_bloquea_monto_pagado():
    pagado = models.Movimiento(monto=25.00, estado="pagado")
    pendiente = models.Movimiento(monto=25.00, estado="pendiente")

    with pytest.raises(HTTPException) as error:
        validar_edicion(pagado, schemas.MovimientoUpdate(monto=30.00))
    assert error.value.status_code == 409

    # Enviar el mismo monto (sin cambio real) o no enviarlo está permitido
    validar_edicion(pagado, schemas.MovimientoUpdate(monto=25.00))
    validar_edicion(pagado, schemas.MovimientoUpdate(descripcion="Micro"))
    # Un movimiento pendiente sí puede cambiar el monto
    validar_edicion(pendiente, schemas.MovimientoUpdate(monto=30.00))


# =============================================================================
# PRUEBA 3: UN MOVIMIENTO PAGADO SÍ PERMITE EDITAR DESCRIPCIÓN Y FECHA
# =============================================================================
def test_03_pagado_permite_editar_descripcion_y_fecha(client, db_session):
    mov = crear_movimiento(db_session, "pagado", monto=25.00)

    response = client.put(f"/movimientos/{mov.id}", json={
        "descripcion": "Pasaje minibús",
        "fecha": "2026-10-07",
        "monto": 25.00
    })

    assert response.status_code == 200, response.text
    db_session.refresh(mov)
    assert mov.descripcion == "Pasaje minibús"
    assert mov.fecha == date(2026, 10, 7)
    assert float(mov.monto) == 25.00


# =============================================================================
# PRUEBA 4: UN MOVIMIENTO PENDIENTE SÍ PERMITE EDITAR EL MONTO
# =============================================================================
def test_04_pendiente_permite_editar_monto(client, db_session):
    mov = crear_movimiento(db_session, "pendiente", monto=25.00)

    response = client.put(f"/movimientos/{mov.id}", json={"monto": 40.50})

    assert response.status_code == 200, response.text
    assert response.json()["monto"] == 40.50
    db_session.refresh(mov)
    assert float(mov.monto) == 40.50


# =============================================================================
# PRUEBA 5: ELIMINAR UN MOVIMIENTO LO BORRA DE LA BASE DE DATOS
# =============================================================================
def test_05_eliminar_movimiento(client, db_session):
    mov = crear_movimiento(db_session, "pagado")
    mov_id = mov.id

    response = client.delete(f"/movimientos/{mov_id}")
    assert response.status_code == 200, response.text

    db_session.expire_all()
    assert db_session.query(models.Movimiento).filter(models.Movimiento.id == mov_id).first() is None
    assert client.delete(f"/movimientos/{mov_id}").status_code == 404
