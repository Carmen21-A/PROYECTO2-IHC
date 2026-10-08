<template>
  <div class="movimientos-page">
    <div class="container">

      <div class="dashboard-header">
        <h1 class="page-title">Mis Movimientos</h1>
      </div>

      <div v-if="esDemo" class="demo-banner">
        <strong>Estás viendo una demo</strong> con datos de ejemplo. Para registrar tus propios movimientos,
        <button type="button" class="demo-link" @click="salirDemo">crea tu cuenta gratis</button>.
      </div>

      <div class="summary-cards-grid">

        <div class="summary-card">
          <img :src="iconSaldo" alt="" class="card-icon" />
          <div class="card-info">
            <span class="card-label">Saldo Disponible</span>
            <span class="card-amount amount-navy">{{ esDemo ? `$${saldoTotal.toFixed(2)}` : `${saldoTotal.toFixed(2)} Bs` }}</span>
            <span class="card-subtext">Actualizado hoy</span>
          </div>
        </div>

        <div class="summary-card">
          <img :src="iconIngresos" alt="" class="card-icon" />
          <div class="card-info">
            <span class="card-label">Ingresos del Mes</span>
            <span class="card-amount amount-sky">{{ esDemo ? `$${ingresosTotal.toFixed(2)}` : `${ingresosTotal.toFixed(2)} Bs` }}</span>
            <span class="card-subtext">Octubre 2026</span>
          </div>
        </div>

        <div class="summary-card">
          <img :src="iconGastos" alt="" class="card-icon" />
          <div class="card-info">
            <span class="card-label">Gastos del Mes</span>
            <span class="card-amount amount-danger">{{ esDemo ? `$${gastosTotal.toFixed(2)}` : `${gastosTotal.toFixed(2)} Bs` }}</span>
            <span class="card-subtext">Octubre 2026</span>
          </div>
        </div>

      </div>

      <div class="actions-bar">
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

      <!-- Tarjeta Principal de Movimientos para cuentas de usuario (Docente / IHC) -->
      <div v-if="!esDemo" class="tarjeta-estudiantil-card">
        <table class="tarjeta-estudiantil-table">
          <thead>
            <tr>
              <th class="col-mov-header">MOVIMIENTO</th>
              <th class="col-desc-header">DESCRIPCION</th>
              <th class="col-fecha-header">FECHA</th>
              <th class="col-estado-header text-center">ESTADO</th>
              <th class="col-accion-header text-center">ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="listaMovimientos.length === 0" class="fila-vacia">
              <td colspan="5" class="celda-vacia">
                <div class="estado-vacio">
                  <span class="emoji-vacio">💳</span>
                  <p class="titulo-vacio">No hay movimientos registrados</p>
                  <p class="subtitulo-vacio">Presiona el botón <strong>"+ Registrar Movimiento"</strong> para agregar tu primer gasto.</p>
                </div>
              </td>
            </tr>

            <tr v-for="item in listaMovimientos" :key="item.id" class="fila-movimiento">
              <td class="col-mov-dato">
                <span :class="['badge-movimiento', item.tipo === 'ingreso' ? 'badge-ingreso-bs' : (item.estado === 'pagado' ? 'badge-gasto-bs' : 'badge-pendiente-monto')]">
                  {{ formatearMovimientoTexto(item) }}
                </span>
              </td>
              <td class="col-desc-dato">
                {{ item.descripcion }}
              </td>
              <td class="col-fecha-dato">
                {{ formatearFechaEspanol(item.fecha) }}
              </td>
              <td class="col-estado-dato text-center">
                <span :class="['badge-estado-pill', item.estado === 'pagado' ? 'badge-estado-pagado' : 'badge-estado-pendiente']">
                  {{ item.estado === 'pagado' ? 'Pagado' : 'Pendiente' }}
                </span>
              </td>
              <td class="col-accion-dato text-center">
                <div class="acciones-fila">
                <button
                  v-if="item.estado !== 'pagado'"
                  type="button"
                  class="btn-marcar-pagado"
                  :disabled="actualizandoEstado === item.id"
                  @click="marcarComoPagado(item)"
                  title="Marcar como pagado"
                >
                  <span v-if="actualizandoEstado === item.id">Guardando...</span>
                  <span v-else>Marcar como pagado</span>
                </button>
                <div v-else class="estado-pagado-check" title="Gasto pagado">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
                <button
                  type="button"
                  class="btn-accion btn-editar"
                  @click="abrirEdicion(item)"
                  :aria-label="`Editar ${item.descripcion}`"
                >
                  Editar
                </button>
                <button
                  type="button"
                  class="btn-accion btn-eliminar"
                  @click="pedirConfirmacionEliminar(item)"
                  :aria-label="`Eliminar ${item.descripcion}`"
                >
                  Eliminar
                </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Tabla para la cuenta Demo (intacta) -->
      <div v-else class="table-card">
        <table class="movimientos-table">
          <thead>
            <tr>
              <th class="col-fecha">FECHA</th>
              <th class="col-desc">DESCRIPCIÓN</th>
              <th class="col-cat">CATEGORÍA</th>
              <th class="col-monto text-right">MONTO</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in listaMovimientos" :key="item.id" class="table-row">
              <td class="col-fecha font-date">{{ item.fecha }}</td>
              <td class="col-desc font-desc">{{ item.descripcion }}</td>
              <td class="col-cat">
                <span :class="['cat-badge', badgeClass(item.categoria)]">
                  {{ item.categoria }}
                </span>
              </td>
              <td :class="['col-monto', 'text-right', item.tipo === 'ingreso' ? 'monto-plus' : 'monto-minus']">
                {{ item.tipo === 'ingreso' ? '+' : '-' }}${{ Math.abs(item.monto).toFixed(2) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>

    <!-- Modal en modo Demo (intacto, sin tocar) -->
    <div v-if="abrirModal && esDemo" class="modal-overlay" @click.self="abrirModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Registrar Nuevo Movimiento</h3>
          <button @click="abrirModal = false" class="btn-close-modal">✕</button>
        </div>

        <form @submit.prevent="guardarMovimiento" class="modal-form">
          <div class="form-group">
            <label>Tipo de Movimiento</label>
            <div class="type-selector">
              <button
                type="button"
                :class="['btn-type', nuevoTipo === 'gasto' ? 'active-gasto' : '']"
                @click="nuevoTipo = 'gasto'"
              >
                Gasto
              </button>
              <button
                type="button"
                :class="['btn-type', nuevoTipo === 'ingreso' ? 'active-ingreso' : '']"
                @click="nuevoTipo = 'ingreso'"
              >
                Ingreso
              </button>
            </div>
          </div>

          <div class="form-group">
            <label>Descripción</label>
            <input
              v-model="nuevaDescripcion"
              type="text"
              placeholder="Ej. Almuerzo menú estudiante"
              required
              class="modal-input"
            />
          </div>

          <div class="form-group">
            <label>Categoría</label>
            <select v-model="nuevaCategoria" class="modal-input" required>
              <option v-for="cat in categoriasDelTipo" :key="cat.id" :value="cat.nombre">
                {{ cat.nombre }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Monto ($)</label>
            <input
              v-model.number="nuevoMonto"
              type="number"
              step="0.01"
              min="0.01"
              placeholder="0.00"
              required
              class="modal-input"
            />
          </div>

          <p v-if="errorMsg" class="modal-error">{{ errorMsg }}</p>

          <div class="modal-actions">
            <button type="button" @click="abrirModal = false" class="btn-cancel">Cancelar</button>
            <button type="submit" class="btn-save">Guardar Movimiento</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Dashboard: Registrar Gasto (Para Cuentas Normales) -->
    <div v-if="abrirModal && !esDemo" class="modal-overlay" @click.self="cerrarModalGasto">
      <div class="modal-card dashboard-modal-card">
        <div class="dashboard-modal-header">
          <div class="dashboard-header-left">
            <div class="dashboard-icon-circle">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
            </div>
            <h2 class="dashboard-titulo">Gasto</h2>
          </div>
          <button @click="cerrarModalGasto" class="btn-close-modal" title="Cerrar">✕</button>
        </div>

        <p class="dashboard-subtitulo">Registra los detalles del gasto universitario</p>

        <form @submit.prevent="guardarGastoEstudiantil" class="dashboard-form">
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
              placeholder="Transporte"
              required
              class="form-input-custom"
            />
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

          <p v-if="errorMsgGasto" class="form-error-custom">{{ errorMsgGasto }}</p>

          <div class="dashboard-modal-actions">
            <button type="button" @click="cerrarModalGasto" class="btn-cancelar-modal">
              Cancelar
            </button>
            <button type="submit" class="btn-guardar-principal" :disabled="guardandoGasto">
              {{ guardandoGasto ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal: Editar Movimiento (Tarea 3) -->
    <div v-if="movimientoEditando" class="modal-overlay" @click.self="cerrarEdicion">
      <div class="modal-card dashboard-modal-card">
        <div class="dashboard-modal-header">
          <div class="dashboard-header-left">
            <div class="dashboard-icon-circle icon-editar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20h9"></path>
                <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"></path>
              </svg>
            </div>
            <h2 class="dashboard-titulo">Editar gasto</h2>
          </div>
          <button @click="cerrarEdicion" class="btn-close-modal" title="Cerrar">✕</button>
        </div>

        <p class="dashboard-subtitulo">
          Estado actual:
          <span :class="['badge-estado-pill', movimientoEditando.estado === 'pagado' ? 'badge-estado-pagado' : 'badge-estado-pendiente']">
            {{ movimientoEditando.estado === 'pagado' ? 'Pagado' : 'Pendiente' }}
          </span>
        </p>

        <form @submit.prevent="guardarEdicion" class="dashboard-form">
          <div class="form-grupo-custom">
            <label class="form-label-custom" for="editar-cantidad">Cantidad:</label>
            <div class="input-moneda-wrapper">
              <span class="prefijo-bs">Bs</span>
              <input
                id="editar-cantidad"
                v-model.number="editCantidad"
                type="number"
                step="any"
                min="0.01"
                required
                :disabled="montoBloqueado"
                :aria-describedby="montoBloqueado ? 'motivo-monto-bloqueado' : undefined"
                class="form-input-custom input-cantidad"
              />
            </div>
            <p v-if="montoBloqueado" id="motivo-monto-bloqueado" class="aviso-bloqueo">
              🔒 Este gasto ya está <strong>pagado</strong>, por eso su monto no se puede modificar.
              Puedes cambiar la descripción y la fecha.
            </p>
          </div>

          <div class="form-grupo-custom">
            <label class="form-label-custom" for="editar-descripcion">Descripción:</label>
            <input
              id="editar-descripcion"
              v-model="editDescripcion"
              type="text"
              required
              class="form-input-custom"
            />
          </div>

          <div class="form-fila-fecha">
            <div class="form-grupo-custom col-fecha-dia">
              <label class="form-label-custom" for="editar-dia">Día:</label>
              <input
                id="editar-dia"
                v-model.number="editDia"
                type="number"
                min="1"
                max="31"
                required
                class="form-input-custom text-center"
              />
            </div>
            <div class="form-grupo-custom col-fecha-mes">
              <label class="form-label-custom" for="editar-mes">Mes:</label>
              <select id="editar-mes" v-model="editMes" class="form-input-custom select-mes-custom" required>
                <option v-for="m in mesesDisponibles" :key="m" :value="m">{{ m }}</option>
              </select>
            </div>
          </div>

          <p v-if="errorEdicion" class="form-error-custom" role="alert">{{ errorEdicion }}</p>

          <div class="dashboard-modal-actions">
            <button type="button" @click="cerrarEdicion" class="btn-cancelar-modal">Cancelar</button>
            <button type="submit" class="btn-guardar-principal" :disabled="guardandoEdicion">
              {{ guardandoEdicion ? 'Guardando...' : 'Guardar cambios' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal: Confirmar Eliminación (Tarea 3) -->
    <div v-if="movimientoAEliminar" class="modal-overlay" @click.self="cancelarEliminar">
      <div class="modal-card dashboard-modal-card" role="alertdialog" aria-labelledby="titulo-eliminar" aria-describedby="texto-eliminar">
        <div class="dashboard-modal-header">
          <div class="dashboard-header-left">
            <div class="dashboard-icon-circle">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
                <path d="M10 11v6M14 11v6"></path>
                <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"></path>
              </svg>
            </div>
            <h2 id="titulo-eliminar" class="dashboard-titulo">¿Eliminar gasto?</h2>
          </div>
        </div>

        <p id="texto-eliminar" class="texto-confirmar">
          Vas a eliminar <strong>"{{ movimientoAEliminar.descripcion }}"</strong>
          por <strong>{{ formatearMovimientoTexto(movimientoAEliminar) }}</strong>
          del {{ formatearFechaEspanol(movimientoAEliminar.fecha) }}.
          Esta acción no se puede deshacer.
        </p>

        <p v-if="errorEliminar" class="form-error-custom" role="alert">{{ errorEliminar }}</p>

        <div class="dashboard-modal-actions">
          <button type="button" @click="cancelarEliminar" class="btn-cancelar-modal">Cancelar</button>
          <button type="button" class="btn-confirmar-eliminar" :disabled="eliminando" @click="confirmarEliminar">
            {{ eliminando ? 'Eliminando...' : 'Sí, eliminar' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import iconSaldo from '../assets/icon-saldo.png'
import iconIngresos from '../assets/icon-ingresos.png'
import iconGastos from '../assets/icon-gastos.png'

// =========================================================================
// SALDO BASE CONFIGURABLE:
// Modifica aquí la cantidad (por defecto 700).
// Si cambias este número en el código, se verá reflejado automáticamente
// en el Saldo Disponible y se descontarán los gastos registrados.
// =========================================================================
const SALDO_BASE = 700

const API_URL = 'http://localhost:8000'
const router = useRouter()

const usuarioActual = JSON.parse(localStorage.getItem('usuario') || '{}')
const esDemo = usuarioActual.es_demo === true

// Clave única para guardar los movimientos de cada usuario en localStorage
const storageKey = computed(() => {
  const email = usuarioActual.email || 'estudiante'
  return `movimientos_${email}`
})

function guardarEnStorage(lista) {
  if (!esDemo) {
    try {
      localStorage.setItem(storageKey.value, JSON.stringify(lista))
    } catch (e) {
      console.error('Error al guardar en localStorage:', e)
    }
  }
}

function cargarDeStorage() {
  if (esDemo) return []
  try {
    const data = localStorage.getItem(storageKey.value)
    return data ? JSON.parse(data) : []
  } catch (e) {
    return []
  }
}

function salirDemo() {
  localStorage.removeItem('token')
  localStorage.removeItem('usuario')
  router.push('/registro')
}

const abrirModal = ref(false)
const nuevoTipo = ref('gasto')
const nuevaDescripcion = ref('')
const nuevaCategoria = ref('')
const nuevoMonto = ref(null)
const errorMsg = ref('')

// Inicia de inmediato con los movimientos almacenados localmente para evitar pérdida al recargar
const listaMovimientos = ref(cargarDeStorage())
const categorias = ref([])

// Variables específicas para modo Demo
const saldoDemo = ref(0)
const ingresosDemo = ref(0)
const gastosDemo = ref(0)

// Gastos calculados automáticamente a partir de los movimientos (solo gastos pagados)
const gastosTotal = computed(() => {
  if (esDemo) return gastosDemo.value
  return listaMovimientos.value
    .filter(m => m.tipo === 'gasto' && m.estado === 'pagado')
    .reduce((sum, item) => sum + Number(item.monto || 0), 0)
})

// Ingresos calculados automáticamente a partir de los movimientos
const ingresosTotal = computed(() => {
  if (esDemo) return ingresosDemo.value
  return listaMovimientos.value
    .filter(m => m.tipo === 'ingreso')
    .reduce((sum, item) => sum + Number(item.monto || 0), 0)
})

// Saldo Disponible: SALDO_BASE (700) + Ingresos - Gastos
const saldoTotal = computed(() => {
  if (esDemo) return saldoDemo.value
  return SALDO_BASE + ingresosTotal.value - gastosTotal.value
})

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${localStorage.getItem('token')}`
  }
}

function sesionExpirada() {
  localStorage.removeItem('token')
  localStorage.removeItem('usuario')
  router.push('/login')
}

async function cargarMovimientos() {
  try {
    const res = await fetch(`${API_URL}/movimientos`, { headers: authHeaders() })
    if (res.status === 401) return sesionExpirada()
    if (res.ok) {
      const data = await res.json()
      if (esDemo) {
        listaMovimientos.value = data.movimientos
        saldoDemo.value = data.saldo_disponible
        ingresosDemo.value = data.ingresos_del_mes
        gastosDemo.value = data.gastos_del_mes
      } else {
        // La base de datos es la fuente de verdad: así las ediciones y
        // eliminaciones se mantienen tal cual después de recargar
        listaMovimientos.value = data.movimientos || []
        guardarEnStorage(listaMovimientos.value)
      }
    }
  } catch (e) {
    console.warn('Servidor offline: usando movimientos almacenados localmente.')
  }
}

async function cargarCategorias() {
  try {
    const res = await fetch(`${API_URL}/categorias`)
    if (res.ok) {
      categorias.value = await res.json()
    }
  } catch (e) {
    // Si no hay conexión de categorías, continuar normalmente
  }
}

const categoriasDelTipo = computed(() => {
  return categorias.value.filter(c => c.tipo === nuevoTipo.value)
})

watch(categoriasDelTipo, (lista) => {
  nuevaCategoria.value = lista.length ? lista[0].nombre : ''
})

function badgeClass(cat) {
  if (cat.includes('Comida')) return 'badge-comida'
  if (cat.includes('Transporte')) return 'badge-transporte'
  if (cat.includes('Libros')) return 'badge-libros'
  if (['Ingreso', 'Beca', 'Apoyo', 'Trabajo'].some(p => cat.includes(p))) return 'badge-ingreso'
  return 'badge-comida'
}

async function guardarMovimiento() {
  if (!nuevaDescripcion.value || !nuevoMonto.value) return
  errorMsg.value = ''

  try {
    const res = await fetch(`${API_URL}/movimientos`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify({
        descripcion: nuevaDescripcion.value,
        categoria: nuevaCategoria.value,
        monto: nuevoMonto.value,
        tipo: nuevoTipo.value
      })
    })
    if (res.status === 401) return sesionExpirada()
    if (!res.ok) {
      errorMsg.value = 'No se pudo guardar el movimiento.'
      return
    }

    await cargarMovimientos()

    nuevaDescripcion.value = ''
    nuevoMonto.value = null
    abrirModal.value = false
  } catch (e) {
    errorMsg.value = 'No se pudo conectar con el servidor.'
  }
}

const mesesDisponibles = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

const cantidadGasto = ref(null)
const descripcionGasto = ref('')
const diaGasto = ref(1)
const mesGasto = ref('Octubre')
const guardandoGasto = ref(false)
const errorMsgGasto = ref('')

function cerrarModalGasto() {
  abrirModal.value = false
  errorMsgGasto.value = ''
}

function formatearMovimientoTexto(item) {
  const monto = Number(item.monto || 0)
  const montoTexto = monto.toFixed(2)
  if (item.tipo === 'ingreso') {
    return `+${montoTexto} Bs`
  }
  return `-${montoTexto} Bs`
}

function formatearFechaEspanol(fechaStr) {
  if (!fechaStr) return ''
  if (fechaStr.toLowerCase().includes(' de ')) return fechaStr

  if (fechaStr.includes('-')) {
    const parts = fechaStr.split('-')
    if (parts.length === 3) {
      const dia = parseInt(parts[2], 10)
      const mesNum = parseInt(parts[1], 10)
      const mesNombre = mesesDisponibles[mesNum - 1] || 'Octubre'
      return `${dia} de ${mesNombre}`
    }
  }
  return fechaStr
}

async function guardarGastoEstudiantil() {
  if (!cantidadGasto.value || !descripcionGasto.value) {
    errorMsgGasto.value = 'Por favor completa la cantidad y la descripción.'
    return
  }

  errorMsgGasto.value = ''
  guardandoGasto.value = true

  const diaNum = parseInt(diaGasto.value || 1, 10)
  const diaStr = String(diaNum).padStart(2, '0')
  const mesIdx = mesesDisponibles.indexOf(mesGasto.value) + 1
  const mesStr = String(mesIdx > 0 ? mesIdx : 10).padStart(2, '0')
  const anio = 2026
  const fechaISO = `${anio}-${mesStr}-${diaStr}`

  const nuevoGasto = {
    id: Date.now(),
    descripcion: descripcionGasto.value.trim(),
    categoria: 'Transporte',
    monto: Number(cantidadGasto.value),
    tipo: 'gasto',
    fecha: fechaISO,
    estado: 'pendiente'
  }

  // Se añade de inmediato a la lista y se guarda en localStorage (no se pierde al recargar)
  listaMovimientos.value = [nuevoGasto, ...listaMovimientos.value]
  guardarEnStorage(listaMovimientos.value)

  try {
    const res = await fetch(`${API_URL}/movimientos`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify({
        descripcion: nuevoGasto.descripcion,
        categoria: nuevoGasto.categoria,
        monto: nuevoGasto.monto,
        tipo: nuevoGasto.tipo,
        fecha: nuevoGasto.fecha,
        estado: 'pendiente'
      })
    })

    if (res.status === 401) return sesionExpirada()
    if (res.ok) {
      const data = await res.json()
      nuevoGasto.id = data.id
      nuevoGasto.estado = data.estado || 'pendiente'
      guardarEnStorage(listaMovimientos.value)
      avisarOtrasPestanas('creado', nuevoGasto.descripcion)
      await sincronizarDesdeServidor(`Se registró "${nuevoGasto.descripcion}".`)
    }
  } catch (err) {
    console.warn('Gasto guardado en almacenamiento local (servidor desconectado).')
  } finally {
    guardandoGasto.value = false
    cantidadGasto.value = null
    descripcionGasto.value = ''
    diaGasto.value = 1
    mesGasto.value = 'Octubre'
    abrirModal.value = false
  }
}

const actualizandoEstado = ref(null)
const avisoEstado = ref('')
let avisoTimer = null

function mostrarAvisoEstado(texto) {
  avisoEstado.value = texto
  clearTimeout(avisoTimer)
  avisoTimer = setTimeout(() => { avisoEstado.value = '' }, 8000)
}

async function marcarComoPagado(item) {
  if (item.estado === 'pagado') return
  actualizandoEstado.value = item.id

  // 1. Transición de estado reactiva en frontend y almacenamiento local (persiste al recargar)
  item.estado = 'pagado'
  guardarEnStorage(listaMovimientos.value)

  // 2. Persistencia en Backend / Base de Datos PostgreSQL
  try {
    const res = await fetch(`${API_URL}/movimientos/${item.id}/pagar`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (res.status === 401) return sesionExpirada()
    if (res.ok) {
      const data = await res.json()
      item.estado = data.estado || 'pagado'
      guardarEnStorage(listaMovimientos.value)
    } else if (res.status === 400) {
      // Transición inválida: ya estaba pagado (por ejemplo, desde otra pestaña)
      mostrarAvisoEstado('Transición inválida: el movimiento ya se encuentra en estado pagado.')
    }
  } catch (err) {
    console.warn('Gasto marcado como pagado localmente (servidor no disponible).')
  } finally {
    actualizandoEstado.value = null
  }
}

// ===================== Tarea 3: Editar y Eliminar =====================
const movimientoEditando = ref(null)
const editCantidad = ref(null)
const editDescripcion = ref('')
const editDia = ref(1)
const editMes = ref('Octubre')
const guardandoEdicion = ref(false)
const errorEdicion = ref('')

// Regla de estado: un movimiento pagado no permite modificar su monto
const montoBloqueado = computed(() => movimientoEditando.value?.estado === 'pagado')

function abrirEdicion(item) {
  movimientoEditando.value = item
  editCantidad.value = Number(item.monto)
  editDescripcion.value = item.descripcion
  const [, mes, dia] = String(item.fecha).split('-')
  editDia.value = parseInt(dia, 10) || 1
  editMes.value = mesesDisponibles[parseInt(mes, 10) - 1] || 'Octubre'
  errorEdicion.value = ''
}

function cerrarEdicion() {
  movimientoEditando.value = null
  errorEdicion.value = ''
}

async function guardarEdicion() {
  const item = movimientoEditando.value
  if (!item) return
  if (!editDescripcion.value.trim()) {
    errorEdicion.value = 'La descripción no puede estar vacía.'
    return
  }
  if (!montoBloqueado.value && !(Number(editCantidad.value) > 0)) {
    errorEdicion.value = 'La cantidad debe ser mayor a 0.'
    return
  }

  const anio = String(item.fecha).split('-')[0] || '2026'
  const mesStr = String(mesesDisponibles.indexOf(editMes.value) + 1).padStart(2, '0')
  const diaStr = String(parseInt(editDia.value || 1, 10)).padStart(2, '0')
  const cambios = {
    descripcion: editDescripcion.value.trim(),
    fecha: `${anio}-${mesStr}-${diaStr}`
  }
  if (!montoBloqueado.value) cambios.monto = Number(editCantidad.value)

  guardandoEdicion.value = true
  errorEdicion.value = ''
  try {
    const res = await fetch(`${API_URL}/movimientos/${item.id}`, {
      method: 'PUT',
      headers: authHeaders(),
      body: JSON.stringify(cambios)
    })
    if (res.status === 401) return sesionExpirada()
    const data = await res.json().catch(() => ({}))
    if (res.status === 404) {
      // Se eliminó en otra pestaña o dispositivo mientras se editaba
      cerrarEdicion()
      await sincronizarDesdeServidor(`"${item.descripcion}" ya no existe: se eliminó en otra pestaña o dispositivo. Tus cambios no se guardaron.`)
      return
    }
    if (!res.ok) {
      // El backend explica el motivo (p. ej. 409: se pagó en otra pestaña y el monto quedó bloqueado)
      errorEdicion.value = data.detail || 'No se pudieron guardar los cambios.'
      if (res.status === 409) await sincronizarDesdeServidor()
      return
    }
    avisarOtrasPestanas('editado', data.descripcion)
    cerrarEdicion()
    // Recarga desde la BD: trae también lo que cambió en otras pestañas
    await sincronizarDesdeServidor(`Se editó "${data.descripcion}".`)
  } catch (e) {
    errorEdicion.value = 'No se pudo conectar con el servidor. Los cambios no se guardaron.'
  } finally {
    guardandoEdicion.value = false
  }
}

const movimientoAEliminar = ref(null)
const eliminando = ref(false)
const errorEliminar = ref('')

function pedirConfirmacionEliminar(item) {
  movimientoAEliminar.value = item
  errorEliminar.value = ''
}

function cancelarEliminar() {
  movimientoAEliminar.value = null
  errorEliminar.value = ''
}

async function confirmarEliminar() {
  const item = movimientoAEliminar.value
  if (!item) return
  eliminando.value = true
  errorEliminar.value = ''
  try {
    const res = await fetch(`${API_URL}/movimientos/${item.id}`, {
      method: 'DELETE',
      headers: authHeaders()
    })
    if (res.status === 401) return sesionExpirada()
    // 404: ya no existe en la base de datos, se retira igual de la lista
    if (!res.ok && res.status !== 404) {
      const data = await res.json().catch(() => ({}))
      errorEliminar.value = data.detail || 'No se pudo eliminar el movimiento.'
      return
    }
    cancelarEliminar()
    if (res.status === 404) {
      await sincronizarDesdeServidor(`"${item.descripcion}" ya se había eliminado en otra pestaña o dispositivo.`)
    } else {
      avisarOtrasPestanas('eliminado', item.descripcion)
      await sincronizarDesdeServidor(`Se eliminó "${item.descripcion}".`)
    }
  } catch (e) {
    errorEliminar.value = 'No se pudo conectar con el servidor. El movimiento no se eliminó.'
  } finally {
    eliminando.value = false
  }
}

// ============ Sincronización entre pestañas (misma cuenta) ============
// Cada pestaña avisa a las demás cuando cambia un movimiento; las demás
// recargan la lista desde la base de datos y explican qué cambió.
const canalPestanas = !esDemo && typeof BroadcastChannel !== 'undefined'
  ? new BroadcastChannel(`movimientos_${usuarioActual.email || 'estudiante'}`)
  : null

const TEXTO_ACCION = {
  creado: 'se registró',
  editado: 'se editó',
  eliminado: 'se eliminó'
}

function avisarOtrasPestanas(accion, descripcion) {
  canalPestanas?.postMessage({ accion, descripcion })
}

async function sincronizarDesdeServidor(mensaje) {
  // Se guarda el estado que esta pestaña conocía para detectar pagos hechos en otra
  const estadosAntes = new Map(listaMovimientos.value.map(m => [m.id, m.estado]))
  await cargarMovimientos()
  const pagosExternos = listaMovimientos.value
    .filter(m => estadosAntes.get(m.id) === 'pendiente' && m.estado === 'pagado')
    .map(m => `Se actualizó "${m.descripcion}" a pagado.`)
    .join(' ')
  let extra = ''

  // Los modales abiertos no deben quedarse con datos viejos
  if (movimientoEditando.value) {
    const actual = listaMovimientos.value.find(m => m.id === movimientoEditando.value.id)
    if (!actual) {
      cerrarEdicion()
      extra = ' Se cerró la edición porque ese gasto ya no existe.'
    } else {
      if (actual.estado === 'pagado' && movimientoEditando.value.estado !== 'pagado') {
        editCantidad.value = Number(actual.monto)
        extra = ' Ese gasto ahora está pagado, por eso su monto quedó bloqueado.'
      }
      movimientoEditando.value = actual
    }
  }
  if (movimientoAEliminar.value) {
    const actual = listaMovimientos.value.find(m => m.id === movimientoAEliminar.value.id)
    if (!actual) {
      cancelarEliminar()
      extra = ' Se cerró la confirmación porque ese gasto ya no existe.'
    } else {
      movimientoAEliminar.value = actual
    }
  }

  const texto = [pagosExternos, mensaje].filter(Boolean).join(' ') + extra
  if (texto.trim()) mostrarAvisoEstado(texto.trim())
}

// Avisos recibidos mientras esta pestaña estaba oculta: se muestran al entrar a ella
const avisosPendientes = []

function mostrarAvisosPendientes() {
  if (document.visibilityState !== 'visible' || avisosPendientes.length === 0) return
  const mensaje = avisosPendientes.splice(0).join(' ')
  sincronizarDesdeServidor(`${mensaje} La lista se actualizó.`)
}

if (canalPestanas) {
  canalPestanas.onmessage = ({ data }) => {
    const accion = TEXTO_ACCION[data?.accion] || 'se modificó'
    avisosPendientes.push(`En otra pestaña ${accion} "${data?.descripcion}".`)
    mostrarAvisosPendientes()
  }
}

onMounted(() => {
  cargarMovimientos()
  cargarCategorias()
  document.addEventListener('visibilitychange', mostrarAvisosPendientes)
})

onUnmounted(() => {
  document.removeEventListener('visibilitychange', mostrarAvisosPendientes)
  canalPestanas?.close()
})
</script>

<style scoped>
.movimientos-page {
  padding: clamp(32px, 2.6vw, 52px) 0 80px 0;
  background-color: #EDF2F7;
  min-height: calc(100vh - 75px);
}

.dashboard-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: clamp(30px, 2.2vw, 42px);
  font-weight: 700;
  color: #1E3350;
}

.summary-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: clamp(20px, 1.8vw, 32px);
  margin-bottom: 24px;
}

.summary-card {
  background: #FFFFFF;
  border-radius: 10px;
  padding: clamp(18px, 1.4vw, 26px) clamp(20px, 1.6vw, 30px);
  box-shadow: 0 4px 14px rgba(15, 35, 65, 0.08);
  display: flex;
  align-items: center;
  gap: clamp(14px, 1.1vw, 20px);
}

.card-icon {
  width: clamp(48px, 3.4vw, 64px);
  height: clamp(48px, 3.4vw, 64px);
  flex-shrink: 0;
}

.card-info {
  display: flex;
  flex-direction: column;
}

.card-label {
  font-size: clamp(14px, 1vw, 18px);
  font-weight: 600;
  color: #1E293B;
  margin-bottom: 2px;
}

.card-amount {
  font-size: clamp(26px, 1.9vw, 36px);
  font-weight: 700;
  line-height: 1.15;
  margin-bottom: 2px;
}

.amount-navy {
  color: #1E3A5F;
}

.amount-sky {
  color: #4A7A9B;
}

.amount-danger {
  color: #A63A3A;
}

.card-subtext {
  font-size: clamp(12px, 0.8vw, 14px);
  color: #475569;
}

.actions-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.btn-new-mov {
  background-color: #3B78B0;
  color: #FFFFFF;
  border: none;
  padding: clamp(10px, 0.7vw, 13px) clamp(18px, 1.3vw, 24px);
  border-radius: 6px;
  font-size: clamp(14px, 0.95vw, 17px);
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-new-mov:disabled {
  background-color: #94A3B8;
  cursor: not-allowed;
}

.aviso-estado {
  background-color: #FEF3C7;
  border: 1px solid #FCD34D;
  color: #92400E;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: clamp(14px, 0.95vw, 16px);
  margin-bottom: 20px;
}

.demo-banner {
  background-color: #E0F2F7;
  border: 1px solid #A5D8E6;
  color: #1E4E5C;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: clamp(14px, 0.95vw, 16px);
  margin-bottom: 20px;
}

.demo-link {
  background: none;
  border: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
  color: #154C86;
  font-weight: 600;
  text-decoration: underline;
}

.btn-new-mov:hover:not(:disabled) {
  background-color: #2F6699;
}

.plus-icon {
  font-size: 18px;
  font-weight: 400;
}

.table-card {
  background: transparent;
  overflow: hidden;
}

.movimientos-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.movimientos-table th {
  padding: 12px clamp(12px, 1vw, 20px);
  font-size: clamp(12px, 0.8vw, 14px);
  font-weight: 500;
  letter-spacing: 0.02em;
  color: #475569;
  border-bottom: 1px solid #D5DEE8;
}

.movimientos-table td {
  padding: clamp(12px, 0.9vw, 16px) clamp(12px, 1vw, 20px);
  border-bottom: 1px solid #E2E8F0;
  background-color: #FFFFFF;
}

.table-row:hover td {
  background-color: #DCE9F6;
}

.font-date {
  font-size: clamp(14px, 0.95vw, 16px);
  font-weight: 500;
  color: #1E293B;
  width: 140px;
}

.font-desc {
  font-size: clamp(14px, 0.95vw, 16px);
  font-weight: 400;
  color: #1E293B;
}

.text-right {
  text-align: right;
}

.cat-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: clamp(12px, 0.85vw, 14px);
  font-weight: 500;
}

.badge-comida {
  background-color: #BFE0F5;
  color: #1E3A5F;
}

.badge-transporte {
  background-color: #2E8BA8;
  color: #FFFFFF;
}

.badge-libros {
  background-color: #8E6BBF;
  color: #FFFFFF;
}

.badge-ingreso {
  background-color: #D9A441;
  color: #FFFFFF;
}

.monto-plus {
  font-size: clamp(14px, 0.95vw, 16px);
  font-weight: 600;
  color: #3E8E5E;
}

.monto-minus {
  font-size: clamp(14px, 0.95vw, 16px);
  font-weight: 600;
  color: #A63A3A;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(11, 25, 44, 0.45);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}

.modal-card {
  background: #FFFFFF;
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 480px;
  padding: 28px;
  box-shadow: var(--shadow-float);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  font-size: 19px;
  font-weight: 700;
  color: var(--color-navy);
}

.btn-close-modal {
  background: none;
  border: none;
  font-size: 18px;
  color: var(--color-text-muted);
  cursor: pointer;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.type-selector {
  display: flex;
  gap: 10px;
}

.btn-type {
  flex: 1;
  padding: 10px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--color-border);
  background: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.active-gasto {
  background-color: #FFE4E6;
  border-color: #E11D48;
  color: #E11D48;
}

.active-ingreso {
  background-color: #DCFCE7;
  border-color: #16A34A;
  color: #16A34A;
}

.modal-input {
  width: 100%;
  padding: 10px 14px;
  font-size: 14px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  margin-top: 4px;
}

.modal-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.modal-error {
  color: #DC2626;
  font-size: 14px;
  margin: 0 0 12px 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
}

.btn-cancel {
  background: #F1F5F9;
  border: none;
  padding: 10px 18px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  color: var(--color-navy);
}

.btn-save {
  background-color: #3B78B0;
  color: #FFFFFF;
  border: none;
  padding: 10px 22px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

/* --- TARJETA ESTUDIANTIL (Cuentas Normales - Requerido por el Docente) --- */
.tarjeta-estudiantil-card {
  background: #FFFFFF;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(15, 35, 65, 0.08);
  overflow: hidden;
  border: 1px solid #E2E8F0;
}

.tarjeta-estudiantil-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.tarjeta-estudiantil-table thead {
  background-color: #F8FAFC;
  border-bottom: 2px solid #E2E8F0;
}

.col-mov-header,
.col-desc-header,
.col-fecha-header,
.col-estado-header,
.col-accion-header {
  padding: 18px 24px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #475569;
  text-transform: uppercase;
}

.tarjeta-estudiantil-table td {
  padding: 18px 24px;
  border-bottom: 1px solid #F1F5F9;
  vertical-align: middle;
}

.fila-movimiento:hover {
  background-color: #F8FAFC;
}

.badge-movimiento {
  display: inline-block;
  font-weight: 700;
  font-size: 15px;
  padding: 6px 14px;
  border-radius: 6px;
  letter-spacing: 0.02em;
}

.badge-gasto-bs {
  background-color: #FEE2E2;
  color: #B91C1C;
  border: 1px solid #FECACA;
}

.badge-pendiente-monto {
  background-color: #FEF3C7;
  color: #B45309;
  border: 1px solid #FDE68A;
}

.badge-ingreso-bs {
  background-color: #DCFCE7;
  color: #15803D;
  border: 1px solid #BBF7D0;
}

.col-estado-dato {
  vertical-align: middle;
}

.badge-estado-pill {
  display: inline-block;
  font-weight: 700;
  font-size: 13px;
  padding: 6px 18px;
  border-radius: 9999px;
  letter-spacing: 0.02em;
}

.badge-estado-pendiente {
  background-color: #FBBF24;
  color: #78350F;
  border: 1px solid #F59E0B;
}

.badge-estado-pagado {
  background-color: #22C55E;
  color: #FFFFFF;
}

.btn-marcar-pagado {
  background-color: #2563EB;
  color: #FFFFFF;
  border: none;
  padding: 8px 22px;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-marcar-pagado:hover:not(:disabled) {
  background-color: #1D4ED8;
  box-shadow: 0 4px 12px rgba(29, 78, 216, 0.35);
  transform: translateY(-1px);
}

.btn-marcar-pagado:disabled {
  opacity: 0.7;
  cursor: wait;
}

.estado-pagado-check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* --- Tarea 3: acciones Editar / Eliminar --- */
.acciones-fila {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
}

.btn-accion {
  background: #FFFFFF;
  border: 1.5px solid;
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-editar {
  color: #1E3350;
  border-color: #CBD5E1;
}

.btn-editar:hover {
  background-color: #F1F5F9;
}

.btn-eliminar {
  color: #DC2626;
  border-color: #FCA5A5;
}

.btn-eliminar:hover {
  background-color: #FEF2F2;
}

.icon-editar {
  background-color: #DBEAFE;
  color: #2563EB;
}

.input-cantidad:disabled {
  background-color: #F1F5F9;
  color: #64748B;
  cursor: not-allowed;
}

.aviso-bloqueo {
  font-size: 13px;
  color: #92400E;
  background-color: #FEF3C7;
  border-left: 3px solid #F59E0B;
  padding: 8px 12px;
  border-radius: 6px;
  margin: 2px 0 0 0;
}

.texto-confirmar {
  font-size: 14px;
  color: #334155;
  line-height: 1.5;
  margin: 12px 0 20px 0;
}

.btn-confirmar-eliminar {
  background-color: #DC2626;
  color: #FFFFFF;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-confirmar-eliminar:hover:not(:disabled) {
  background-color: #B91C1C;
}

.btn-confirmar-eliminar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.col-desc-dato {
  font-size: 15px;
  font-weight: 600;
  color: #1E293B;
}

.col-fecha-dato {
  font-size: 15px;
  font-weight: 500;
  color: #475569;
}

/* Estado vacío */
.fila-vacia td {
  padding: 48px 24px;
  text-align: center;
}

.estado-vacio {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.emoji-vacio {
  font-size: 36px;
  margin-bottom: 4px;
}

.titulo-vacio {
  font-size: 17px;
  font-weight: 700;
  color: #1E3350;
  margin: 0;
}

.subtitulo-vacio {
  font-size: 14px;
  color: #64748B;
  margin: 0;
}

/* --- DASHBOARD MODAL: REGISTRAR GASTO --- */
.dashboard-modal-card {
  max-width: 440px;
  border-radius: 14px;
  padding: 28px 32px;
  box-shadow: 0 20px 40px rgba(15, 35, 65, 0.2);
}

.dashboard-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.dashboard-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dashboard-icon-circle {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background-color: #FEE2E2;
  color: #DC2626;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-titulo {
  font-size: 24px;
  font-weight: 800;
  color: #1E3350;
  margin: 0;
}

.dashboard-subtitulo {
  font-size: 13px;
  color: #64748B;
  margin: 0 0 22px 0;
}

.dashboard-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-grupo-custom {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label-custom {
  font-size: 14px;
  font-weight: 700;
  color: #1E293B;
}

.input-moneda-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.prefijo-bs {
  position: absolute;
  left: 14px;
  font-weight: 700;
  font-size: 14px;
  color: #64748B;
  pointer-events: none;
}

.form-input-custom {
  width: 100%;
  padding: 10px 14px;
  font-size: 14px;
  border: 1.5px solid #CBD5E1;
  border-radius: 8px;
  background-color: #FFFFFF;
  color: #1E293B;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-input-custom:focus {
  outline: none;
  border-color: #2563EB;
}

.input-moneda-wrapper .input-cantidad {
  padding-left: 42px;
  font-weight: 600;
}

.form-fila-fecha {
  display: grid;
  grid-template-columns: 110px 1fr;
  gap: 12px;
}

.text-center {
  text-align: center;
}

.select-mes-custom {
  cursor: pointer;
  appearance: auto;
}

.form-error-custom {
  font-size: 13px;
  color: #DC2626;
  margin: 0;
  background-color: #FEF2F2;
  padding: 8px 12px;
  border-radius: 6px;
  border-left: 3px solid #DC2626;
}

.dashboard-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
}

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

.btn-cancelar-modal:hover {
  background-color: #E2E8F0;
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

.btn-guardar-principal:hover:not(:disabled) {
  background-color: #1D4ED8;
}

.btn-guardar-principal:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 900px) {
  .summary-cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
