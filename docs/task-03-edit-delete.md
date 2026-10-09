# Tarea 3 - Completar el ciclo del elemento

**Aplicación Asignada:** Presupuesto Estudiantil  
**Estudiante:** Carmen Jenifer Aranibar Fernandez  
**Materia:** Interacción Hombre Computador (IHC) - Proyecto 2  

---

## 1. Qué se implementó

Sobre el flujo principal (registrar gasto → marcar como pagado) se agregó:

1. **Editar** un movimiento: cantidad, descripción y fecha (día y mes).
2. **Eliminar** un movimiento, **pidiendo confirmación** antes de borrarlo.
3. **Restricción según el estado:** un movimiento **pagado no permite modificar su monto**.

| Estado del gasto | Editar descripción / fecha | Editar monto | Eliminar |
|------------------|:--------------------------:|:------------:|:--------:|
| Pendiente        | Sí                         | Sí           | Sí (con confirmación) |
| Pagado           | Sí                         | **No (bloqueado)** | Sí (con confirmación) |

---

## 2. Backend (FastAPI + PostgreSQL)

Archivo: `PRESUPUESTO ESTUDIANTIL/BACKEND/routers/movimientos.py`

| Método | Ruta | Qué hace |
|--------|------|----------|
| `PUT`    | `/movimientos/{id}` | Edita descripción, monto y/o fecha. Guarda con `db.commit()`. |
| `DELETE` | `/movimientos/{id}` | Elimina el movimiento de la base de datos. |

* Ambos verifican que el movimiento pertenezca al usuario autenticado (si no, **404**) y bloquean la cuenta demo (**403**).
* **Regla de estado** (`validar_edicion`): si el movimiento está `pagado` y se envía un monto distinto al actual, se rechaza con **HTTP 409 Conflict** y el mensaje:
  > *"No se puede modificar el monto: este movimiento ya está pagado. Solo puedes cambiar la descripción y la fecha."*
* Esquema nuevo `MovimientoUpdate` en `schemas.py` (todos los campos opcionales).
* `BASE DE DATOS/schema.sql` ahora incluye la columna `estado` (`pendiente` / `pagado`).

---

## 3. Frontend (Vue 3) — decisiones de IHC

Archivo: `PRESUPUESTO ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue`

* **Botones con texto** "Editar" y "Eliminar" en la columna ACCIONES (no solo íconos), con `aria-label` que incluye la descripción del gasto.
* **Modal de edición** con los mismos campos que el registro y el estado actual visible.
  * Si el gasto está **pagado**, el campo *Cantidad* aparece **deshabilitado** y debajo se muestra el motivo:
    > 🔒 Este gasto ya está **pagado**, por eso su monto no se puede modificar. Puedes cambiar la descripción y la fecha.
  * Si el servidor rechaza un cambio, se muestra el mensaje exacto que explica el motivo.
* **Modal de confirmación** para eliminar, que muestra la descripción, el monto y la fecha del gasto y advierte que la acción no se puede deshacer. El botón destructivo es rojo y "Cancelar" está siempre disponible.
* Tras guardar o eliminar se muestra un aviso breve de confirmación.

---

## 4. Persistencia

Los cambios se guardan en la base de datos (PostgreSQL, o SQLite si no hay credenciales). Al cargar la página, la lista se obtiene siempre del servidor, por lo que **las ediciones y eliminaciones se mantienen después de recargar (F5)**.

---

## 5. Pruebas unitarias

Archivo: `PRESUPUESTO ESTUDIANTIL/BACKEND/tests/test_editar_eliminar_movimiento.py`  
(los fixtures compartidos están en `tests/conftest.py`)

| # | Prueba | Qué verifica |
|---|--------|--------------|
| 1 | `test_01_pagado_rechaza_cambio_de_monto` | Cambiar el monto de un gasto pagado responde 409 con el mensaje del motivo y el monto en BD no cambia. |
| 2 | `test_02_regla_validar_edicion_bloquea_monto_pagado` | La regla aislada bloquea el monto de un pagado y permite el de un pendiente. |
| 3 | `test_03_pagado_permite_editar_descripcion_y_fecha` | Un gasto pagado sí permite cambiar descripción y fecha. |
| 4 | `test_04_pendiente_permite_editar_monto` | Un gasto pendiente sí permite cambiar el monto. |
| 5 | `test_05_eliminar_movimiento` | Eliminar borra el registro de la BD (y un segundo intento da 404). |

### Comando

```bash
cd "PRESUPUESTO ESTUDIANTIL/BACKEND"
python -m pytest -v tests -p no:warnings
```

Resultado: **9 passed** (4 pruebas de la Tarea 2 + 5 de la Tarea 3).
