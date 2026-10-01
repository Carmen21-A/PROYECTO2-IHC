<template>
  <div class="auth-page">
    <div class="auth-card">

      <div class="card-header">
        <h2 class="card-title">Recuperar Acceso</h2>
        <p class="card-subtitle">
          {{ subtitulos[paso - 1] }}
        </p>
      </div>

      <div class="steps">
        <span v-for="n in 3" :key="n" :class="['step-dot', n <= paso ? 'step-active' : '']"></span>
      </div>

      <form v-if="paso === 1" @submit.prevent="enviarCodigo" class="auth-form">
        <div class="form-group">
          <label class="form-label">Correo Registrado</label>
          <div class="input-wrapper">
            <span class="input-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg></span>
            <input
              v-model="email"
              type="email"
              placeholder="estudiante@universidad.edu"
              class="form-input"
              required
            />
          </div>
        </div>

        <div v-if="errorMsg" class="error-alert">{{ errorMsg }}</div>

        <button type="submit" class="btn-submit" :disabled="cargando">
          {{ cargando ? 'Enviando código...' : 'Enviar código' }}
        </button>

        <div class="auth-footer-links">
          <router-link to="/login" class="link-highlight">
            ← Volver a Iniciar Sesión
          </router-link>
        </div>
      </form>

      <form v-else-if="paso === 2" @submit.prevent="verificarCodigo" class="auth-form">
        <div class="info-alert">
          {{ infoMsg }} Revisa la bandeja de entrada (o spam) de <strong>{{ email }}</strong>.
        </div>

        <div class="form-group">
          <label class="form-label code-label">Código de verificación</label>
          <div class="code-inputs" @paste.prevent="pegarCodigo">
            <input
              v-for="(d, i) in digitos"
              :key="i"
              :ref="el => (casillas[i] = el)"
              v-model="digitos[i]"
              type="text"
              inputmode="numeric"
              maxlength="1"
              class="code-box"
              @input="alEscribir(i)"
              @keydown.backspace="alBorrar(i, $event)"
            />
          </div>
        </div>

        <div v-if="errorMsg" class="error-alert">{{ errorMsg }}</div>

        <button type="submit" class="btn-submit" :disabled="cargando || codigo.length < 4">
          {{ cargando ? 'Verificando...' : 'Verificar código' }}
        </button>

        <div class="auth-footer-links">
          <button type="button" @click="enviarCodigo" class="btn-back-step" :disabled="cargando">
            Reenviar código
          </button>
          <span class="separator">·</span>
          <button type="button" @click="volverAlPaso1" class="btn-back-step">
            Cambiar correo
          </button>
        </div>
      </form>

      <form v-else @submit.prevent="guardarNuevaPassword" class="auth-form">
        <div class="form-group">
          <label class="form-label">Nueva Contraseña</label>
          <div class="input-wrapper">
            <span class="input-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="15.5" r="4.5"/><path d="m10.7 12.3 9.3-9.3M17 6l3 3M15 8l2 2"/></svg></span>
            <input
              v-model="nuevaPassword"
              type="password"
              placeholder="Mínimo 6 caracteres"
              class="form-input"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Confirmar Nueva Contraseña</label>
          <div class="input-wrapper">
            <span class="input-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg></span>
            <input
              v-model="confirmarPassword"
              type="password"
              placeholder="Repite tu nueva contraseña"
              class="form-input"
              required
            />
          </div>
        </div>

        <div v-if="errorMsg" class="error-alert">{{ errorMsg }}</div>
        <div v-if="successMsg" class="success-alert">{{ successMsg }}</div>

        <button type="submit" class="btn-submit" :disabled="cargando || !!successMsg">
          {{ cargando ? 'Guardando...' : 'Cambiar Contraseña' }}
        </button>
      </form>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const API_URL = 'http://localhost:8000'
const router = useRouter()

const subtitulos = [
  'Ingresa tu correo y te enviaremos un código de verificación de 4 dígitos.',
  'Ingresa el código de 4 dígitos que te enviamos por correo.',
  'Código verificado. Define tu nueva contraseña.'
]

const paso = ref(1)
const email = ref('')
const digitos = ref(['', '', '', ''])
const casillas = []
const nuevaPassword = ref('')
const confirmarPassword = ref('')
const cargando = ref(false)
const errorMsg = ref('')
const infoMsg = ref('')
const successMsg = ref('')

const codigo = computed(() => digitos.value.join(''))

async function postRecuperar(ruta, datos) {
  let res
  try {
    res = await fetch(`${API_URL}/auth/recuperar/${ruta}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    })
  } catch (e) {
    throw new Error('No se pudo conectar con el servidor. Verifica que el backend esté encendido.')
  }
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Ocurrió un error. Intenta de nuevo.')
  return data
}

async function enviarCodigo() {
  errorMsg.value = ''
  cargando.value = true
  try {
    const data = await postRecuperar('solicitar', { email: email.value })
    infoMsg.value = data.mensaje
    digitos.value = ['', '', '', '']
    paso.value = 2
    await nextTick()
    casillas[0]?.focus()
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    cargando.value = false
  }
}

function alEscribir(i) {
  digitos.value[i] = digitos.value[i].replace(/\D/g, '').slice(-1)
  if (digitos.value[i] && i < 3) casillas[i + 1]?.focus()
}

function alBorrar(i, evento) {
  if (!digitos.value[i] && i > 0) {
    evento.preventDefault()
    digitos.value[i - 1] = ''
    casillas[i - 1]?.focus()
  }
}

function pegarCodigo(evento) {
  const numeros = evento.clipboardData.getData('text').replace(/\D/g, '').slice(0, 4).split('')
  digitos.value = [0, 1, 2, 3].map(i => numeros[i] || '')
  casillas[Math.min(numeros.length, 3)]?.focus()
}

function volverAlPaso1() {
  errorMsg.value = ''
  paso.value = 1
}

async function verificarCodigo() {
  errorMsg.value = ''
  cargando.value = true
  try {
    await postRecuperar('verificar', { email: email.value, codigo: codigo.value })
    paso.value = 3
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    cargando.value = false
  }
}

async function guardarNuevaPassword() {
  errorMsg.value = ''
  successMsg.value = ''

  if (nuevaPassword.value.length < 6) {
    errorMsg.value = 'La nueva contraseña debe tener al menos 6 caracteres.'
    return
  }
  if (nuevaPassword.value !== confirmarPassword.value) {
    errorMsg.value = 'Las contraseñas no coinciden.'
    return
  }

  cargando.value = true
  try {
    await postRecuperar('restablecer', {
      email: email.value,
      codigo: codigo.value,
      nueva_password: nuevaPassword.value
    })
    successMsg.value = '¡Contraseña cambiada exitosamente! Redirigiendo al login...'
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    cargando.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  min-height: calc(100vh - 75px);
  background: linear-gradient(135deg, #C3D0FA 0%, #BDEFF4 40%, #B8ECF2 60%, #D8CBF7 100%);
}

.auth-card {
  background: #FFFFFF;
  width: 100%;
  max-width: clamp(420px, 30vw, 580px);
  border-radius: 14px;
  box-shadow: 0 12px 32px rgba(30, 64, 120, 0.16);
  padding: clamp(20px, 1.6vw, 28px);
}

.card-header {
  text-align: center;
  margin-bottom: 18px;
}

.card-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--color-navy);
  margin-bottom: 6px;
}

.card-subtitle {
  font-size: 13.5px;
  color: var(--color-text-muted);
  line-height: 1.5;
}

.steps {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 22px;
}

.step-dot {
  width: 36px;
  height: 5px;
  border-radius: 3px;
  background-color: #E2E8F0;
}

.step-dot.step-active {
  background-color: #2E7D9A;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.form-label {
  font-size: clamp(14px, 0.95vw, 17px);
  font-weight: 600;
  color: #0F172A;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 13px;
  display: flex;
  color: #475569;
}

.form-input {
  width: 100%;
  padding: clamp(10px, 0.7vw, 13px) 42px;
  font-size: clamp(14px, 0.95vw, 17px);
  border: 1px solid #CBD5E1;
  border-radius: 6px;
  color: #334155;
  background-color: #FFFFFF;
  transition: all 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #2E7D9A;
  box-shadow: 0 0 0 3px rgba(46, 125, 154, 0.15);
}

.code-label {
  text-align: center;
}

.code-inputs {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.code-box {
  width: clamp(52px, 3.6vw, 64px);
  height: clamp(58px, 4vw, 70px);
  text-align: center;
  font-size: clamp(26px, 1.8vw, 32px);
  font-weight: 700;
  color: #154C86;
  border: 1.5px solid #CBD5E1;
  border-radius: 8px;
  transition: all 0.2s;
}

.code-box:focus {
  outline: none;
  border-color: #2E7D9A;
  box-shadow: 0 0 0 3px rgba(46, 125, 154, 0.15);
}

.info-alert {
  background-color: var(--color-sky-light);
  color: #0369A1;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  line-height: 1.45;
}

.error-alert {
  background-color: var(--color-danger-light);
  color: var(--color-danger);
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
}

.success-alert {
  background-color: #DCFCE7;
  color: var(--color-success);
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
}

.btn-submit {
  background-color: #2E7D9A;
  color: #FFFFFF;
  border: none;
  padding: clamp(12px, 0.8vw, 15px);
  border-radius: 6px;
  font-size: clamp(15px, 1.05vw, 19px);
  font-weight: 500;
  cursor: pointer;
  margin-top: 4px;
  transition: all 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background-color: #24677F;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-back-step {
  background: none;
  border: none;
  color: var(--color-text-muted);
  font-size: 13px;
  cursor: pointer;
  text-decoration: underline;
}

.separator {
  color: #94A3B8;
  margin: 0 6px;
}

.auth-footer-links {
  text-align: center;
  margin-top: 10px;
}

.link-highlight {
  color: #154C86;
  font-weight: 500;
  text-decoration: none;
}
</style>
