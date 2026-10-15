"""
Módulo de Reglas de Negocio - Presupuesto Estudiantil
IHC Clase 14: Del requisito al código
Regla asignada: ¿El límite mensual es válido?

Las funciones son puras (no tocan la base de datos ni la interfaz): reciben
números y devuelven None si la operación está permitida, o un texto que
explica el motivo del rechazo.
"""

from math import isfinite


def convertir_limite(valor):
    """
    Convierte lo que escribió el estudiante a número.
    Devuelve None si el valor está vacío, tiene letras o no es un número real.
    """
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, str):
        texto = valor.strip().replace(",", ".")                                          #REMPLAZA LA COMA POR PUNTO
        if not texto:
            return None
        try:
            valor = float(texto)
        except ValueError:
            return None
    if not isinstance(valor, (int, float)) or not isfinite(valor):
        return None
    return float(valor)


# =========================================================================================
# [H5 - Prevención de errores] Validación anticipada de reglas de negocio para el límite
# =========================================================================================
def validar_limite_mensual(limite, gastos_mes: float = 0.0):
    """
    Criterios de aceptación:
    1. El límite no puede estar vacío ni tener letras.
    2. Debe ser mayor a 0 (rechaza cero y negativos).
    3. No puede ser menor que lo que ya se gastó en el mes.

    Retorna None si el límite es válido, o el motivo del rechazo.
    """
    numero = convertir_limite(limite)
    if numero is None:
        return "El límite debe ser un número. No puede estar vacío ni tener letras."
    if numero <= 0:
        return "El límite mensual debe ser mayor a 0 Bs."
    if round(numero, 2) < round(gastos_mes, 2):
        return (
            f"El límite no puede ser menor que lo que ya gastaste este mes "
            f"({gastos_mes:.2f} Bs)."                                   #Gastos delmes con 2 decimales al final pon BS
        )
    return None


def es_limite_mensual_valido(limite, gastos_mes: float = 0.0) -> bool:
    """True si el límite es válido (caso permitido), False si se rechaza."""
    return validar_limite_mensual(limite, gastos_mes) is None


# =========================================================================================
# [H5 y H9 - Prevención de errores y Diagnóstico para Recuperación]
# - H5 (Prevención): Bloquea gastos que rebasen el límite establecido antes de persistir.
# - H9 (Diagnóstico preciso): Comunica con exactitud el total al que se llegaría,
#   el límite configurado y el monto 'disponible' exacto restante (ej. 325.00 Bs),
#   permitiendo que el Frontend ofrezca el botón constructivo de ajuste en 1 clic.
# =========================================================================================
def validar_gasto_con_limite(monto: float, gastos_mes: float, limite):
    """
    Un gasto nuevo no puede hacer que el total del mes supere el límite.
    Si el estudiante no definió límite (None), el gasto se permite.

    Retorna None si el gasto está permitido, o el motivo del bloqueo.
    """
    if limite is None:
        return None
    total = round(gastos_mes + monto, 2)
    if total > round(limite, 2):
        disponible = max(round(limite - gastos_mes, 2), 0)                #SI DA NEGATIVO DEJALO EN 0
        return (
            f"Gasto bloqueado: con {monto:.2f} Bs tus gastos del mes llegarían a "
            f"{total:.2f} Bs y superarían tu límite de {limite:.2f} Bs. "
            f"Solo te quedan {disponible:.2f} Bs disponibles este mes."
        )
    return None
