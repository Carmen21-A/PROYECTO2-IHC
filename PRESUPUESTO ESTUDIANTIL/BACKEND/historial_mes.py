"""
Historial del mes - Presupuesto Estudiantil
Issue #12: ¿Qué movimientos tuvo el mes?

Convierte los movimientos guardados en una trayectoria visible por mes:
qué ocurrió, cuándo, con qué categoría y cómo terminó el mes.

- mes_desde_texto(): valida el mes pedido ("AAAA-MM") (regla pura).
- consultar_historial(): movimientos del mes y del usuario, del más reciente al más antiguo.
- agrupar_por_dia(): junta los movimientos por fecha, sin perder el orden (regla pura).
- resumen_del_mes(): ingresos, gastos y balance del mes (regla pura).
"""

from datetime import date
from filtros_movimientos import Filtros, consultar_movimientos

MESES = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")


def mes_desde_texto(texto, hoy: date) -> date:
    """Devuelve el primer día del mes pedido. Sin mes, usa el mes actual. Lanza ValueError si no es válido."""
    if texto is None or not str(texto).strip():
        return hoy.replace(day=1)
    try:
        anio, mes = str(texto).strip().split("-")                           # convierte texto a str, le quita espacios, lo corta por el guión y guarda las 2 partes en anio y mes ("2026-10" -> "2026", "10")
        return date(int(anio), int(mes), 1)
    except ValueError:
        raise ValueError("El mes no es válido. Usa el formato AAAA-MM, por ejemplo 2026-10.")


def consultar_historial(db, usuario_id: int, primer_dia: date):
    """Movimientos del usuario en ese mes, del más reciente al más antiguo.
    Reutiliza la consulta del filtro "este mes" (Issue #2) tomando ese mes como referencia."""
    return consultar_movimientos(db, usuario_id, Filtros(periodo="este_mes"), hoy=primer_dia)


def agrupar_por_dia(movimientos) -> list:
    """movimientos: dicts ya ordenados con 'fecha' (AAAA-MM-DD). Devuelve [{fecha, movimientos}]."""
    dias = []
    for m in movimientos:
        if not dias or dias[-1]["fecha"] != m["fecha"]:                     # si dias está vacía, o si la fecha del último día de la lista es distinta a la fecha de m, entonces...
            dias.append({"fecha": m["fecha"], "movimientos": []})           # agrega a dias un día nuevo con la fecha de m y su lista de movimientos vacía
        dias[-1]["movimientos"].append(m)                                   # al último día de la lista, en su lista de movimientos, agrega m
    return dias


def resumen_del_mes(movimientos) -> dict:
    """Pagados y pendientes, igual que las tarjetas "del Mes" y el límite mensual (#1)."""
    ingresos = round(sum(float(m["monto"]) for m in movimientos if m["tipo"] == "ingreso"), 2)     # por cada m en movimientos, si el tipo de m es "ingreso", toma el monto de m, lo convierte a número con decimales (float), suma todo y redondea a 2 decimales
    gastos = round(sum(float(m["monto"]) for m in movimientos if m["tipo"] == "gasto"), 2)         # por cada m en movimientos, si el tipo de m es "gasto", toma el monto de m, lo convierte a número con decimales (float), suma todo y redondea a 2 decimales
    return {
        "cantidad": len(movimientos),
        "ingresos": ingresos,
        "gastos": gastos,
        "balance": round(ingresos - gastos, 2),
    }


def armar_historial(movimientos, primer_dia: date) -> dict:
    """Respuesta completa del historial: el mes, su resumen y los días con sus movimientos."""
    return {
        "mes": primer_dia.strftime("%Y-%m"),
        "mes_texto": f"{MESES[primer_dia.month - 1]} {primer_dia.year}",
        "resumen": resumen_del_mes(movimientos),
        "dias": agrupar_por_dia(movimientos),
    }
