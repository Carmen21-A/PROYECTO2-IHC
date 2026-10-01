<template>
  <div class="auth-page">
    <div class="auth-card">

      <div class="auth-tabs">
        <router-link to="/login" class="tab-btn">
          Iniciar Sesión
        </router-link>
        <button class="tab-btn active">
          Registrarse
        </button>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">

        <div class="form-group">
          <label class="form-label">Nombre Completo</label>
          <div class="input-wrapper">
            <span class="input-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/></svg></span>
            <input
              v-model="nombre"
              type="text"
              placeholder="Ej. Carmen Aranibar"
              class="form-input"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Correo Electrónico</label>
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

        <div class="form-group">
          <label class="form-label">Contraseña</label>
          <div class="input-wrapper">
            <span class="input-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg></span>
            <input
              v-model="password"
              type="password"
              placeholder="Mínimo 6 caracteres"
              class="form-input"
              required
            />
          </div>
        </div>

        <div v-if="errorMsg" class="error-alert">
          {{ errorMsg }}
        </div>
        <div v-if="successMsg" class="success-alert">
          {{ successMsg }}
        </div>

        <button type="submit" class="btn-submit" :disabled="cargando">
          {{ cargando ? 'Creando cuenta...' : 'Crear Cuenta' }}
        </button>

        <div class="auth-footer-links">
          <p class="footer-link-text">
            ¿Ya tienes una cuenta?
            <router-link to="/login" class="link-highlight">Inicia sesión aquí</router-link>
          </p>
        </div>

      </form>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const nombre = ref('')
const email = ref('')
const password = ref('')
const cargando = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

async function handleRegister() {
  cargando.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    const res = await fetch('http://localhost:8000/auth/registro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nombre: nombre.value,
        email: email.value,
        password: password.value
      })
    })

    if (res.ok) {
      const data = await res.json()
      successMsg.value = '¡Cuenta creada con éxito! Redirigiendo...'
      localStorage.setItem('token', data.token)
      localStorage.setItem('usuario', JSON.stringify(data.usuario))
      window.dispatchEvent(new Event('usuario-autenticado'))
      setTimeout(() => router.push('/movimientos'), 1200)
    } else {
      const err = await res.json()
      errorMsg.value = err.detail || 'No se pudo crear la cuenta.'
    }
  } catch (e) {
    errorMsg.value = 'No se pudo conectar con el servidor. Verifica que el backend esté encendido.'
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

.auth-tabs {
  display: flex;
  border-bottom: 1px solid #E2E8F0;
  margin-bottom: 22px;
}

.tab-btn {
  flex: 1;
  text-align: center;
  padding: clamp(10px, 0.7vw, 13px) 0;
  font-size: clamp(15px, 1vw, 18px);
  font-weight: 500;
  color: #64748B;
  background: none;
  border: none;
  border-radius: 6px 6px 0 0;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
}

.tab-btn.active {
  background-color: #154C86;
  color: #FFFFFF;
}

.tab-btn:hover:not(.active) {
  color: #154C86;
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

.auth-footer-links {
  text-align: center;
  margin-top: 10px;
}

.footer-link-text {
  font-size: clamp(13px, 0.9vw, 16px);
  color: #0F172A;
}

.link-highlight {
  color: #154C86;
  font-weight: 500;
  text-decoration: none;
}
</style>
