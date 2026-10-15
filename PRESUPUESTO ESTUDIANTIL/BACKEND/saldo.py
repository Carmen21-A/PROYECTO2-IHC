"""
Saldo disponible - Presupuesto Estudiantil

La aplicación empieza en 0 Bs: el estudiante registra lo que recibe (mesada, beca,
sueldo) como ingreso y lo que gasta como gasto. Como en una billetera real:

    Saldo disponible = ingresos recibidos - gastos pagados   (de todos los meses)

Un ingreso pendiente todavía no llegó y un gasto pendiente todavía no salió,
por eso ninguno de los dos mueve el saldo.

Regla: el saldo no puede quedar negativo. Si no hay dinero suficiente,
el pago no se realiza y se explica el motivo.
"""

from datetime import date
from sqlalchemy import func, case
import models


def calcular_resumen(movimientos, hoy: date) -> dict:
    """movimientos: lista de dicts con 'tipo', 'monto', 'estado' y 'fecha' (date)."""
    def suma(condicion):
        return round(sum(float(m["monto"]) for m in movimientos if condicion(m)), 2)            #Por m en la lista de movimiento, si cumple la condicion  de m, entonces el monto de m, se convierte a decimal, se suma todo, y se redondea a 2 decimales

    def del_mes(m):
        return m["fecha"].year == hoy.year and m["fecha"].month == hoy.month                     #DEVUELVE TRUE

    recibidos = suma(lambda m: m["tipo"] == "ingreso" and m["estado"] == "pagado")                 #Recibidos es igual a la suma de los movimientos donde el tipo sea ingreso y el estado sea pagado
    pagados = suma(lambda m: m["tipo"] == "gasto" and m["estado"] == "pagado")
    return {
        "saldo_disponible": round(recibidos - pagados, 2),
        # Del mes: pagados y pendientes, igual que el límite (#1) y el filtro "este mes" (#2)
        "ingresos_del_mes": suma(lambda m: m["tipo"] == "ingreso" and del_mes(m)),
        "gastos_del_mes": suma(lambda m: m["tipo"] == "gasto" and del_mes(m)),
    }


def validar_pago_con_saldo(monto: float, saldo: float):
    """Retorna None si el pago está permitido, o el motivo si dejaría el saldo en negativo."""
    if round(saldo - monto, 2) < 0:
        disponible = max(round(saldo, 2), 0)
        return (
            f"Saldo insuficiente: este pago es de {monto:.2f} Bs y solo tienes "
            f"{disponible:.2f} Bs disponibles. Registra un ingreso o espera a recibirlo para pagar."
        )
    return None


def validar_quitar_ingreso(monto: float, saldo: float):
    """Quitar un ingreso ya recibido no puede dejar el saldo en negativo."""
    if round(saldo - monto, 2) < 0:
        return (
            f"No se puede eliminar este ingreso: ya usaste parte de ese dinero en gastos pagados "
            f"y tu saldo quedaría en {saldo - monto:.2f} Bs."
        )
    return None


def saldo_actual(db, usuario_id: int, excluir_id: int = None) -> float:
    """Saldo del usuario calculado en la base de datos."""
    signo = case((models.Movimiento.tipo == "ingreso", models.Movimiento.monto), else_=-models.Movimiento.monto)    #Si el movimiento es tipo ingreso, monto positivo, si es gasto monto con signo  negativo
    consulta = db.query(func.coalesce(func.sum(signo), 0)).filter(                                                    #Consulta la BD , suma todos los montos con signo "-" , si no hay se pone 0, pero solo los: 
        models.Movimiento.usuario_id == usuario_id,
        models.Movimiento.estado == "pagado",
    )
    if excluir_id is not None:
        consulta = consulta.filter(models.Movimiento.id != excluir_id)
    return round(float(consulta.scalar() or 0), 2)



# filtra y quita el movimiento con ese ID de la consulta. Después, 
#retorna el resultado, si es NONE pon 0, como decimal redondeado a 2 decimales 