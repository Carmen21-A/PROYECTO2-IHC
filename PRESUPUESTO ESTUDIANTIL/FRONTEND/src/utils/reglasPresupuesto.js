/**
 * Módulo de Reglas de Negocio - Presupuesto Estudiantil
 * IHC Clase 14: Del requisito al código
 * Regla: ¿El límite mensual es válido?
 */

/**
 * Valida si el límite mensual ingresado por el estudiante es válido.
 * 
 * @param {number} limite - Monto del límite mensual a establecer.
 * @param {number} gastosMes - Monto de gastos ya acumulados en el mes (por defecto 0).
 * @param {number} saldoMaximo - Saldo base disponible (por defecto 700 Bs).
 * @returns {boolean} true si es válido (caso permitido), false si no (caso rechazado).
 */
export function esLimiteMensualValido(limite, gastosMes = 0, saldoMaximo = 700) {
  // 1. Debe ser un número válido
  if (typeof limite !== 'number' || isNaN(limite)) {
    return false;
  }

  // 2. No puede ser 0 ni negativo
  if (limite <= 0) {
    return false;
  }

  // 3. No puede ser menor a los gastos ya realizados en el mes
  if (limite < gastosMes) {
    return false;
  }

  // 4. No puede superar el saldo máximo disponible (700 Bs)
  if (limite > saldoMaximo) {
    return false;
  }

  return true;
}

