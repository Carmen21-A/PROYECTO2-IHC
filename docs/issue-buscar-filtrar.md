# Issue #2: Buscar y filtrar movimientos

> **Asignada:** Carmen Jenifer Aranibar Fernandez
> **Issue del docente:** #2 (no se cierra; lo cierra el docente tras la revisión)

---

## Historia de usuario

**Como** estudiante,
**quiero** buscar y filtrar mis movimientos,
**para** entender en qué gasto mi dinero.

---

## Sub-issues

| Sub-issue | Criterios del #2 que cubre | Commit |
|---|---|---|
| #6 · Búsqueda y filtros (regla y pruebas) | 1, 2, 3, 4, 5, 6 y 10 | `feat: busqueda y filtros combinables de movimientos con pruebas (closes #6)` |
| #7 · Consulta en la API | 7, la relación con el #1 y el saldo | `feat: endpoint de filtros con total, categorias iniciales y saldo sin negativos (closes #7)` |
| #8 · Interfaz de filtros | 8 y 9 | `feat: interfaz de busqueda y filtros de movimientos (closes #8)` |

---

## Decisiones tomadas al aclarar el requisito

- **"Concepto" = categoría.** La búsqueda encuentra el texto en la descripción **o** en el nombre de la categoría, sin importar mayúsculas. Por eso "almuerzo" también encuentra "Cena con amigos" (categoría "Comida y Almuerzos").
- **Periodos según la fecha del movimiento:** "este mes" va del día 1 al último día del mes actual, "mes anterior" es el mes completo anterior (en enero, diciembre del año pasado) y el rango incluye las dos fechas.
- **El total separa gastos e ingresos.** Sumarlos juntos no tiene sentido. El total sale de la misma lista que se muestra, así que siempre coincide.
- **Relación con el #1:** "gastos de este mes" (sin filtro de estado) suma pagados y pendientes, igual que el "gastado del mes" del límite. Hay una prueba que lo comprueba (`test_20`).
- **Al recargar** se mantienen los datos (vienen de la base de datos) y también los filtros elegidos (se guardan en la URL).
- **"General"** es el filtro para los movimientos sin categoría.
- **Diseño en la misma pantalla, plegado:** filtrar es otra forma de ver la misma lista, así que no se creó otra pantalla con una segunda tabla. El buscador está siempre a la vista; los selectores aparecen al pulsar "Filtros" (revelación progresiva), y los chips y el total solo cuando hay algún filtro aplicado. Así el límite y las tarjetas de resumen siguen visibles mientras se filtra.
- **Cambios previos necesarios:**
    - El formulario enviaba siempre la categoría "Transporte", que no existe en la base de datos (allí se llama "Transporte y Pasajes"), así que todo quedaba sin categoría. Ahora se elige la categoría en el formulario.
    - Las cuentas normales no podían registrar ingresos, así que el filtro por tipo no servía. Ahora el formulario permite elegir Gasto o Ingreso.
    - Si la base de datos no tiene categorías, el backend carga las de `seed.sql` al iniciar.
    - Las tarjetas "Gastos del Mes" e "Ingresos del Mes" sumaban todos los meses. Ahora cuentan solo el mes actual, así "Gastos del Mes", el "Llevo gastado" del límite y el filtro "Gastos + Este mes" muestran el mismo número.
    - **Saldo sin monto inventado:** antes había 700 Bs fijos en el código que no salían de ningún dato del estudiante, y con el historial el saldo llegaba a -245 Bs. Ahora la app **empieza en 0 Bs**, como una billetera real (Yape): el estudiante registra lo que recibe (mesada, beca) como ingreso. `Saldo = ingresos recibidos - gastos pagados` de todos los meses; lo que sobra un mes sigue disponible el siguiente.
    - **El saldo no puede quedar negativo:** si no hay dinero suficiente, el pago no se realiza y se explica el motivo ("Saldo insuficiente"). Se valida al marcar un gasto como pagado, al crear un gasto ya pagado y al eliminar un ingreso que ya se gastó. Está en `BACKEND/saldo.py` y se prueba en `tests/test_saldo.py`.

---

## Criterios de aceptación → dónde se cumplen en el código

| Criterio | Dónde está | Prueba |
|---|---|---|
| 1. Buscar por descripción o concepto | `BACKEND/filtros_movimientos.py` → `consultar_movimientos()` | `test_07`, `test_08`, `test_16` |
| 2. Filtrar por tipo | `consultar_movimientos()` | `test_09` |
| 3. Filtrar por categoría | `consultar_movimientos()` | `test_10` |
| 4. Filtrar por periodo | `rango_del_periodo()` + `consultar_movimientos()` | `test_01`, `test_02`, `test_03`, `test_12` |
| 5. Filtrar por estado | `consultar_movimientos()` | `test_11` |
| 6. Búsqueda y filtros combinables | Todos los filtros se aplican juntos en la misma consulta | `test_13` |
| 7. Total de lo filtrado, coincide con la lista | `calcular_totales()`; `GET /movimientos/filtrar` en `BACKEND/routers/movimientos.py` | `test_05`, `test_17`, `test_20` |
| 8. La interfaz muestra los filtros activos y permite quitarlos | `FRONTEND/src/views/MovimientosView.vue` → botón "Filtros" con contador, chips "Filtros aplicados" con ✕ y "Quitar todos" | — |
| 9. Mensaje claro si nada coincide | `MovimientosView.vue` → "Ningún movimiento coincide con tu búsqueda" | `test_14`, `test_18` |
| 10. Pruebas unitarias con y sin resultados | `BACKEND/tests/test_filtros_movimientos.py` (20 pruebas, 25 casos) | `test_13` (con resultados), `test_14` y `test_06` (sin resultados) |

Los filtros inválidos (tipo o estado inexistente, rango con fechas al revés) se rechazan con el motivo: `test_04`, `test_19`. Nunca aparecen movimientos de otro usuario: `test_15`.

---

## Flujo de punta a punta

1. **Interfaz:** el estudiante escribe en "Buscar" o elige tipo, categoría, estado o periodo. Los filtros se guardan en la URL.
2. **Consulta:** la página llama a `GET /movimientos/filtrar?q=...&tipo=...`. `crear_filtros()` valida los filtros y `consultar_movimientos()` arma una sola consulta con todos ellos, solo sobre los movimientos del usuario del token.
3. **Base de datos:** devuelve los movimientos que cumplen todo; `calcular_totales()` suma esa misma lista.
4. La tabla muestra la lista, el total, los chips de filtros activos o el mensaje de "sin resultados".
5. Al recargar, la página lee los filtros de la URL y vuelve a consultar.

---

## Cómo ejecutar las pruebas

```bash
cd "PRESUPUESTO ESTUDIANTIL/BACKEND"
python -m pytest -v tests/test_filtros_movimientos.py tests/test_saldo.py -p no:warnings
```
