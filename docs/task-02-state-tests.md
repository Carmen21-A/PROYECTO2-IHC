# Tarea 2 - Máquina de Estados y Pruebas Unitarias

**Aplicación Asignada:** Presupuesto Estudiantil  
**Estudiante:** Carmen Jenifer Aranibar Fernandez  
**Materia:** Interacción Hombre Computador (IHC) - Proyecto 2  
**Modalidad:** P2 (con IA)  

---

## 1. Definición de la Regla de Estado

Siguiendo las especificaciones de la **Tarea 2** para el proyecto **Presupuesto Estudiantil**:

* **Entidad / Elemento:** Movimiento (Gasto universitario)
* **Estado inicial:** `Pendiente` (gasto programado o por pagar)
* **Estado final:** `Pagado` (gasto efectivamente liquidado)
* **Nombre de la acción:** `"Marcar como pagado"`

```
  ┌───────────────────────────────────────────────────────────────┐
  │                                                               │
  │   [ + Registrar Movimiento ]                                  │
  │               │                                               │
  │               ▼                                               │
  │     ┌───────────────────┐                                     │
  │     │ Estado Inicial:   │                                     │
  │     │  🟡 PENDIENTE     │                                     │
  │     └─────────┬─────────┘                                     │
  │               │                                               │
  │               │  Acción: "Marcar como pagado" (Botón azul)    │
  │               ▼                                               │
  │     ┌───────────────────┐                                     │
  │     │  🟢 PAGADO        │                                     │
  │     └─────────┬─────────┘                                     │
  │               │                                               │
  │               ▼                                               │
  │        ✓ Completado                                           │
  │   (Reintento rechazado con 400 Bad Request)                   │
  │                                                               │
  └───────────────────────────────────────────────────────────────┘
```

---

## 2. Implementación de la Nueva Funcionalidad (Parte 1)

### 2.1 Backend y Base de Datos (PostgreSQL / FastAPI)
1. **Modelo de Datos (`models.py`):**
   * Se agregó el atributo `estado = Column(String(20), default="pendiente", nullable=False)` a la entidad `Movimiento`.
   * En el inicio de la API (`main.py`), se ejecuta una verificación y migración automática que garantiza que la columna exista en la base de datos PostgreSQL.
2. **Esquemas Pydantic (`schemas.py`):**
   * `MovimientoCreate` y `MovimientoOut` incorporan el campo `estado`, garantizando que todo nuevo movimiento nazca por defecto en `"pendiente"`.
3. **Endpoint de Transición (`routers/movimientos.py`):**
   * Se habilitó el endpoint `PATCH /movimientos/{movimiento_id}/pagar` (también compatible con `PUT`).
   * Valida la existencia del movimiento y la pertenencia al usuario autenticado.
   * **Regla de negocio:** Si el movimiento ya está en estado `"pagado"`, rechaza la solicitud retornando un error **HTTP 400 Bad Request** con el mensaje descriptivo: *"Transición inválida: el movimiento ya se encuentra en estado pagado."*
   * Si es válido, actualiza el estado a `"pagado"` y guarda el cambio de forma permanente en PostgreSQL (`db.commit()`).
4. **Cálculo Financiero:**
   * La métrica *"Gastos del Mes"* suma exclusivamente los movimientos en estado `"pagado"`, reflejando con fidelidad los desembolsos reales del estudiante. Los gastos pendientes quedan reservados sin descontarse del saldo efectivo hasta que se concreten.

### 2.2 Frontend (Vue 3 / IHC)
1. **Estructura de la Tabla (`MovimientosView.vue`):**
   * Se agregó la columna **ESTADO** y se configuró la columna **ACCIONES**.
2. **Diseño Visual y Semántica de Colores (IHC):**
   * **Gasto Pendiente:** 
     * Monto en badge amarillo mostaza (`-25.00 Bs`).
     * Badge de estado amarillo (`Pendiente`).
     * Botón azul estilizado: **`Marcar como pagado`**.
   * **Gasto Pagado:**
     * Monto en badge rojo (`-15.50 Bs`), señalando el gasto ya desembolsado.
     * Badge de estado verde (`Pagado`).
     * Icono checkmark verde discreto (`✓`).
3. **Persistencia Garantizada:**
   * La acción actualiza la interfaz reactivamente y sincroniza con el backend mediante la API REST y el almacenamiento local.
   * **Al recargar la página (F5)**, el estado `"Pagado"` se mantiene conservado y visible.

---

## 3. Pruebas Unitarias Automatizadas (Parte 2)

Las pruebas están implementadas con **Pytest** y **FastAPI TestClient** en el archivo:
`PRESUPUESTO ESTUDIANTIL/BACKEND/tests/test_estado_movimiento.py`

Utilizan una base de datos SQLite en memoria aislada (`sqlite:///:memory:` con `StaticPool`), garantizando ejecución veloz, independiente y reproducible en cualquier entorno.

### Detalle de las 4 Pruebas Obligatorias:

| # | Nombre de la Prueba | Regla Verificada | Resultado |
|---|---------------------|------------------|:---------:|
| 1 | `test_01_estado_inicial_es_correcto` | Al registrar un nuevo gasto, su estado inicial es obligatoriamente `'pendiente'`. | **PASÓ (PASSED)** |
| 2 | `test_02_accion_realiza_transicion_esperada` | Al invocar la acción `"Marcar como pagado"`, el elemento transiciona exitosamente de `'pendiente'` a `'pagado'`. | **PASÓ (PASSED)** |
| 3 | `test_03_transicion_invalida_se_rechaza` | Si un movimiento ya está en `'pagado'`, reintentar la acción es rechazado con error HTTP 400. | **PASÓ (PASSED)** |
| 4 | `test_04_demas_datos_del_elemento_se_conservan` | Tras cambiar a `'pagado'`, el monto, descripción, fecha y usuario_id se mantienen intactos. | **PASÓ (PASSED)** |

---

## 4. Comando para Ejecutar las Pruebas

Para ejecutar las pruebas en la terminal del backend:

```bash
cd "PRESUPUESTO ESTUDIANTIL/BACKEND"
python -m pytest -v tests/test_estado_movimiento.py -p no:warnings
```

### Salida de la Ejecución en Consola:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\HP\Pictures\PROYECTO2-IHC\PRESUPUESTO ESTUDIANTIL\BACKEND
collected 4 items

tests/test_estado_movimiento.py::test_01_estado_inicial_es_correcto PASSED [ 25%]
tests/test_estado_movimiento.py::test_02_accion_realiza_transicion_esperada PASSED [ 50%]
tests/test_estado_movimiento.py::test_03_transicion_invalida_se_rechaza PASSED [ 75%]
tests/test_estado_movimiento.py::test_04_demas_datos_del_elemento_se_conservan PASSED [100%]

============================== 4 passed in 1.09s ===============================
```
---