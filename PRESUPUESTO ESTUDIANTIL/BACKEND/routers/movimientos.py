from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
import models
import schemas
from security import get_current_user

router = APIRouter(prefix="/movimientos", tags=["Movimientos Estudiantiles"])

def bloquear_demo(usuario: models.Usuario):
    if usuario.es_demo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Modo demo: no se pueden registrar ni eliminar movimientos."
        )

@router.get("", response_model=schemas.ResumenFinanciero)
def listar_movimientos(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    movimientos_db = db.query(models.Movimiento)\
        .filter(models.Movimiento.usuario_id == usuario.id)\
        .order_by(models.Movimiento.fecha.desc(), models.Movimiento.id.desc())\
        .all()

    movimientos_out = []
    ingresos = 0.0
    gastos = 0.0

    for m in movimientos_db:
        monto_float = float(m.monto)
        if m.tipo == "ingreso":
            ingresos += monto_float
        else:
            gastos += monto_float

        categoria_nombre = "General"
        if m.categoria_id:
            cat = db.query(models.Categoria).filter(models.Categoria.id == m.categoria_id).first()
            if cat:
                categoria_nombre = cat.nombre

        movimientos_out.append({
            "id": m.id,
            "descripcion": m.descripcion,
            "categoria": categoria_nombre,
            "monto": monto_float,
            "tipo": m.tipo,
            "fecha": m.fecha.strftime("%b %d") if hasattr(m.fecha, 'strftime') else str(m.fecha)
        })

    saldo = round(ingresos - gastos, 2)

    return {
        "saldo_disponible": saldo,
        "ingresos_del_mes": round(ingresos, 2),
        "gastos_del_mes": round(gastos, 2),
        "movimientos": movimientos_out
    }

@router.post("", response_model=schemas.MovimientoOut)
def crear_movimiento(
    datos: schemas.MovimientoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    bloquear_demo(usuario)

    cat = db.query(models.Categoria).filter(models.Categoria.nombre == datos.categoria).first()
    cat_id = cat.id if cat else None

    nuevo = models.Movimiento(
        usuario_id=usuario.id,
        categoria_id=cat_id,
        monto=datos.monto,
        tipo=datos.tipo,
        descripcion=datos.descripcion.strip(),
        fecha=datetime.utcnow().date()
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "id": nuevo.id,
        "descripcion": nuevo.descripcion,
        "categoria": datos.categoria,
        "monto": float(nuevo.monto),
        "tipo": nuevo.tipo,
        "fecha": nuevo.fecha.strftime("%b %d")
    }

@router.delete("/{movimiento_id}")
def eliminar_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    bloquear_demo(usuario)

    mov = db.query(models.Movimiento).filter(
        models.Movimiento.id == movimiento_id,
        models.Movimiento.usuario_id == usuario.id
    ).first()

    if not mov:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")

    db.delete(mov)
    db.commit()
    return {"mensaje": "Movimiento eliminado exitosamente."}
