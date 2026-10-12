"""
Búsqueda y filtros de movimientos - Presupuesto Estudiantil
Issue #2: Buscar y filtrar movimientos

- crear_filtros(): valida lo que eligió el estudiante (regla pura).
- rango_del_periodo(): convierte "este mes", "mes anterior" o un rango en fechas (regla pura).
- consultar_movimientos(): aplica todos los filtros juntos en la consulta a la base de datos.
- calcular_totales(): suma lo que quedó en la lista filtrada (regla pura).
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional
from sqlalchemy import or_
import models

TIPOS = ("ingreso", "gasto")
ESTADOS = ("pendiente", "pagado")
PERIODOS = ("todos", "este_mes", "mes_anterior", "rango")
SIN_CATEGORIA = "General"


@dataclass
class Filtros:
    texto: str = ""
    tipo: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None
    periodo: str = "todos"
    desde: Optional[date] = None
    hasta: Optional[date] = None


def _limpiar(valor):
    if valor is None:
        return None
    valor = str(valor).strip()
    return valor or None


def _fecha(valor, nombre):
    try:
        return date.fromisoformat(valor)
    except (TypeError, ValueError):
        raise ValueError(f"La fecha '{nombre}' no es válida. Usa el formato AAAA-MM-DD.")


def crear_filtros(texto=None, tipo=None, categoria=None, estado=None,
                  periodo=None, desde=None, hasta=None) -> Filtros:
    """Valida los filtros elegidos. Lanza ValueError con el motivo si alguno no es válido."""
    tipo, estado, categoria = _limpiar(tipo), _limpiar(estado), _limpiar(categoria)
    periodo = _limpiar(periodo) or "todos"

    if tipo and tipo not in TIPOS:
        raise ValueError("El tipo debe ser 'ingreso' o 'gasto'.")
    if estado and estado not in ESTADOS:
        raise ValueError("El estado debe ser 'pendiente' o 'pagado'.")
    if periodo not in PERIODOS:
        raise ValueError("El periodo debe ser 'todos', 'este_mes', 'mes_anterior' o 'rango'.")

    filtros = Filtros(texto=_limpiar(texto) or "", tipo=tipo, categoria=categoria,
                      estado=estado, periodo=periodo)
    if periodo == "rango":
        if not _limpiar(desde) or not _limpiar(hasta):
            raise ValueError("Para filtrar por rango elige la fecha 'desde' y la fecha 'hasta'.")
        filtros.desde = _fecha(_limpiar(desde), "desde")
        filtros.hasta = _fecha(_limpiar(hasta), "hasta")
        if filtros.desde > filtros.hasta:
            raise ValueError("La fecha 'desde' no puede ser posterior a la fecha 'hasta'.")
    return filtros


def rango_del_periodo(filtros: Filtros, hoy: date):
    """Devuelve (inicio, fin) del periodo, ambos incluidos, o (None, None) si es 'todos'."""
    if filtros.periodo == "este_mes":
        inicio = hoy.replace(day=1)
        fin = (inicio.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        return inicio, fin
    if filtros.periodo == "mes_anterior":
        fin = hoy.replace(day=1) - timedelta(days=1)
        return fin.replace(day=1), fin
    if filtros.periodo == "rango":
        return filtros.desde, filtros.hasta
    return None, None


def consultar_movimientos(db, usuario_id: int, filtros: Filtros, hoy: date = None):
    """Movimientos del usuario que cumplen TODOS los filtros a la vez, del más reciente al más antiguo."""
    hoy = hoy or date.today()
    consulta = db.query(models.Movimiento).outerjoin(
        models.Categoria, models.Movimiento.categoria_id == models.Categoria.id
    ).filter(models.Movimiento.usuario_id == usuario_id)

    if filtros.texto:
        patron = "%" + filtros.texto.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        consulta = consulta.filter(or_(
            models.Movimiento.descripcion.ilike(patron, escape="\\"),
            models.Categoria.nombre.ilike(patron, escape="\\"),
        ))
    if filtros.tipo:
        consulta = consulta.filter(models.Movimiento.tipo == filtros.tipo)
    if filtros.estado:
        consulta = consulta.filter(models.Movimiento.estado == filtros.estado)
    if filtros.categoria:
        if filtros.categoria == SIN_CATEGORIA:
            consulta = consulta.filter(models.Movimiento.categoria_id.is_(None))
        else:
            consulta = consulta.filter(models.Categoria.nombre == filtros.categoria)

    inicio, fin = rango_del_periodo(filtros, hoy)
    if inicio:
        consulta = consulta.filter(models.Movimiento.fecha >= inicio, models.Movimiento.fecha <= fin)

    return consulta.order_by(models.Movimiento.fecha.desc(), models.Movimiento.id.desc()).all()


def calcular_totales(movimientos) -> dict:
    """Totales de la lista filtrada: lo que se suma es exactamente lo que se ve."""
    ingresos = sum(float(m["monto"]) for m in movimientos if m["tipo"] == "ingreso")
    gastos = sum(float(m["monto"]) for m in movimientos if m["tipo"] == "gasto")
    return {
        "cantidad": len(movimientos),
        "total_ingresos": round(ingresos, 2),
        "total_gastos": round(gastos, 2),
    }
