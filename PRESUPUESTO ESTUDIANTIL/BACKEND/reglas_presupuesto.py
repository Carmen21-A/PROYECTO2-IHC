"""
Módulo de Reglas de Negocio - Presupuesto Estudiantil
IHC Clase 14: Del requisito al código
Regla asignada: ¿El límite mensual es válido?
"""

def es_limite_mensual_valido(limite: float, gastos_mes: float = 0.0, saldo_maximo: float = 700.0) -> bool:
    """
    Determina si un límite de gasto mensual ingresado por el estudiante es válido.
    
    Criterios de aceptación:
    1. Debe ser un valor numérico estrictamente mayor a 0 (rechaza negativos y cero).
    2. No puede ser menor a los gastos ya realizados en el mes actual.
    3. No puede superar el saldo máximo disponible del estudiante (700 Bs).
    
    Retorna True si el límite es válido, False si debe ser rechazado.
    """
    # 1. Validación de tipo y existencia
    if limite is None or not isinstance(limite, (int, float)):
        return False
    
    # 2. Caso rechazado: monto menor o igual a cero
    if limite <= 0:
        return False
        
    # 3. Caso rechazado: límite inferior a los gastos ya comprometidos
    if limite < gastos_mes:
        return False
        
    # 4. Caso rechazado: límite superior al saldo disponible del estudiante
    if limite > saldo_maximo:
        return False
        
    # Caso permitido: cumple todas las condiciones
    return True

