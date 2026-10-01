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
            <span class="card-amount amount-navy">${{ saldoTotal.toFixed(2) }}</span>
            <span class="card-subtext">Actualizado hoy</span>
          </div>
        </div>

        <div class="summary-card">
          <img :src="iconIngresos" alt="" class="card-icon" />
          <div class="card-info">
            <span class="card-label">Ingresos del Mes</span>
            <span class="card-amount amount-sky">${{ ingresosTotal.toFixed(2) }}</span>
            <span class="card-subtext">Octubre 2026</span>
          </div>
        </div>

        <div class="summary-card">
          <img :src="iconGastos" alt="" class="card-icon" />
          <div class="card-info">
            <span class="card-label">Gastos del Mes</span>
            <span class="card-amount amount-danger">${{ gastosTotal.toFixed(2) }}</span>
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

      <div class="table-card">
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

    <div v-if="abrirModal" class="modal-overlay" @click.self="abrirModal = false">
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

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import iconSaldo from '../assets/icon-saldo.png'
import iconIngresos from '../assets/icon-ingresos.png'
import iconGastos from '../assets/icon-gastos.png'

const API_URL = 'http://localhost:8000'
const router = useRouter()

const usuarioActual = JSON.parse(localStorage.getItem('usuario') || '{}')
const esDemo = usuarioActual.es_demo === true

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

const listaMovimientos = ref([])
const categorias = ref([])
const ingresosTotal = ref(0)
const gastosTotal = ref(0)
const saldoTotal = ref(0)

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
  const res = await fetch(`${API_URL}/movimientos`, { headers: authHeaders() })
  if (res.status === 401) return sesionExpirada()
  const data = await res.json()
  listaMovimientos.value = data.movimientos
  ingresosTotal.value = data.ingresos_del_mes
  gastosTotal.value = data.gastos_del_mes
  saldoTotal.value = data.saldo_disponible
}

async function cargarCategorias() {
  const res = await fetch(`${API_URL}/categorias`)
  categorias.value = await res.json()
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

onMounted(() => {
  cargarMovimientos()
  cargarCategorias()
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
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

@media (max-width: 900px) {
  .summary-cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
