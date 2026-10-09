# Actividad Clase 14: Del requisito al código - Presupuesto Estudiantil

**Proyecto:** Presupuesto Estudiantil  
**Cuestionante Asignada:** ¿El límite mensual es válido?  
**Materia:** Interacción Hombre Computador (IHC)  

---

## 1. Analizar (Historia de Usuario y Criterios)

### Historia de usuario
> Como estudiante universitario, quiero definir un límite de gasto mensual para controlar mi presupuesto y evitar gastar más del dinero que tengo disponible.

### Criterios de aceptación
- [ ] El límite debe ser un valor numérico estrictamente mayor a 0 (no se permiten montos cero ni negativos).
- [ ] El límite no puede ser menor a los gastos ya realizados en el mes actual.
- [ ] El límite no puede superar el saldo máximo disponible del estudiante (700 Bs).
- [ ] Si el límite no cumple las reglas, el sistema lo rechaza y no actualiza el presupuesto.

---

## 2. Issue para GitHub (Formato oficial)

```markdown
## Historia de usuario
Como estudiante universitario, quiero definir un límite de gasto mensual para controlar mi presupuesto y evitar gastar más del dinero que tengo disponible.

## Criterios de aceptación
- [ ] El límite debe ser un número estrictamente mayor a 0.
- [ ] El límite no puede ser menor a los gastos ya acumulados en el mes.
- [ ] El límite no puede superar el saldo máximo disponible (700 Bs).
- [ ] Los valores inválidos se rechazan sin alterar el presupuesto actual.
```

---

## 3. Implementación de la Regla (Separada de la interfaz)

Archivo: `PRESUPUESTO ESTUDIANTIL/BACKEND/reglas_presupuesto.py`

```python
def es_limite_mensual_valido(limite: float, gastos_mes: float = 0.0, saldo_maximo: float = 700.0) -> bool:
    if limite is None or not isinstance(limite, (int, float)):
        return False
    if limite <= 0:
        return False
    if limite < gastos_mes:
        return False
    if limite > saldo_maximo:
        return False
    return True
```

---

## 4. Pruebas Unitarias Automatizadas

Archivo: `PRESUPUESTO ESTUDIANTIL/BACKEND/tests/test_limite_mensual.py`

* **Caso permitido:** Límite de 500 Bs con gastos de 70 Bs y saldo de 700 Bs → `True`.
* **Caso rechazado 1:** Límite de 0 Bs o negativo (-50 Bs) → `False`.
* **Caso rechazado 2:** Límite de 50 Bs cuando ya se gastaron 70 Bs → `False`.
* **Caso rechazado 3:** Límite de 1200 Bs que supera el saldo de 700 Bs → `False`.
* **Caso rechazado 4:** Valor nulo o texto no numérico → `False`.

Comando para ejecutar:
```bash
python -m pytest -v tests/test_limite_mensual.py -p no:warnings
```
Resultado: **5 passed** (100%).

