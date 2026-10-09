# Issues del Proyecto - Presupuesto Estudiantil

Registro de Issues y unidades de trabajo del proyecto (IHC).

---

## Issue: ¿El límite mensual es válido?

> **Título en GitHub:** `[Feature] Regla de negocio: Validar límite de gasto mensual`  
> **Etiquetas:** `enhancement`, `regla-negocio`, `IHC-Clase-14`  

### Historia de usuario

**Como** estudiante universitario,  
**quiero** definir un límite de gasto mensual en mi presupuesto,  
**para** controlar mis finanzas personales y evitar gastar más del dinero que tengo disponible.

### Criterios de aceptación

- [x] **Monto positivo:** El límite ingresado debe ser un número estrictamente mayor a 0 (rechaza valores negativos, cero o vacíos).
- [x] **Consistencia con gastos actuales:** El límite mensual no puede ser menor a la suma de los gastos que ya se realizaron en el mes actual.
- [x] **Respeto del saldo disponible:** El límite no puede exceder el saldo máximo disponible del estudiante (700.00 Bs).
- [x] **Rechazo controlado:** Si el límite no cumple cualquiera de estas condiciones, el sistema lo rechaza (`False`) sin alterar el presupuesto actual.

---

### Verificación Técnica y Pruebas Unitarias

* **Regla en código:** `PRESUPUESTO ESTUDIANTIL/BACKEND/reglas_presupuesto.py`
* **Pruebas:** `PRESUPUESTO ESTUDIANTIL/BACKEND/tests/test_limite_mensual.py`

Comando de verificación:
```bash
python -m pytest -v tests/test_limite_mensual.py -p no:warnings
```
Resultado: **5 passed in 0.05s**.

