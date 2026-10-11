/**
 * Módulo de Reglas de Negocio - Presupuesto Estudiantil
 * IHC Clase 14: Del requisito al código
 * Regla: ¿El límite mensual es válido?
 *
 * Es la misma regla que BACKEND/reglas_presupuesto.py. Aquí se usa para avisar
 * al estudiante antes de enviar; el backend vuelve a validar y es quien decide.
 * Cada función devuelve null si está permitido, o el motivo del rechazo.
 */

/** Convierte lo escrito a número; null si está vacío, tiene letras o no es un número. */
export function convertirLimite(valor) {
  if (valor === null || valor === undefined || typeof valor === 'boolean') return null
  if (typeof valor === 'string') {
    const texto = valor.trim().replace(',', '.')
    if (!texto || !/^[+-]?(\d+\.?\d*|\.\d+)$/.test(texto)) return null
    valor = Number(texto)
  }
  if (typeof valor !== 'number' || !Number.isFinite(valor)) return null
  return valor
}

/**
 * @param {number|string} limite - Límite mensual que escribió el estudiante.
 * @param {number} gastosMes - Lo que ya gastó en el mes.
 */
export function validarLimiteMensual(limite, gastosMes = 0) {
  const numero = convertirLimite(limite)
  if (numero === null) return 'El límite debe ser un número. No puede estar vacío ni tener letras.'
  if (numero <= 0) return 'El límite mensual debe ser mayor a 0 Bs.'
  if (Math.round(numero * 100) < Math.round(gastosMes * 100)) {
    return `El límite no puede ser menor que lo que ya gastaste este mes (${gastosMes.toFixed(2)} Bs).`
  }
  return null
}

export function esLimiteMensualValido(limite, gastosMes = 0) {
  return validarLimiteMensual(limite, gastosMes) === null
}

/** Un gasto nuevo no puede hacer que el total del mes supere el límite (null = sin límite). */
export function validarGastoConLimite(monto, gastosMes, limite) {
  if (limite === null || limite === undefined) return null
  const total = Math.round((gastosMes + monto) * 100) / 100
  if (total > limite) {
    const disponible = Math.max(Math.round((limite - gastosMes) * 100) / 100, 0)
    return `Gasto bloqueado: con ${monto.toFixed(2)} Bs tus gastos del mes llegarían a ` +
      `${total.toFixed(2)} Bs y superarían tu límite de ${limite.toFixed(2)} Bs. ` +
      `Solo te quedan ${disponible.toFixed(2)} Bs disponibles este mes.`
  }
  return null
}
