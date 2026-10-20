<template>
  <div class="historial-page">
    <div class="container historial-contenedor">

      <!-- Issue #12: ¿Qué movimientos tuvo el mes? -->
      <h1 class="page-title">Historial del mes</h1>

      <!-- /// [Fitts: cambiar de mes con objetivos grandes y pegados al nombre del mes] /// -->
      <div class="mes-navegacion">
        <button type="button" class="btn-mes" @click="cambiarMes(-1)" :aria-label="`Ver ${textoMes(mesVecino(-1))}`">‹</button>
        <h2 class="mes-titulo" aria-live="polite">{{ historial ? historial.mes_texto : textoMes(mes) }}</h2>
        <button type="button" class="btn-mes" @click="cambiarMes(1)" :aria-label="`Ver ${textoMes(mesVecino(1))}`">›</button>
      </div>
      <button v-if="mes !== mesActual" type="button" class="btn-volver-mes" @click="irAlMes(mesActual)">
        Volver a {{ textoMes(mesActual) }}
      </button>
      <!-- /// =========================================================================== /// -->

      <p v-if="error" class="aviso-error" role="alert">{{ error }}</p>
      <p v-else-if="cargando && !historial" class="aviso-cargando">Cargando historial…</p>

      <template v-else-if="historial">
        <!-- /// [Carga cognitiva: el resumen del mes está junto a la lista, no hay que recordarlo de otra pantalla] /// -->
        <section v-if="historial.resumen.cantidad > 0" class="resumen-mes" aria-label="Resumen del mes">
          <div class="resumen-item">
            <span class="resumen-etiqueta">Ingresos</span>
            <span class="resumen-valor monto-ingreso">{{ historial.resumen.ingresos > 0 ? '+' : '' }}{{ bs(historial.resumen.ingresos) }}</span>
          </div>
          <div class="resumen-item">
            <span class="resumen-etiqueta">Gastos</span>
            <span class="resumen-valor monto-gasto">{{ historial.resumen.gastos > 0 ? '−' : '' }}{{ bs(historial.resumen.gastos) }}</span>
          </div>
          <div class="resumen-item">
            <span class="resumen-etiqueta">Balance del mes</span>
            <span :class="['resumen-valor', historial.resumen.balance < 0 ? 'monto-gasto' : 'monto-balance']">
              {{ historial.resumen.balance < 0 ? '−' : '' }}{{ bs(Math.abs(historial.resumen.balance)) }}
            </span>
          </div>
          <span class="resumen-nota">
            {{ historial.resumen.cantidad }} {{ historial.resumen.cantidad === 1 ? 'movimiento' : 'movimientos' }} · pagados y pendientes
          </span>
        </section>
        <!-- /// ================================================================================================ /// -->

        <!-- Estado vacío orientador -->
        <section v-if="historial.resumen.cantidad === 0" class="estado-vacio">
          <img :src="iconHistorial" alt="" class="vacio-icono" />
          <h3>No registraste movimientos en {{ historial.mes_texto }}</h3>
          <p>Cuando registres un gasto o un ingreso con fecha de este mes, aparecerá aquí ordenado por día.</p>
          <button type="button" class="btn-principal" @click="irARegistrar">+ Registrar movimiento</button>
        </section>

        <template v-else>
          <!-- /// [Hick: solo 3 opciones visibles; el mes ya viene elegido] /// -->
          <div class="segmentos" role="group" aria-label="Mostrar">
            <button
              v-for="op in OPCIONES_TIPO"
              :key="op.valor"
              type="button"
              :class="['segmento', { 'segmento-activo': tipoVisible === op.valor }]"
              :aria-pressed="tipoVisible === op.valor"
              @click="tipoVisible = op.valor"
            >{{ op.texto }}</button>
          </div>
          <!-- /// ======================================================== /// -->

          <p v-if="diasVisibles.length === 0" class="aviso-sin-tipo">
            No hay {{ tipoVisible === 'ingreso' ? 'ingresos' : 'gastos' }} en {{ historial.mes_texto }}.
          </p>

          <!-- /// [Carga cognitiva: movimientos agrupados por día, del más reciente al más antiguo] /// -->
          <section v-for="dia in diasVisibles" :key="dia.fecha" class="dia">
            <h3 class="dia-titulo">{{ textoDia(dia.fecha) }}</h3>
            <ul class="dia-lista">
              <li v-for="mov in dia.movimientos" :key="mov.id" class="mov">
                <div class="mov-info">
                  <span class="mov-descripcion">{{ mov.descripcion }}</span>
                  <span class="mov-detalle">{{ mov.tipo === 'ingreso' ? 'Ingreso' : 'Gasto' }} · {{ mov.categoria }}</span>
                </div>
                <div class="mov-resultado">
                  <span :class="['mov-monto', mov.tipo === 'ingreso' ? 'monto-ingreso' : 'monto-gasto']">
                    {{ mov.tipo === 'ingreso' ? '+' : '−' }}{{ bs(mov.monto) }}
                  </span>
                  <span :class="['mov-estado', mov.estado === 'pagado' ? 'estado-ok' : 'estado-pendiente']">
                    {{ textoEstado(mov) }}
                  </span>
                </div>
              </li>
            </ul>
          </section>
          <!-- /// =================================================================================== /// -->
        </template>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import iconHistorial from '../assets/icon-historial.png'

const API_URL = 'http://localhost:8000'
const route = useRoute()
const router = useRouter()

const MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
  'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
const DIAS = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
const OPCIONES_TIPO = [
  { valor: 'todos', texto: 'Todos' },
  { valor: 'ingreso', texto: 'Ingresos' },
  { valor: 'gasto', texto: 'Gastos' }
]

const hoy = new Date()
const mesActual = `${hoy.getFullYear()}-${String(hoy.getMonth() + 1).padStart(2, '0')}`

// El mes elegido vive en la URL (?mes=AAAA-MM): al recargar se ve el mismo mes
const mes = computed(() => (/^\d{4}-\d{2}$/.test(route.query.mes || '') ? route.query.mes : mesActual))

const historial = ref(null)
const cargando = ref(false)
const error = ref('')
const tipoVisible = ref('todos')

const bs = n => `${Number(n).toFixed(2)} Bs`

function textoMes(aaaamm) {
  const [anio, m] = aaaamm.split('-').map(Number)
  return `${MESES[m - 1]} ${anio}`
}

function mesVecino(paso) {
  const [anio, m] = mes.value.split('-').map(Number)
  const d = new Date(anio, m - 1 + paso, 1)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
}

function textoDia(fechaISO) {
  const [anio, m, d] = fechaISO.split('-').map(Number)
  const fecha = new Date(anio, m - 1, d)
  return `${DIAS[fecha.getDay()]} ${d} de ${MESES[m - 1].toLowerCase()}`
}

// El estado se lee con texto, no solo con color
function textoEstado(mov) {
  if (mov.estado !== 'pagado') return 'Pendiente'
  return mov.tipo === 'ingreso' ? 'Recibido' : 'Pagado'
}

function irAlMes(aaaamm) {
  router.replace({ query: aaaamm === mesActual ? {} : { mes: aaaamm } })
}

function cambiarMes(paso) {
  irAlMes(mesVecino(paso))
}

function irARegistrar() {
  router.push({ path: '/movimientos', query: { registrar: '1' } })
}

const diasVisibles = computed(() => {
  if (!historial.value) return []
  if (tipoVisible.value === 'todos') return historial.value.dias
  return historial.value.dias
    .map(dia => ({ ...dia, movimientos: dia.movimientos.filter(m => m.tipo === tipoVisible.value) }))
    .filter(dia => dia.movimientos.length > 0)
})

async function cargarHistorial() {
  cargando.value = true
  error.value = ''
  try {
    const res = await fetch(`${API_URL}/movimientos/historial?mes=${mes.value}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    if (res.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('usuario')
      return router.push('/login')
    }
    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      error.value = data.detail || 'No se pudo cargar el historial.'
      return
    }
    historial.value = data
  } catch (e) {
    error.value = 'No se pudo conectar con el servidor para cargar el historial.'
  } finally {
    cargando.value = false
  }
}

watch(mes, () => {
  tipoVisible.value = 'todos'
  cargarHistorial()
}, { immediate: true })
</script>

<style scoped>
.historial-page {
  padding: clamp(32px, 2.6vw, 52px) 0 80px 0;
  background-color: #EDF2F7;
  min-height: calc(100vh - 75px);
}

.historial-contenedor {
  max-width: 960px;
}

.page-title {
  font-size: clamp(30px, 2.2vw, 42px);
  font-weight: 700;
  color: #1E3350;
  margin-bottom: 20px;
}

.mes-navegacion {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Fitts: 48 px, mínimo cómodo para mouse y dedo */
.btn-mes {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 10px;
  border: 1px solid #3B6EA5;
  background: #FFFFFF;
  color: #1E3350;
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-mes:hover {
  background: #E0ECF8;
}

.mes-titulo {
  flex: 1;
  text-align: center;
  font-size: clamp(22px, 1.6vw, 28px);
  font-weight: 700;
  color: #1E3350;
}

.btn-volver-mes {
  display: block;
  margin: 10px auto 0;
  min-height: 40px;
  padding: 0 18px;
  border: none;
  background: transparent;
  color: #3B6EA5;
  font-size: 15px;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
}

.resumen-mes {
  margin-top: 20px;
  background: #FFFFFF;
  border-radius: 10px;
  box-shadow: 0 4px 14px rgba(15, 35, 65, 0.08);
  padding: 20px 24px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px 20px;
}

.resumen-item {
  display: flex;
  flex-direction: column;
}

.resumen-etiqueta {
  font-size: 14px;
  color: #475569;
}

.resumen-valor {
  font-size: clamp(22px, 1.6vw, 28px);
  font-weight: 700;
}

.resumen-nota {
  grid-column: 1 / -1;
  font-size: 13px;
  color: #64748B;
}

.monto-ingreso { color: #15803D; }
.monto-gasto { color: #B91C1C; }
.monto-balance { color: #1E3350; }

.segmentos {
  display: flex;
  gap: 8px;
  margin: 24px 0 8px;
}

.segmento {
  min-height: 44px;
  padding: 0 22px;
  border-radius: 999px;
  border: 1px solid #CBD5E1;
  background: #FFFFFF;
  color: #1E3350;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.segmento-activo {
  background: #3B6EA5;
  border-color: #3B6EA5;
  color: #FFFFFF;
}

.dia {
  margin-top: 20px;
}

.dia-titulo {
  font-size: 15px;
  font-weight: 700;
  color: #475569;
  margin-bottom: 8px;
}

.dia-lista {
  list-style: none;
  background: #FFFFFF;
  border-radius: 10px;
  box-shadow: 0 4px 14px rgba(15, 35, 65, 0.06);
}

.mov {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 14px 20px;
}

.mov + .mov {
  border-top: 1px solid #E2E8F0;
}

.mov-info,
.mov-resultado {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.mov-resultado {
  align-items: flex-end;
  flex-shrink: 0;
}

.mov-descripcion {
  font-size: 16px;
  font-weight: 600;
  color: #1E293B;
  overflow-wrap: anywhere;
}

.mov-detalle {
  font-size: 14px;
  color: #64748B;
}

.mov-monto {
  font-size: 17px;
  font-weight: 700;
}

.mov-estado {
  font-size: 13px;
  font-weight: 600;
}

.estado-ok { color: #15803D; }
.estado-pendiente { color: #B45309; }

.estado-vacio {
  margin-top: 24px;
  background: #FFFFFF;
  border-radius: 10px;
  box-shadow: 0 4px 14px rgba(15, 35, 65, 0.08);
  padding: 40px 24px;
  text-align: center;
}

.vacio-icono {
  width: 64px;
  height: 64px;
  margin-bottom: 12px;
}

.estado-vacio h3 {
  font-size: 20px;
  color: #1E3350;
  margin-bottom: 8px;
}

.estado-vacio p {
  color: #475569;
  margin-bottom: 20px;
}

.btn-principal {
  min-height: 48px;
  padding: 0 28px;
  border: none;
  border-radius: 8px;
  background: #3B6EA5;
  color: #FFFFFF;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.btn-principal:hover {
  background: #2F5A88;
}

.aviso-error {
  margin-top: 20px;
  padding: 14px 18px;
  border-radius: 8px;
  background: #FFE4E6;
  color: #9F1239;
}

.aviso-cargando,
.aviso-sin-tipo {
  margin-top: 20px;
  color: #475569;
}

@media (max-width: 640px) {
  .resumen-mes {
    grid-template-columns: 1fr;
  }
  .segmento {
    flex: 1;
    padding: 0 10px;
  }
  .mov {
    padding: 12px 14px;
  }
}
</style>
