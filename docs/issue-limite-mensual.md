# Issue #1: Validar el límite mensual de gastos

> **Asignada:** Carmen Jenifer Aranibar Fernandez
> **Issue del docente:** #1 (no se cierra; lo cierra el docente tras la revisión)

---

## Historia de usuario

**Como** estudiante,
**quiero** definir un límite mensual de gastos,
**para** saber cuánto puedo gastar y no pasarme.

---

## Sub-issues

| Sub-issue | Criterios del #1 que cubre | Commit |
|---|---|---|
| #3 · Regla | 1, 2, 3, 4 y 8 | `feat: regla de limite mensual y bloqueo de gastos con pruebas (closes #3)` |
| #4 · Persistencia | 6 y 7 | `feat: guardar limite mensual por usuario en la base de datos (closes #4)` |
| #5 · Interfaz | 5 | `feat: panel de limite mensual en la interfaz (closes #5)` |

---

## Decisiones tomadas al aclarar el requisito

- **¿Qué cuenta como "gastado en el mes"?** Todos los gastos con fecha del mes, **pagados y pendientes**. Un gasto pendiente ya es dinero comprometido; si solo contaran los pagados, un gasto nuevo (que nace pendiente) nunca podría bloquearse.
- **¿El límite puede ser igual a lo gastado?** Sí. Se rechaza solo si es **menor**.
- **¿Llegar justo al límite está permitido?** Sí. Se bloquea solo si el total lo **supera**.
- **Sin límite definido** no se bloquea ningún gasto.
- Se quitó el tope fijo de 700 Bs de la versión anterior: no era parte del requisito y no consideraba los ingresos.

---

## Criterios de aceptación → dónde se cumplen en el código

| Criterio | Dónde está | Prueba |
|---|---|---|
| Puedo definir un límite mensual mayor a 0 | `BACKEND/routers/limite.py` → `PUT /limite` | `test_01`, `test_10` |
| Vacío, 0, negativo o con letras se rechaza | `BACKEND/reglas_presupuesto.py` → `validar_limite_mensual()` | `test_03`, `test_04`, `test_11` |
| No puede ser menor que lo ya gastado en el mes | `validar_limite_mensual()` + `gastos_del_mes()` | `test_06`, `test_12` |
| Un gasto que supera el límite se bloquea y explica el motivo | `validar_gasto_con_limite()`; se aplica en `POST /movimientos` y `PUT /movimientos/{id}` (`verificar_limite_mensual()` en `routers/movimientos.py`) → HTTP 409 con el motivo | `test_08`, `test_14`, `test_15` |
| La interfaz muestra cuánto llevo gastado y cuánto me queda | `FRONTEND/src/views/MovimientosView.vue` → panel "Límite mensual de gastos" (`GET /limite`) | `test_13` |
| Cada usuario ve y cambia solo su propio límite | `/limite` no recibe id de usuario: usa el del token (`get_current_user`) | `test_16` |
| Se guarda en la base de datos y se mantiene al recargar | Columna `usuarios.limite_mensual` (`models.py`, `schema.sql`, migración en `main.py`) | `test_10` |
| Pruebas unitarias: un caso permitido y uno rechazado | `BACKEND/tests/test_limite_mensual.py` (16 pruebas, 26 casos) | — |

---

## Flujo de punta a punta

1. **Interfaz:** el estudiante pulsa "Definir límite" y escribe un monto. `reglasPresupuesto.js` (la misma regla en JS) avisa al instante si no es válido.
2. **Regla:** el backend vuelve a validar con `validar_limite_mensual()` — es quien decide.
3. **Base de datos:** si es válido se guarda en `usuarios.limite_mensual`.
4. Al registrar o editar un gasto, el backend suma los gastos del mes (`gastos_del_mes()`) y aplica `validar_gasto_con_limite()`. Si lo supera responde **409** con el motivo, el gasto **no se guarda** y la interfaz muestra el mensaje en el formulario.
5. Al recargar, la página pide `GET /limite` y muestra el límite guardado, lo gastado y lo que queda.

---

## Cómo ejecutar las pruebas

```bash
cd "PRESUPUESTO ESTUDIANTIL/BACKEND"
python -m pytest -v tests/test_limite_mensual.py -p no:warnings
```
