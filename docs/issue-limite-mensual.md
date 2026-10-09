# Issue: ¿El límite mensual es válido?

> **Título sugerido para GitHub:** `[Feature] Regla de negocio: Validar límite de gasto mensual`  
> **Etiquetas (Labels):** `enhancement`, `regla-negocio`, `IHC-Clase-14`  
> **Asignada:** Carmen Jenifer Aranibar Fernandez  

---

## Historia de usuario

**Como** estudiante universitario,  
**quiero** definir un límite de gasto mensual en mi presupuesto,  
**para** controlar mis finanzas personales y evitar gastar más del dinero que tengo disponible.

---

## Criterios de aceptación

- [x] **Monto positivo:** El límite ingresado debe ser un número estrictamente mayor a 0 (rechaza valores negativos, cero o vacíos).
- [x] **Consistencia con gastos actuales:** El límite mensual no puede ser menor a la suma de los gastos que ya se realizaron en el mes actual.
- [x] **Respeto del saldo disponible:** El límite no puede exceder el saldo máximo disponible del estudiante (700.00 Bs).
- [x] **Rechazo controlado:** Si el límite no cumple cualquiera de estas condiciones, el sistema lo rechaza (`False`) sin alterar el presupuesto actual.

---

## Detalles técnicos y comprobación (IHC Clase 14)

### 1. Qué resultado se espera
Una función pura, aislada de la interfaz gráfica, que reciba el límite propuesto y retorne `True` si es válido o `False` si debe ser rechazado.

### 2. Dónde se encuentra la regla en el código
* **Backend (Python):** `PRESUPUESTO ESTUDIANTIL/BACKEND/reglas_presupuesto.py` → función `es_limite_mensual_valido()`.
* **Frontend (JavaScript):** `PRESUPUESTO ESTUDIANTIL/FRONTEND/src/utils/reglasPresupuesto.js` → función `esLimiteMensualValido()`.

### 3. Cómo se comprobará (Pruebas Unitarias)
Archivo de pruebas: `PRESUPUESTO ESTUDIANTIL/BACKEND/tests/test_limite_mensual.py`

* **Caso permitido:**
  * Límite de `500.00 Bs` con `70.00 Bs` de gastos y `700.00 Bs` de saldo → Retorna `True`.
* **Casos rechazados:**
  * Límite de `0.00 Bs` o `-50.00 Bs` (cero o negativo) → Retorna `False`.
  * Límite de `50.00 Bs` cuando ya gastó `70.00 Bs` → Retorna `False`.
  * Límite de `1200.00 Bs` superando los `700.00 Bs` de saldo → Retorna `False`.
  * Entradas nulas o de texto inválido (`None`, `"abc"`) → Retorna `False`.

### 4. Comando para ejecutar las pruebas
```bash
python -m pytest -v tests/test_limite_mensual.py -p no:warnings
```
**Resultado:** `5 passed in 0.05s` (100% aprobado).

---

## Cuándo puede cerrarse este Issue
Este issue se considera completado y listo para cerrarse cuando:
1. La regla de validación esté implementada y separada de la interfaz.
2. Todos los casos de prueba (permitidos y rechazados) pasen exitosamente con Pytest.
3. Se haya realizado el commit correspondiente en el repositorio.

