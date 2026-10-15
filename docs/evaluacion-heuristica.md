# Evaluación Heurística H1–H10 · Tarea 3

* **Materia:** Interacción Humano-Computador (IHC) - Proyecto 2  
* **Estudiante:** Carmen Jenifer Aranibar Fernandez  
* **Aplicación:** Presupuesto Estudiantil  
* **Funcionalidad Evaluada:** Configurar el límite y registrar un gasto  
* **Issue Principal de GitHub:** [#9 - Evaluación heurística H1–H10](https://github.com/Carmen21-A/PROYECTO2-IHC/issues/9)  
* **Sub-issues asociados:**  
  * [#10 - Sub-issue de #9 · H3 Control y libertad: permitir restablecer o quitar el límite mensual](https://github.com/Carmen21-A/PROYECTO2-IHC/issues/10) (Resuelto / Cerrado)  
  * [#11 - Sub-issue de #9 · H9 Recuperación de errores: acción constructiva al superar el límite mensual](https://github.com/Carmen21-A/PROYECTO2-IHC/issues/11) (Resuelto / Cerrado)  

---

## 1. Resumen Ejecutivo de la Evaluación

Se realizó una inspección heurística integral sobre el flujo de **«Configurar el límite mensual y registrar un gasto»** aplicando las 10 Heurísticas de Usabilidad de Jakob Nielsen.  
En la inspección inicial se identificaron 8 heurísticas en estado **Cumple** y 2 en estado **Falla** (H3 y H9), las cuales fueron derivadas a Sub-issues en GitHub y resueltas exitosamente mediante código:

| # | Heurística | Evaluación Inicial | Severidad | Pantalla / Componente | Resolución |
|:-:|:---|:---:|:---:|:---|:---:|
| **H1** | Visibilidad del estado del sistema | **Cumple** | — | Modal de Gasto y Dashboard | Aprobada |
| **H2** | Relación con el mundo real | **Cumple** | — | Panel de Límite y Métricas | Aprobada |
| **H3** | Control y libertad del usuario | **Falla** | 3 (Mayor) | Modal "Límite mensual" | Corregida en Sub-issue #10 |
| **H4** | Consistencia y estándares | **Cumple** | — | Modales, Botones e Inputs | Aprobada |
| **H5** | Prevención de errores | **Cumple** | — | Input Cantidad en Modal Gasto | Aprobada |
| **H6** | Reconocer antes que recordar | **Cumple** | — | Contexto de Límite en Modal | Aprobada |
| **H7** | Flexibilidad y eficiencia de uso | **Cumple** | — | Barra de Búsqueda y Filtros | Aprobada |
| **H8** | Diseño estético y minimalista | **Cumple** | — | Formulario Modal de Gasto | Aprobada |
| **H9** | Reconocer y recuperarse de errores | **Falla** | 2 (Menor) | Alerta de rechazo de gasto | Corregida en Sub-issue #11 |
| **H10** | Ayuda y documentación | **Cumple** | — | Textos contextuales de Límite | Aprobada |

---

## 2. Registro Detallado de las 10 Heurísticas

### H1: Visibilidad del estado del sistema
* **Estado:** **Cumple**
* **Pantalla o flujo:** Modal "Registrar Gasto" (`+ Registrar Movimiento`)
* **Explicación y comprobación:**  
  Al ingresar una cantidad (ej. 25.00 Bs), el modal informa oportunamente el estado financiero en vivo. En la cabecera muestra la insignia destacada `Disponible: 350.00 Bs` y debajo un mensaje reactivo positivo en verde: *«✓ Con este gasto te quedarán 325.00 Bs disponibles.»*. El usuario siempre sabe cuál será el resultado de su acción antes de pulsar guardar.
* **Referencia al código:**  
  * Archivo: [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L432-L450) (Líneas 432–436 y 446–450, elementos de feedback activo dentro del panel contextual)
  ```html
  <!-- /// [H1 - Visibilidad del estado del sistema: disponibilidad en tiempo real] /// -->
  <span :class="['limite-contexto-badge', limiteInfo.disponible > 0 ? 'badge-disp-ok' : 'badge-disp-alerta']">
    Disponible: {{ limiteInfo.disponible.toFixed(2) }} Bs
  </span>
  <!-- /// ========================================================================= /// -->

  ...

  <!-- /// [H1 - Visibilidad del estado del sistema: cálculo del saldo que le quedará] /// -->
  <p v-else-if="cantidadGasto && cantidadGasto > 0 && cantidadGasto <= limiteInfo.disponible" class="aviso-queda-preventivo">
    ✓ Con este gasto te quedarán <strong>{{ (limiteInfo.disponible - cantidadGasto).toFixed(2) }} Bs</strong> disponibles.
  </p>
  <!-- /// =========================================================================== /// -->
  ```
* **Evidencia gráfica:**  
  ![H1 - Visibilidad del estado del sistema](<evidencias/Ehuristica- H1 2026-10-15 000547.png>)

---

### H2: Relación con el mundo real
* **Estado:** **Cumple**
* **Pantalla o flujo:** Tarjeta del Dashboard "Límite mensual de gastos" y métricas principales
* **Explicación y comprobación:**  
  La interfaz utiliza vocabulario natural, cotidiano y comprensible para estudiantes universitarios. Emplea expresiones claras como *"Disponible este mes"*, *"Llevo gastado"*, *"Me queda"*, *"Mi límite"* y la moneda boliviana oficial en *"Bs"*. Evita por completo tecnicismos de programación o bases de datos como `balance_remaining`, `limit_amount` o códigos de estado del servidor.
* **Referencia al código:**  
  * Archivo: [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L65-L80) (Líneas 65–80)
  ```html
  <!-- Panel de límite mensual con vocabulario cotidiano para el estudiante (H2) -->
  <div class="limite-cifras">
    <div>
      <span class="limite-etiqueta">Llevo gastado</span>
      <span class="limite-valor amount-danger">{{ limiteInfo.gastado_mes.toFixed(2) }} Bs</span>
    </div>
    <div>
      <span class="limite-etiqueta">Me queda</span>
      <span :class="['limite-valor', limiteInfo.disponible > 0 ? 'amount-ok' : 'amount-danger']">{{ limiteInfo.disponible.toFixed(2) }} Bs</span>
    </div>
    <div>
      <span class="limite-etiqueta">Mi límite</span>
      <span class="limite-valor amount-navy">{{ limiteInfo.limite.toFixed(2) }} Bs</span>
    </div>
  </div>
  ```
* **Evidencia gráfica:**  
  ![H2 - Relación con el mundo real](<evidencias/Ehuristica- H2  2026-10-15 000911.png>)

---

### H3: Control y libertad del usuario
* **Estado:** **Falla**
* **Pantalla o flujo:** Modal "Límite mensual" (al pulsar `Cambiar límite`)
* **Problema observado (Falla):**  
  Una vez que el estudiante definía un límite mensual (ej. 350.00 Bs), la interfaz no ofrecía ninguna opción o botón para "Quitar límite" o volver al estado inicial sin restricción. El diálogo solo contenía los botones "Cancelar" y "Guardar límite". Si el usuario borraba el número e intentaba guardar en blanco o 0, el formulario lo rechazaba. El estudiante quedaba cautivo bajo una restricción permanente sin salida de emergencia.  
* **Severidad:** **3 (Mayor)**.
* **Referencia al código del fallo:**  
  * Archivo: [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L587-L603) (Líneas 587–603)
  ```html
  <!-- Modal original sin opción para quitar o resetear el límite configurado -->
  <div class="dashboard-modal-actions">
    <button type="button" @click="cerrarModalLimite" class="btn-cancelar-modal">
      Cancelar
    </button>
    <button type="submit" class="btn-guardar-principal" :disabled="guardandoLimite">
      {{ guardandoLimite ? 'Guardando...' : 'Guardar límite' }}
    </button>
  </div>
  ```
* **Evidencia gráfica (Falla):**  
  ![H3 - Control y libertad del usuario (Falla)](<evidencias/Ehuristica- H3-ANTES-FALLA  2026-10-15 001251.png>)

---

### H4: Consistencia y estándares
* **Estado:** **Cumple**
* **Pantalla o flujo:** Modales y controles interactivos en toda la aplicación
* **Explicación y comprobación:**  
  La interfaz sigue estándares visuales y de interacción predecibles. Los botones principales de guardado mantienen el mismo color azul corporativo (`#2563EB`) y bordes redondeados; los botones de salida emplean el mismo estilo secundario gris neutral (`.btn-cancelar-modal`). Las cifras y badges usan una semántica consistente en toda la plataforma: rojo para gastos/bloqueos y verde para disponible/ingresos.
* **Referencia al código:**  
  * Archivo: [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L2626-L2663) (Líneas 2626–2663)
  ```css
  /* Estilos estándar para botones principales y cancelaciones */
  .btn-cancelar-modal {
    background-color: #F1F5F9;
    color: #475569;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  .btn-guardar-principal {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: background-color 0.2s ease;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
  }
  ```
* **Evidencia gráfica:**  
  ![H4 - Consistencia y estándares](<evidencias/Ehuristica- H4  2026-10-15 002429.png>)

---

### H5: Prevención de errores
* **Estado:** **Cumple**
* **Pantalla o flujo:** Campo "Cantidad" en Modal de Registrar Gasto
* **Explicación y comprobación:**  
  El diseño previene proactivamente que ocurra el error antes de que el usuario envíe el formulario. Al ingresar un monto superior al disponible (ej. 5000.00 Bs teniendo 325.00 Bs disponibles), el sistema calcula en vivo y muestra al instante una alerta preventiva en recuadro rojo:  
  *«⚠️ Atención: Esta cantidad supera tu límite disponible por 4675.00 Bs.»*  
  Esto evita que el estudiante pierda tiempo completando descripción, categoría y fecha para luego enterarse de que el formulario será rechazado.
* **Referencia al código:**  
  * **Template HTML (Alerta visual preventiva):** [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L441-L445) (Líneas 441–445)
  ```html
  <!-- /// [H5 - Prevención de errores: advertencia anticipada de exceso al escribir] /// -->
  <p v-if="excesoPreventivoGasto > 0" class="aviso-exceso-preventivo">
    ⚠️ <strong>Atención:</strong> Esta cantidad supera tu límite disponible por <strong>{{ excesoPreventivoGasto.toFixed(2) }} Bs</strong>.
  </p>
  <!-- /// ========================================================================= /// -->
  ```
  * **Lógica Reactiva (Script - Detección en tiempo real):** [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L1189-L1200) (Líneas 1189–1200)
  ```javascript
  // /// [H5 - Prevención de errores: cálculo reactivo de exceso al escribir] ///
  const excesoPreventivoGasto = computed(() => {
    if (tipoGasto.value !== 'gasto' || limiteInfo.value.limite === null || !cantidadGasto.value) return 0
    const diaNum = parseInt(diaGasto.value || 1, 10)
    const diaStr = String(diaNum).padStart(2, '0')
    const mesIdx = mesesDisponibles.indexOf(mesGasto.value) + 1
    const mesStr = String(mesIdx > 0 ? mesIdx : 10).padStart(2, '0')
    const fechaISO = `2026-${mesStr}-${diaStr}`
    const gastado = gastosDelMesDe(fechaISO)
    const total = Number((gastado + Number(cantidadGasto.value)).toFixed(2))
    const limite = Number(limiteInfo.value.limite)
    return total > limite ? Number((total - limite).toFixed(2)) : 0
  })
  // /// ================================================================== ///
  ```
* **Evidencia gráfica:**  
  ![H5 - Prevención de errores](<evidencias/Ehuristica- H5  2026-10-15 002706.png>)

---

### H6: Reconocer antes que recordar
* **Estado:** **Cumple**
* **Pantalla o flujo:** Contexto financiero dentro del Modal de Gasto
* **Explicación y comprobación:**  
  Al abrir el formulario para registrar un gasto, el fondo oscuro cubre las cifras del dashboard. Para evitar que el estudiante tenga que memorizar o calcular mentalmente cuánto dinero le quedaba en el mes, el propio formulario muestra una tarjeta de contexto visible con el *Disponible*, el *Límite fijado* y lo *Llevas gastado*.
* **Referencia al código:**  
  * Archivo: [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L428-L452) (Líneas 428–452, tarjeta contenedora de contexto financiero)  
  *Nota de integración en H6:* Esta tarjeta constituye el bloque integral de **H6** (*Reconocer antes que recordar*). Su función es mantener visible todo el estado presupuestario en el modal para que el usuario no dependa de su memoria. Dentro de esta misma tarjeta conviven de manera sinérgica **H1** (visibilidad en tiempo real mediante el badge de disponible y el cálculo de saldo restante) y **H5** (prevención de errores con alerta en rojo al escribir), logrando un componente de asistencia completa en una sola vista.
  ```html
  <!-- /// [H6 - Reconocer antes que recordar: contexto financiero visible en el modal] /// -->
  <div v-if="tipoGasto === 'gasto' && limiteInfo.limite !== null" class="limite-contexto-modal" role="status" aria-live="polite">
    <div class="limite-contexto-cabecera">
      <span class="limite-contexto-label">Presupuesto del mes:</span>
      <!-- /// [H1 - Visibilidad del estado del sistema: disponibilidad en tiempo real] /// -->
      <span :class="['limite-contexto-badge', limiteInfo.disponible > 0 ? 'badge-disp-ok' : 'badge-disp-alerta']">
        Disponible: {{ limiteInfo.disponible.toFixed(2) }} Bs
      </span>
      <!-- /// ========================================================================= /// -->
    </div>
    <div class="limite-contexto-detalle">
      <span>Límite fijado: {{ limiteInfo.limite.toFixed(2) }} Bs · Llevas gastado: {{ limiteInfo.gastado_mes.toFixed(2) }} Bs</span>
    </div>
    <!-- /// [H5 - Prevención de errores: advertencia anticipada de exceso al escribir] /// -->
    <p v-if="excesoPreventivoGasto > 0" class="aviso-exceso-preventivo">
      ⚠️ <strong>Atención:</strong> Esta cantidad supera tu límite disponible por <strong>{{ excesoPreventivoGasto.toFixed(2) }} Bs</strong>.
    </p>
    <!-- /// ========================================================================= /// -->
    <!-- /// [H1 - Visibilidad del estado del sistema: cálculo del saldo que le quedará] /// -->
    <p v-else-if="cantidadGasto && cantidadGasto > 0 && cantidadGasto <= limiteInfo.disponible" class="aviso-queda-preventivo">
      ✓ Con este gasto te quedarán <strong>{{ (limiteInfo.disponible - cantidadGasto).toFixed(2) }} Bs</strong> disponibles.
    </p>
    <!-- /// =========================================================================== /// -->
  </div>
  <!-- /// ============================================================================== /// -->
  ```
* **Evidencia gráfica:**  
  ![H6 - Reconocer antes que recordar](<evidencias/Ehuristica- H6 2026-10-15 003210.png>)

---

### H7: Flexibilidad y eficiencia de uso
* **Estado:** **Cumple**
* **Pantalla o flujo:** Barra de Búsqueda instantánea y Filtros combinables
* **Explicación y comprobación:**  
  La interfaz proporciona atajos y aceleradores de interacción para usuarios frecuentes. Permite filtrar al vuelo movimientos al tipear términos clave (ej. *"salida"*) combinados con filtros desplegables por tipo (*Gastos*), mostrando chips interactivos con botón rápido para eliminar filtros individuales o *"Quitar todos"*, sin necesidad de recargar la página.
* **Referencia al código:**  
  * Archivo: [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L98-L212) (Líneas 98–212, barra de acciones, panel de filtros, chips y totalizadores)
  ```html
  <!-- /// [H7 - Flexibilidad y eficiencia de uso: barra de búsqueda y filtros combinables] /// -->
  <!-- Barra de acciones: buscador + botón de filtros + registrar (Issue #2) -->
  <div :class="['actions-bar', { 'actions-bar-filtros': !esDemo }]">
    <template v-if="!esDemo">
      <div class="buscador">
        <svg class="buscador-icono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="11" cy="11" r="7"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <label for="filtro-q" class="solo-lector">Buscar movimientos</label>
        <input id="filtro-q" v-model="filtros.q" type="search" class="filtro-input buscador-input" placeholder="Buscar por descripción o categoría" />
      </div>
      <button
        type="button"
        :class="['btn-filtros', { 'btn-filtros-activo': mostrarFiltros || cantidadFiltrosPanel }]"
        :aria-expanded="mostrarFiltros"
        aria-controls="panel-filtros"
        @click="mostrarFiltros = !mostrarFiltros"
      >
        Filtros
        <span v-if="cantidadFiltrosPanel" class="contador-filtros" :aria-label="`${cantidadFiltrosPanel} activos`">{{ cantidadFiltrosPanel }}</span>
        <span aria-hidden="true">{{ mostrarFiltros ? '▴' : '▾' }}</span>
      </button>
    </template>
    <button
      @click="abrirModal = true"
      class="btn-new-mov"
      :disabled="esDemo"
      :title="esDemo ? 'No disponible en modo demo' : ''"
    >
      <span class="plus-icon">+</span> Registrar Movimiento
    </button>
  </div>

  <div v-if="avisoEstado" class="aviso-estado" role="alert">{{ avisoEstado }}</div>

  <!-- Filtros (Issue #2): los selectores solo se ven al pulsar "Filtros"; los chips y el total, solo si hay filtros -->
  <section
    v-if="!esDemo && (mostrarFiltros || hayFiltrosActivos || errorFiltro)"
    class="filtros-card"
    aria-label="Filtros de movimientos"
  >
    <div v-if="mostrarFiltros" id="panel-filtros" class="filtros-grid">
      <div class="filtro-campo">
        <label for="filtro-tipo" class="filtro-label">Tipo</label>
        <select id="filtro-tipo" v-model="filtros.tipo" class="filtro-input">
          <option value="">Todos</option>
          <option value="gasto">Gastos</option>
          <option value="ingreso">Ingresos</option>
        </select>
      </div>
      <div class="filtro-campo">
        <label for="filtro-categoria" class="filtro-label">Categoría</label>
        <select id="filtro-categoria" v-model="filtros.categoria" class="filtro-input">
          <option value="">Todas</option>
          <option v-for="cat in categoriasDelFiltro" :key="cat.id" :value="cat.nombre">{{ cat.nombre }}</option>
          <option value="General">General (sin categoría)</option>
        </select>
      </div>
      <div class="filtro-campo">
        <label for="filtro-estado" class="filtro-label">Estado</label>
        <select id="filtro-estado" v-model="filtros.estado" class="filtro-input">
          <option value="">Todos</option>
          <option value="pendiente">Pendiente</option>
          <option value="pagado">Pagado</option>
        </select>
      </div>
      <div class="filtro-campo">
        <label for="filtro-periodo" class="filtro-label">Periodo</label>
        <select id="filtro-periodo" v-model="filtros.periodo" class="filtro-input">
          <option value="todos">Todo el tiempo</option>
          <option value="este_mes">Este mes</option>
          <option value="mes_anterior">Mes anterior</option>
          <option value="rango">Rango de fechas</option>
        </select>
      </div>
      <template v-if="filtros.periodo === 'rango'">
        <div class="filtro-campo">
          <label for="filtro-desde" class="filtro-label">Desde</label>
          <input id="filtro-desde" v-model="filtros.desde" type="date" class="filtro-input" />
        </div>
        <div class="filtro-campo">
          <label for="filtro-hasta" class="filtro-label">Hasta</label>
          <input id="filtro-hasta" v-model="filtros.hasta" type="date" class="filtro-input" />
        </div>
      </template>
    </div>

    <p v-if="mostrarFiltros && avisoRangoIncompleto" class="filtro-aviso">Elige la fecha "desde" y la fecha "hasta" para aplicar el rango.</p>
    <p v-if="errorFiltro" class="form-error-custom" role="alert">{{ errorFiltro }}</p>

    <div v-if="hayFiltrosActivos" class="filtros-activos">
      <span class="filtro-label">Filtros aplicados:</span>
      <button
        v-for="chip in chipsFiltros"
        :key="chip.clave"
        type="button"
        class="chip-filtro"
        :aria-label="`Quitar filtro ${chip.texto}`"
        @click="quitarFiltro(chip.clave)"
      >
        {{ chip.texto }} <span aria-hidden="true">✕</span>
      </button>
      <button type="button" class="btn-quitar-filtros" @click="quitarTodosLosFiltros">Quitar todos</button>
    </div>

    <p v-if="hayFiltrosActivos" class="filtro-total" aria-live="polite">
      <template v-if="cargandoFiltro">Buscando...</template>
      <template v-else>
        {{ totalesVisibles.cantidad }} {{ totalesVisibles.cantidad === 1 ? 'movimiento' : 'movimientos' }}
        · Gastos: <strong class="amount-danger">{{ totalesVisibles.total_gastos.toFixed(2) }} Bs</strong>
        · Ingresos: <strong class="amount-ok">{{ totalesVisibles.total_ingresos.toFixed(2) }} Bs</strong>
      </template>
    </p>
  </section>
  <!-- /// ================================================================================= /// -->
  ```
* **Evidencia gráfica:**  
  ![H7 - Flexibilidad y eficiencia de uso](<evidencias/Ehuristica- H7 2026-10-15 005718.png>)

---

### H8: Diseño estético y minimalista
* **Estado:** **Cumple**
* **Pantalla o flujo:** Formulario Modal de Registrar Gasto
* **Explicación y comprobación:**  
  El diseño visual contiene únicamente los elementos indispensables para registrar la transacción (tipo, cantidad, descripción, categoría, día y mes). Cuenta con una distribución aireada, buen contraste visual, tipografía clara y ausencia total de campos o información irrelevante que compita por la atención del usuario.
* **Referencia al código:**  
  * Archivo: [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L454-L547) (Líneas 454–547)  
  *Nota de integración en H8:* El formulario reúne únicamente la información indispensable (tipo, monto, descripción, categoría y fecha) respetando la sobriedad visual y la ergonomía del estudiante. Dentro de este mismo formulario se incrusta de forma armónica la caja de alerta de **H9** (líneas 527–536); de este modo, cuando el servidor rechaza un gasto por exceder el límite, el mensaje explicativo y el botón de recuperación «💡 Ajustar monto al disponible» aparecen en el propio flujo sin alterar el orden ni abrir molestas ventanas emergentes o modales anidados.
  ```html
  <!-- /// [H8 - Diseño estético y minimalista: formulario enfocado en campos indispensables] /// -->
  <form @submit.prevent="guardarGastoEstudiantil" class="dashboard-form">
    <!-- Tipo de movimiento (Issue #2: permite registrar ingresos para poder filtrarlos) -->
    <div class="form-grupo-custom">
      <span class="form-label-custom">Tipo:</span>
      <div class="type-selector" role="group" aria-label="Tipo de movimiento">
        <button type="button" :class="['btn-type', tipoGasto === 'gasto' ? 'active-gasto' : '']" :aria-pressed="tipoGasto === 'gasto'" @click="tipoGasto = 'gasto'">Gasto</button>
        <button type="button" :class="['btn-type', tipoGasto === 'ingreso' ? 'active-ingreso' : '']" :aria-pressed="tipoGasto === 'ingreso'" @click="tipoGasto = 'ingreso'">Ingreso</button>
      </div>
    </div>

    <!-- Campo Cantidad -->
    <div class="form-grupo-custom">
      <label class="form-label-custom">Cantidad:</label>
      <div class="input-moneda-wrapper">
        <span class="prefijo-bs">Bs</span>
        <input
          v-model.number="cantidadGasto"
          type="number"
          step="any"
          min="0.01"
          placeholder="25"
          required
          class="form-input-custom input-cantidad"
        />
      </div>
    </div>

    <!-- Campo Descripción -->
    <div class="form-grupo-custom">
      <label class="form-label-custom">Descripción:</label>
      <input
        v-model="descripcionGasto"
        type="text"
        :placeholder="tipoGasto === 'ingreso' ? 'Beca de octubre' : 'Almuerzo'"
        required
        class="form-input-custom"
      />
    </div>

    <!-- Campo Categoría -->
    <div class="form-grupo-custom">
      <label class="form-label-custom" for="categoria-gasto">Categoría:</label>
      <select id="categoria-gasto" v-model="categoriaGasto" class="form-input-custom select-mes-custom" required>
        <option v-for="cat in categoriasDelFormulario" :key="cat.id" :value="cat.nombre">{{ cat.nombre }}</option>
      </select>
    </div>

    <!-- Fila Día y Mes -->
    <div class="form-fila-fecha">
      <div class="form-grupo-custom col-fecha-dia">
        <label class="form-label-custom">Día:</label>
        <input
          v-model.number="diaGasto"
          type="number"
          min="1"
          max="31"
          placeholder="1"
          required
          class="form-input-custom text-center"
        />
      </div>

      <div class="form-grupo-custom col-fecha-mes">
        <label class="form-label-custom">Mes:</label>
        <select v-model="mesGasto" class="form-input-custom select-mes-custom" required>
          <option v-for="m in mesesDisponibles" :key="m" :value="m">
            {{ m }}
          </option>
        </select>
      </div>
    </div>

    <!-- /// [H9 - Reconocer, diagnosticar y recuperarse de errores: acción constructiva] /// -->
    <div v-if="errorMsgGasto" class="form-error-custom caja-error-recuperable" role="alert">
      <p class="texto-error-bloqueo">{{ errorMsgGasto }}</p>
      <div v-if="limiteInfo.disponible !== null && limiteInfo.disponible > 0 && Number(cantidadGasto) > limiteInfo.disponible" class="acciones-recuperacion-error">
        <button type="button" class="btn-recuperar-disponible" @click="ajustarMontoAlDisponible">
          💡 Ajustar monto a {{ limiteInfo.disponible.toFixed(2) }} Bs disponibles
        </button>
      </div>
    </div>
    <!-- /// =========================================================================== /// -->

    <div class="dashboard-modal-actions">
      <button type="button" @click="cerrarModalGasto" class="btn-cancelar-modal">
        Cancelar
      </button>
      <button type="submit" class="btn-guardar-principal" :disabled="guardandoGasto">
        {{ guardandoGasto ? 'Guardando...' : 'Guardar' }}
      </button>
    </div>
  </form>
  <!-- /// ================================================================================= /// -->
  ```
* **Evidencia gráfica:**  
  ![H8 - Diseño estético y minimalista](<evidencias/Ehuristica- H8  2026-10-15 005909.png>)

---

### H9: Reconocer, diagnosticar y recuperarse de errores
* **Estado:** **Falla**
* **Pantalla o flujo:** Mensaje de error al rechazar el guardado de gasto que supera el límite
* **Problema observado (Falla):**  
  Cuando el usuario intentaba guardar un gasto que superaba el límite configurado (ej. 555.00 Bs con un disponible de 325.00 Bs), el sistema bloqueaba la acción y mostraba un mensaje en rojo:  
  *«Gasto bloqueado: con 555.00 Bs tus gastos del mes llegarían a 580.00 Bs y superarían tu límite de 350.00 Bs. Solo te quedan 325.00 Bs disponibles este mes.»*  
  Si bien el mensaje diagnosticaba con precisión el problema, dejaba al estudiante sin una salida constructiva directa dentro del diálogo, obligándolo a borrar el campo manualmente o a cancelar todo el formulario.  
* **Severidad:** **2 (Menor)**.
* **Referencia al código del fallo:**  
  * **Código original del fallo (Evaluación inicial):**  
    El componente solo contenía un párrafo pasivo de texto sin ningún mecanismo de acción constructiva:
    ```html
    <!-- Fallo original: Alerta pasiva sin botón de recuperación o ajuste -->
    <div v-if="errorMsgGasto" class="form-error-custom" role="alert">
      <p>{{ errorMsgGasto }}</p>
    </div>
    ```
  * **Ubicación en el código actual:** [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L527-L536) (Líneas 527–536)  
    *(Nota: Al consultar estas líneas en el archivo actualmente, verás que ya contienen la solución implementada en el Sub-issue #11 con la clase `.caja-error-recuperable` y el botón interactivo `ajustarMontoAlDisponible`, tal como se detalla en la Sección 3)*:
    ```html
    <!-- /// [H9 - Reconocer, diagnosticar y recuperarse de errores: acción constructiva] /// -->
    <div v-if="errorMsgGasto" class="form-error-custom caja-error-recuperable" role="alert">
      <p class="texto-error-bloqueo">{{ errorMsgGasto }}</p>
      <div v-if="limiteInfo.disponible !== null && limiteInfo.disponible > 0 && Number(cantidadGasto) > limiteInfo.disponible" class="acciones-recuperacion-error">
        <button type="button" class="btn-recuperar-disponible" @click="ajustarMontoAlDisponible">
          💡 Ajustar monto a {{ limiteInfo.disponible.toFixed(2) }} Bs disponibles
        </button>
      </div>
    </div>
    <!-- /// =========================================================================== /// -->
    ```
* **Evidencia gráfica (Falla):**  
  ![H9 - Reconocer, diagnosticar y recuperarse de errores (Falla)](<evidencias/Ehuristica- H9-ANTES-FALLA 2026-10-15 003956.png>)

---

### H10: Ayuda y documentación
* **Estado:** **Cumple**
* **Pantalla o flujo:** Tarjeta del Dashboard "Límite mensual de gastos"
* **Explicación y comprobación:**  
  La ayuda es breve, proactiva y está ubicada exactamente donde se toma la decisión. Debajo del título de la tarjeta se indica explícitamente: *«Octubre 2026 · cuenta gastos pagados y pendientes del mes»*, aclarando qué transacciones se computan. Además, debajo de la barra de progreso se muestra el cálculo orientativo del porcentaje consumido: *«Usaste el 7% de tu límite.»*.
* **Referencia al código:**  
  * Archivo: [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L52-L54) (Líneas 52–54) y [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L91-L93) (Líneas 91–93)
  ```html
  <!-- Ayuda contextual visible de inmediato (H10) -->
  <span class="card-subtext">{{ limiteInfo.mes }} · cuenta gastos pagados y pendientes del mes</span>
  ...
  <span class="card-subtext">Usaste el {{ porcentajeLimite }}% de tu límite.</span>
  ```
* **Evidencia gráfica:**  
  ![H10 - Ayuda y documentación](<evidencias/Ehuristica- H10  2026-10-15 010029.png>)

---

## 3. Cierre y Trazabilidad de Sub-issues

De acuerdo con lo requerido en la consigna de la Tarea 3:

### Sub-issue #10 (H3 - Control y libertad del usuario)
* **Estado:** **Cerrado / Resuelto**.
* **Heurística asociada:** H3 (Control y libertad del usuario) — Severidad 3 corregida.
* **Resultado:** Se implementó la opción «Quitar límite» y el endpoint backend `DELETE /limite`, verificado con captura del antes (`Ehuristica- H3-ANTES-FALLA`) y después (`Ehuristica- H3-ANTES-CUMPLE`).
* **Solución implementada:**  
  Se incorporó el botón secundario **«Quitar límite»** en el modal de configuración de límite cuando ya existe un valor fijado. Al pulsarlo, el sistema ejecuta una petición `DELETE /limite` que restablece `usuario.limite_mensual = None` en la base de datos y devuelve la tarjeta al estado inicial *"Aún no definiste un límite"*, otorgando una salida de emergencia limpia y autonomía total al usuario.
* **Código corregido implementado:**
  * **Frontend Template:** [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L588-L598) (Líneas 588–598)
  ```html
  <!-- Botón de Quitar límite para dar salida de emergencia y autonomía (H3) -->
  <button
    v-if="limiteInfo.limite !== null"
    type="button"
    class="btn-quitar-limite"
    :disabled="guardandoLimite || quitandoLimite"
    @click="quitarLimite"
  >
    {{ quitandoLimite ? 'Quitando...' : 'Quitar límite' }}
  </button>
  ```
  * **Frontend Lógica reactiva:** [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L939-L963) (Líneas 939–963)
  ```javascript
  // H3: Permite restablecer o eliminar el límite mensual
  async function quitarLimite() {
    quitandoLimite.value = true
    errorLimite.value = ''
    try {
      const res = await fetch(`${API_URL}/limite`, {
        method: 'DELETE',
        headers: authHeaders()
      })
      if (res.status === 401) return sesionExpirada()
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        errorLimite.value = data.detail || 'No se pudo quitar el límite.'
        return
      }
      limiteInfo.value = await res.json()
      cerrarModalLimite()
      mostrarAvisoEstado('Se eliminó tu límite mensual. Ahora puedes gastar sin restricción.')
    } catch (e) {
      errorLimite.value = 'No se pudo conectar con el servidor para quitar el límite.'
    } finally {
      quitandoLimite.value = false
    }
  }
  ```
  * **Frontend Estilos Scoped:** [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L2742-L2760) (Líneas 2742–2760)
  ```css
  /* H3: Botón para quitar el límite mensual */
  .btn-quitar-limite {
    background-color: #FEE2E2;
    color: #B91C1C;
    border: 1px solid #FCA5A5;
    border-radius: 8px;
    padding: 9px 14px;
    font-size: 13.5px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-right: auto;
  }
  .btn-quitar-limite:hover:not(:disabled) {
    background-color: #FECACA;
    color: #991B1B;
  }
  ```
  * **Backend Endpoint DELETE /limite:** [`routers/limite.py`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/BACKEND/routers/limite.py#L102-L122) (Líneas 102–122)
  ```python
  # =========================================================================================
  # [H3 - CUMPLE] Sub-issue #10: Control y libertad del usuario (Salida de emergencia)
  # SE AUMENTÓ ESTE ENDPOINT: Permite al estudiante eliminar o resetear su límite mensual
  # asignando usuario.limite_mensual = None, devolviendo al usuario a su estado sin restricción.
  # =========================================================================================
  @router.delete("", response_model=schemas.LimiteMensualOut)
  def eliminar_limite(
      db: Session = Depends(get_db),                          #abre la conexion a la base de datos
      usuario: models.Usuario = Depends(get_current_user)     #obtiene el usuario que inicio sesion
  ):
      if usuario.es_demo:
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="Modo demo: no se puede cambiar el límite mensual."
          )

      usuario.limite_mensual = None
      db.commit()             #guarda el cambio en la base de datos
      db.refresh(usuario)     #vuelve a leer el usuario para confirmar
      return resumen_limite(db, usuario)
  ```
* **Evidencias gráficas (Antes vs Después):**  
  * **Antes (Falla):**  
    ![H3 Antes (Falla)](<evidencias/Ehuristica- H3-ANTES-FALLA  2026-10-15 001251.png>)  
  * **Después (Imagen 1 - Ya cumple / Corregido):**  
    ![H3 Después - Ya cumple (Imagen 1)](<evidencias/Ehuristica- H3-ANTES-CUMPLE 2026-10-15 023326.png>)

---

### Sub-issue #11 (H9 - Reconocer, diagnosticar y recuperarse de errores)
* **Estado:** **Cerrado / Resuelto**.
* **Heurística asociada:** H9 (Reconocer, diagnosticar y recuperarse de errores) — Severidad 2 corregida.
* **Resultado:** Se incorporó el botón de recuperación «💡 Ajustar monto a 325.00 Bs disponibles», verificado con captura del antes (`Ehuristica- H9-ANTES-FALLA`) y después (`Ehuristica- H9-ANTES-CUMPLE`).
* **Solución implementada:**  
  Se implementó una caja de error recuperable (`.caja-error-recuperable`) que ofrece el botón constructivo **«💡 Ajustar monto a 325.00 Bs disponibles»**. Al pulsar dicho botón, el sistema asigna de forma inmediata el valor disponible exacto a la casilla de cantidad (`cantidadGasto`), permitiendo al usuario continuar y guardar su registro con un único clic sin necesidad de realizar cálculos mentales ni descartar el formulario.
* **Código corregido implementado:**
  * **Frontend Template:** [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L527-L536) (Líneas 527–536)
  ```html
  <!-- Alerta de rechazo con acción de recuperación constructiva (H9) -->
  <div v-if="errorMsgGasto" class="form-error-custom caja-error-recuperable" role="alert">
    <p class="texto-error-bloqueo">{{ errorMsgGasto }}</p>
    <div v-if="limiteInfo.disponible !== null && limiteInfo.disponible > 0 && Number(cantidadGasto) > limiteInfo.disponible" class="acciones-recuperacion-error">
      <button type="button" class="btn-recuperar-disponible" @click="ajustarMontoAlDisponible">
        💡 Ajustar monto a {{ limiteInfo.disponible.toFixed(2) }} Bs disponibles
      </button>
    </div>
  </div>
  ```
  * **Frontend Lógica reactiva:** [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L965-L972) (Líneas 965–972)
  ```javascript
  // H9: Ajuste constructivo en 1 clic al disponible restante
  function ajustarMontoAlDisponible() {
    if (limiteInfo.value.disponible !== null && limiteInfo.value.disponible > 0) {
      cantidadGasto.value = Number(limiteInfo.value.disponible.toFixed(2))
      errorMsgGasto.value = ''
    }
  }
  ```
  * **Frontend Estilos Scoped:** [`MovimientosView.vue`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue#L2762-L2798) (Líneas 2762–2798)
  ```css
  /* H9: Acción constructiva de recuperación de errores */
  .caja-error-recuperable {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .texto-error-bloqueo {
    margin: 0;
    line-height: 1.4;
  }
  .acciones-recuperacion-error {
    display: flex;
    align-items: center;
    margin-top: 2px;
  }
  .btn-recuperar-disponible {
    background-color: #FFFFFF;
    color: #B91C1C;
    border: 1.5px solid #F87171;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }
  .btn-recuperar-disponible:hover {
    background-color: #FEF2F2;
    border-color: #DC2626;
    color: #991B1B;
  }
  ```
  * **Backend Validación y diagnóstico para recuperación:** [`reglas_presupuesto.py`](file:///c:/Users/HP/Pictures/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/BACKEND/reglas_presupuesto.py#L64-L89) (Líneas 64–89)
  ```python
  # =========================================================================================
  # [H5 y H9 - Prevención de errores y Diagnóstico para Recuperación]
  # - H5 (Prevención): Bloquea gastos que rebasen el límite establecido antes de persistir.
  # - H9 (Diagnóstico preciso): Comunica con exactitud el total al que se llegaría,
  #   el límite configurado y el monto 'disponible' exacto restante (ej. 325.00 Bs),
  #   permitiendo que el Frontend ofrezca el botón constructivo de ajuste en 1 clic.
  # =========================================================================================
  def validar_gasto_con_limite(monto: float, gastos_mes: float, limite):
      """
      Un gasto nuevo no puede hacer que el total del mes supere el límite.
      Si el estudiante no definió límite (None), el gasto se permite.

      Retorna None si el gasto está permitido, o el motivo del bloqueo.
      """
      if limite is None:
          return None
      total = round(gastos_mes + monto, 2)
      if total > round(limite, 2):
          disponible = max(round(limite - gastos_mes, 2), 0)                #SI DA NEGATIVO DEJALO EN 0
          return (
              f"Gasto bloqueado: con {monto:.2f} Bs tus gastos del mes llegarían a "
              f"{total:.2f} Bs y superarían tu límite de {limite:.2f} Bs. "
              f"Solo te quedan {disponible:.2f} Bs disponibles este mes."
          )
      return None
  ```
* **Evidencias gráficas (Antes vs Después):**  
  * **Antes (Falla):**  
    ![H9 Antes (Falla)](<evidencias/Ehuristica- H9-ANTES-FALLA 2026-10-15 003956.png>)  
  * **Después (Imagen 2 - Ya corregido):**  
    ![H9 Después - Ya corregido (Imagen 2)](<evidencias/Ehuristica- H9-ANTES-CUMPLE 2026-10-15 024042.png>)

---

**Conclusión Final:** Las 10 heurísticas de Jakob Nielsen se encuentran completamente documentadas. Las dos heurísticas que inicialmente fallaban (H3 y H9) fueron resueltas exitosamente mediante código frontend y backend verificado en los Sub-issues #10 y #11, logrando que el flujo de «Configurar límite y registrar gasto» cumpla el 100% de los estándares de usabilidad.
