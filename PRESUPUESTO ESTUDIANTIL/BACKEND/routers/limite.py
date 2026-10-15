from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from security import get_current_user
from reglas_presupuesto import validar_limite_mensual, convertir_limite
#Crea un enrutador de FastAPI. todas las rutas definidas aquí empezarán con /limite
router = APIRouter(prefix="/limite", tags=["Límite mensual de gastos"])

#nombres de los meses, para mostrar por ejemplo "Octubre 2026" en el panel
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

#funcion que suma lo gastado por un usuario en un mes.
#recibe la conexion (db), el usuario (usuario_id), una fecha para saber de que mes se trata (fecha)
#y opcionalmente, un gasto a ignorar (excluir_id) para no contarlo dos veces al editarlo.
def gastos_del_mes(db: Session, usuario_id: int, fecha: date, excluir_id: int = None) -> float:
    """Suma los gastos (pagados y pendientes) del usuario en el mes de 'fecha'."""
    #suma los montos de los movimientos que cumplan los filtros y que devuelve 0 si no hay ninguno, y la guarda en consulta
    consulta = db.query(func.coalesce(func.sum(models.Movimiento.monto), 0)).filter(
        models.Movimiento.usuario_id == usuario_id,                 #solo los movimientos de este usuario
        models.Movimiento.tipo == "gasto",                          #solo gastos, no ingresos
        extract("year", models.Movimiento.fecha) == fecha.year,     #solo del mismo año que 'fecha'
        extract("month", models.Movimiento.fecha) == fecha.month,   #solo del mismo mes que 'fecha'
    )
    #si excluir_id no es nulo, se quita ese movimiento de la suma (caso: se esta editando ese gasto)
    if excluir_id is not None:
        consulta = consulta.filter(models.Movimiento.id != excluir_id)
    #devuelve el total gastado en el mes, como número con 2 decimales.
    return round(float(consulta.scalar() or 0), 2)

#funcion que lee el limite mensual guardado dentro del propio usuario (no necesita consultar la base de datos)
def limite_del_usuario(usuario: models.Usuario):
    #límite mensual del usuario como float. Si no tiene límite configurado (None), devuelve None
    return float(usuario.limite_mensual) if usuario.limite_mensual is not None else None

# =========================================================================================
# [H1, H2, H6, H10] Datos de contexto y visibilidad del estado financiero
# - H1 (Visibilidad del estado): calcula 'disponible' y 'gastado_mes' en tiempo real.
# - H2 (Mundo real): maneja cifras en moneda oficial (Bs) y mes legible ("Octubre 2026").
# - H6 (Reconocer antes que recordar): entrega el presupuesto activo para que el modal
#   muestre disponible y gastado sin obligar al usuario a memorizar cifras.
# - H10 (Ayuda y documentación): provee el mes del cómputo para los textos de ayuda.
# =========================================================================================
def resumen_limite(db: Session, usuario: models.Usuario) -> dict:
    hoy = date.today()                                  #fecha de hoy, para trabajar con el mes actual
    limite = limite_del_usuario(usuario)                #cuanto puede gastar en el mes (o None si no tiene limite)
    gastado = gastos_del_mes(db, usuario.id, hoy)       #cuanto lleva gastado este mes
    return {
        "limite": limite,
        "gastado_mes": gastado,
        #lo que le queda por gastar; si no tiene limite, no se puede calcular y queda en None
        "disponible": round(limite - gastado, 2) if limite is not None else None,
        #nombre del mes actual,(se resta 1 porque la lista empieza en 0)
        "mes": f"{MESES[hoy.month - 1]} {hoy.year}",
    }

# endpoint GET /limite: devuelve el resumen del limite mensual del usuario que inicio sesion (H1, H2, H6)
@router.get("", response_model=schemas.LimiteMensualOut)
def obtener_limite(
    db: Session = Depends(get_db),                          #abre la conexion a la base de datos
    usuario: models.Usuario = Depends(get_current_user)     #obtiene el usuario que inicio sesion
):
    return resumen_limite(db, usuario)

# =========================================================================================
# [H5 - Prevención de errores] Guardar o modificar el límite mensual
# Valida con reglas de negocio que el límite sea mayor a 0 y no sea menor a lo ya gastado.
# =========================================================================================
@router.put("", response_model=schemas.LimiteMensualOut)
def definir_limite(
    datos: schemas.LimiteMensualIn,                         #el limite nuevo que envia el frontend
    db: Session = Depends(get_db),                          #abre la conexion a la base de datos
    usuario: models.Usuario = Depends(get_current_user)     #obtiene el usuario que inicio sesion
):

    if usuario.es_demo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Modo demo: no se puede cambiar el límite mensual."
        )

    gastado = gastos_del_mes(db, usuario.id, date.today())
    #revisa que el limite sea valido 
    motivo = validar_limite_mensual(datos.limite, gastado)
    #si hay un motivo de rechazo, responde con error 400 y el mensaje
    if motivo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=motivo)

    #convierte el limite a numero, lo redondea a 2 decimales y lo guarda en el usuario
    usuario.limite_mensual = round(convertir_limite(datos.limite), 2)
    db.commit()             #guarda el cambio en la base de datos
    db.refresh(usuario)     #vuelve a leer el usuario para tener los datos actualizados
    #devuelve el resumen ya con el limite nuevo
    return resumen_limite(db, usuario)

# =========================================================================================
# [H3 - CUMPLE] Sub-issue #10: Control y libertad del usuario (Salida de emergencia)
# SE AUMENTÓ ESTE ENDPOINT: Permite al estudiante eliminar o resetear su límite mensual
# asignando usuario.limite_mensual = None, devolviendo al usuario a su estado sin restricción.
# =========================================================================================
@router.delete("", response_model=schemas.LimiteMensualOut)
def eliminar_limite(
    db: Session = Depends(get_db),                          #abre la conexion a la base de datos
    usuario: models.Usuario = Depends(get_current_user)     #obtiene el usuario que inicio sesion
):
    if usuario.es_demo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Modo demo: no se puede cambiar el límite mensual."
        )

    usuario.limite_mensual = None
    db.commit()             #guarda el cambio en la base de datos
    db.refresh(usuario)     #vuelve a leer el usuario para confirmar
    return resumen_limite(db, usuario)
