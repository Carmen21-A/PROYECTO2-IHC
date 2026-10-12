from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from database import get_db
import models
import schemas
from security import get_current_user
from reglas_presupuesto import validar_gasto_con_limite
from routers.limite import gastos_del_mes, limite_del_usuario
from filtros_movimientos import crear_filtros, consultar_movimientos, calcular_totales
from saldo import calcular_resumen, validar_pago_con_saldo, validar_quitar_ingreso, saldo_actual

router = APIRouter(prefix="/movimientos", tags=["Movimientos Estudiantiles"])

def bloquear_demo(usuario: models.Usuario):
    if usuario.es_demo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Modo demo: no se pueden registrar ni modificar movimientos."
        )

MENSAJE_MONTO_BLOQUEADO = (
    "No se puede modificar el monto: este movimiento ya está pagado. "
    "Solo puedes cambiar la descripción y la fecha."
)

def validar_edicion(mov: models.Movimiento, datos: schemas.MovimientoUpdate):
    """Regla de estado (Tarea 3): un movimiento pagado no permite modificar su monto."""
    estado_actual = getattr(mov, "estado", "pendiente") or "pendiente"
    if estado_actual == "pagado" and datos.monto is not None             and round(float(datos.monto), 2) != round(float(mov.monto), 2):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=MENSAJE_MONTO_BLOQUEADO
        )

def verificar_limite_mensual(db: Session, usuario: models.Usuario, monto: float, fecha, excluir_id: int = None):
    """Regla del límite mensual: un gasto no puede hacer que el total del mes supere el límite."""
    gastado = gastos_del_mes(db, usuario.id, fecha, excluir_id)
    motivo = validar_gasto_con_limite(float(monto), gastado, limite_del_usuario(usuario))
    if motivo:
        db.rollback()  # una edición rechazada no debe dejar cambios pendientes
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=motivo)

def verificar_saldo_para_pago(db: Session, usuario: models.Usuario, monto: float):
    """Regla del saldo: no se paga con dinero que no hay."""
    motivo = validar_pago_con_saldo(float(monto), saldo_actual(db, usuario.id))
    if motivo:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=motivo)

def obtener_movimiento_propio(movimiento_id: int, db: Session, usuario: models.Usuario) -> models.Movimiento:
    mov = db.query(models.Movimiento).filter(
        models.Movimiento.id == movimiento_id,
        models.Movimiento.usuario_id == usuario.id
    ).first()
    if not mov:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")
    return mov

def serializar_movimiento(mov: models.Movimiento, db: Session) -> dict:
    categoria_nombre = "General"
    if mov.categoria_id:
        cat = db.query(models.Categoria).filter(models.Categoria.id == mov.categoria_id).first()
        if cat:
            categoria_nombre = cat.nombre
    return {
        "id": mov.id,
        "descripcion": mov.descripcion,
        "categoria": categoria_nombre,
        "monto": float(mov.monto),
        "tipo": mov.tipo,
        "fecha": mov.fecha.strftime("%Y-%m-%d") if hasattr(mov.fecha, 'strftime') else str(mov.fecha),
        "estado": getattr(mov, "estado", "pendiente") or "pendiente"
    }

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
        estado_val = getattr(m, "estado", "pendiente") or "pendiente"
        if m.tipo == "ingreso":
            ingresos += monto_float
        else:
            if estado_val == "pagado":
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
            "fecha": m.fecha.strftime("%Y-%m-%d") if hasattr(m.fecha, 'strftime') else str(m.fecha),
            "estado": estado_val
        })

    saldo = round(ingresos - gastos, 2)

    # Saldo acumulado (empieza en 0) y totales del mes actual (lo usan las cuentas normales)
    resumen_mes = calcular_resumen(
        [{"tipo": m.tipo, "monto": m.monto, "estado": m.estado or "pendiente", "fecha": m.fecha}
         for m in movimientos_db],
        date.today()
    )

    return {
        "saldo_disponible": saldo,
        "ingresos_del_mes": round(ingresos, 2),
        "gastos_del_mes": round(gastos, 2),
        "resumen_mes": resumen_mes,
        "movimientos": movimientos_out
    }

@router.get("/filtrar", response_model=schemas.ResultadoFiltro)
def filtrar_movimientos(
    q: Optional[str] = None,
    tipo: Optional[str] = None,
    categoria: Optional[str] = None,
    estado: Optional[str] = None,
    periodo: Optional[str] = None,
    desde: Optional[str] = None,
    hasta: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    """Issue #2: búsqueda y filtros combinables, con el total de lo que se encontró."""
    try:
        filtros = crear_filtros(q, tipo, categoria, estado, periodo, desde, hasta)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    movimientos = [serializar_movimiento(m, db) for m in consultar_movimientos(db, usuario.id, filtros)]
    return {"movimientos": movimientos, **calcular_totales(movimientos)}

@router.post("", response_model=schemas.MovimientoOut)
def crear_movimiento(
    datos: schemas.MovimientoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    bloquear_demo(usuario)

    cat = None
    if datos.categoria:
        cat = db.query(models.Categoria).filter(models.Categoria.nombre == datos.categoria).first()
    cat_id = cat.id if cat else None

    fecha_val = datetime.utcnow().date()
    if datos.fecha:
        try:
            fecha_val = datetime.strptime(datos.fecha, "%Y-%m-%d").date()
        except Exception:
            pass

    if (datos.tipo or "gasto") == "gasto":
        verificar_limite_mensual(db, usuario, datos.monto, fecha_val)
        if datos.estado == "pagado":
            verificar_saldo_para_pago(db, usuario, datos.monto)

    nuevo = models.Movimiento(
        usuario_id=usuario.id,
        categoria_id=cat_id,
        monto=datos.monto,
        tipo=datos.tipo or "gasto",
        descripcion=datos.descripcion.strip(),
        fecha=fecha_val,
        estado=datos.estado or "pendiente"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "id": nuevo.id,
        "descripcion": nuevo.descripcion,
        "categoria": cat.nombre if cat else (datos.categoria or "General"),
        "monto": float(nuevo.monto),
        "tipo": nuevo.tipo,
        "fecha": nuevo.fecha.strftime("%Y-%m-%d") if hasattr(nuevo.fecha, 'strftime') else str(nuevo.fecha),
        "estado": nuevo.estado
    }

@router.patch("/{movimiento_id}/pagar", response_model=schemas.MovimientoOut)
def marcar_como_pagado(
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

    if getattr(mov, "estado", "pendiente") == "pagado":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transición inválida: el movimiento ya se encuentra en estado pagado."
        )

    if mov.tipo == "gasto":
        verificar_saldo_para_pago(db, usuario, mov.monto)

    mov.estado = "pagado"
    db.commit()
    db.refresh(mov)

    categoria_nombre = "General"
    if mov.categoria_id:
        cat = db.query(models.Categoria).filter(models.Categoria.id == mov.categoria_id).first()
        if cat:
            categoria_nombre = cat.nombre

    return {
        "id": mov.id,
        "descripcion": mov.descripcion,
        "categoria": categoria_nombre,
        "monto": float(mov.monto),
        "tipo": mov.tipo,
        "fecha": mov.fecha.strftime("%Y-%m-%d") if hasattr(mov.fecha, 'strftime') else str(mov.fecha),
        "estado": mov.estado
    }

@router.put("/{movimiento_id}", response_model=schemas.MovimientoOut)
def editar_movimiento(
    movimiento_id: int,
    datos: schemas.MovimientoUpdate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    bloquear_demo(usuario)
    mov = obtener_movimiento_propio(movimiento_id, db, usuario)

    validar_edicion(mov, datos)

    if datos.descripcion is not None:
        descripcion = datos.descripcion.strip()
        if not descripcion:
            raise HTTPException(status_code=400, detail="La descripción no puede estar vacía.")
        mov.descripcion = descripcion

    if datos.monto is not None:
        if datos.monto <= 0:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0.")
        mov.monto = datos.monto

    if datos.fecha:
        try:
            mov.fecha = datetime.strptime(datos.fecha, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Fecha inválida. Usa el formato AAAA-MM-DD.")

    if mov.tipo == "gasto":
        verificar_limite_mensual(db, usuario, mov.monto, mov.fecha, excluir_id=mov.id)

    db.commit()
    db.refresh(mov)
    return serializar_movimiento(mov, db)

@router.delete("/{movimiento_id}")
def eliminar_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    bloquear_demo(usuario)
    mov = obtener_movimiento_propio(movimiento_id, db, usuario)
    if mov.tipo == "ingreso" and mov.estado == "pagado":
        motivo = validar_quitar_ingreso(float(mov.monto), saldo_actual(db, usuario.id))
        if motivo:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=motivo)
    db.delete(mov)
    db.commit()
    return {"ok": True, "id": movimiento_id}
