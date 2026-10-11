from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from security import get_current_user
from reglas_presupuesto import validar_limite_mensual, convertir_limite

router = APIRouter(prefix="/limite", tags=["Límite mensual de gastos"])

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

def gastos_del_mes(db: Session, usuario_id: int, fecha: date, excluir_id: int = None) -> float:
    """Suma los gastos (pagados y pendientes) del usuario en el mes de 'fecha'."""
    consulta = db.query(func.coalesce(func.sum(models.Movimiento.monto), 0)).filter(
        models.Movimiento.usuario_id == usuario_id,
        models.Movimiento.tipo == "gasto",
        extract("year", models.Movimiento.fecha) == fecha.year,
        extract("month", models.Movimiento.fecha) == fecha.month,
    )
    if excluir_id is not None:
        consulta = consulta.filter(models.Movimiento.id != excluir_id)
    return round(float(consulta.scalar() or 0), 2)

def limite_del_usuario(usuario: models.Usuario):
    return float(usuario.limite_mensual) if usuario.limite_mensual is not None else None

def resumen_limite(db: Session, usuario: models.Usuario) -> dict:
    hoy = date.today()
    limite = limite_del_usuario(usuario)
    gastado = gastos_del_mes(db, usuario.id, hoy)
    return {
        "limite": limite,
        "gastado_mes": gastado,
        "disponible": round(limite - gastado, 2) if limite is not None else None,
        "mes": f"{MESES[hoy.month - 1]} {hoy.year}",
    }

@router.get("", response_model=schemas.LimiteMensualOut)
def obtener_limite(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    return resumen_limite(db, usuario)

@router.put("", response_model=schemas.LimiteMensualOut)
def definir_limite(
    datos: schemas.LimiteMensualIn,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    if usuario.es_demo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Modo demo: no se puede cambiar el límite mensual."
        )

    gastado = gastos_del_mes(db, usuario.id, date.today())
    motivo = validar_limite_mensual(datos.limite, gastado)
    if motivo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=motivo)

    usuario.limite_mensual = round(convertir_limite(datos.limite), 2)
    db.commit()
    db.refresh(usuario)
    return resumen_limite(db, usuario)
