<template>
  <div class="app-layout">
    <header v-if="esRutaPrivada" class="navbar-navy">
      <div class="nav-container">
        <div class="nav-left">
          <router-link to="/movimientos" class="brand-logo-white">
            <img :src="logo" alt="Logo Presupuesto Estudiantil" class="icon-cap" />
            <span class="brand-text">Presupuesto<br/>Estudiantil</span>
          </router-link>
          <nav class="nav-links-white">
            <router-link to="/" class="nav-item-white">Inicio</router-link>
            <router-link to="/movimientos" class="nav-item-white active">Mis Movimientos</router-link>
          </nav>
        </div>

        <div class="nav-right">
          <div class="user-greeting">
            <div class="user-avatar" :title="nombreUsuario">{{ inicialUsuario }}</div>
            <span class="greeting-text">¡Hola,<br /><strong>{{ primerNombre }}!</strong></span>
          </div>
          <button @click="cerrarSesion" class="btn-logout">Cerrar Sesión</button>
        </div>
      </div>
    </header>

    <header v-else class="navbar-light">
      <div class="nav-container">
        <router-link to="/" class="brand-logo">
          <img :src="logo" alt="Logo Presupuesto Estudiantil" class="icon-cap" />
          <span class="brand-text">Presupuesto<br/>Estudiantil</span>
        </router-link>

        <nav v-if="$route.path === '/'" class="nav-links">
          <a href="#inicio" class="nav-link active">Inicio</a>
          <a href="#funcionalidades" class="nav-link">Funcionalidades</a>
          <a href="#precios" class="nav-link">Precios</a>
          <a href="#ayuda" class="nav-link">Ayuda</a>
        </nav>

        <div class="nav-actions">
          <router-link v-if="$route.path !== '/'" to="/" class="btn-back-home">
            Volver al Inicio
          </router-link>
          <template v-else>
            <router-link to="/login" class="btn-login-outline">Iniciar Sesión</router-link>
            <router-link to="/registro" class="btn-register-solid">
              <svg class="btn-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/></svg> Crear Cuenta
            </router-link>
          </template>
        </div>
      </div>
    </header>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import logo from './assets/logo.png'

const route = useRoute()
const router = useRouter()

const nombreUsuario = ref('')

const primerNombre = computed(() => nombreUsuario.value.trim().split(' ')[0])
const inicialUsuario = computed(() => nombreUsuario.value.trim().charAt(0).toUpperCase())

const esRutaPrivada = computed(() => {
  return route.path === '/movimientos'
})

function cargarUsuario() {
  const usuarioGuardado = localStorage.getItem('usuario')
  if (usuarioGuardado) {
    try {
      const u = JSON.parse(usuarioGuardado)
      nombreUsuario.value = u.nombre || ''
    } catch (e) {
      nombreUsuario.value = usuarioGuardado
    }
  }
}

function cerrarSesion() {
  localStorage.removeItem('token')
  localStorage.removeItem('usuario')
  router.push('/login')
}

onMounted(() => {
  cargarUsuario()
  window.addEventListener('usuario-autenticado', cargarUsuario)
})
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.nav-container {
  max-width: 1760px;
  margin: 0 auto;
  padding: 16px clamp(24px, 5vw, 96px);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-navy {
  background-color: #10233F;
  color: #FFFFFF;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.brand-logo-white {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  text-decoration: none;
}

.brand-logo-white .icon-cap {
  width: clamp(38px, 2.6vw, 48px);
  height: clamp(38px, 2.6vw, 48px);
}

.brand-logo-white .brand-text {
  font-size: clamp(17px, 1.1vw, 21px);
  font-weight: 600;
  line-height: 1.15;
}

.nav-links-white {
  display: flex;
  gap: clamp(24px, 2vw, 40px);
}

.nav-item-white {
  color: #E2E8F0;
  font-size: clamp(14px, 0.95vw, 17px);
  font-weight: 400;
  text-decoration: none;
  transition: color 0.2s;
}

.nav-item-white:hover, .nav-item-white.active {
  color: #FFFFFF;
  font-weight: 500;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-greeting {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: clamp(38px, 2.6vw, 46px);
  height: clamp(38px, 2.6vw, 46px);
  border-radius: 50%;
  background-color: #2E7D9A;
  border: 2px solid rgba(255, 255, 255, 0.7);
  color: #FFFFFF;
  font-size: clamp(17px, 1.2vw, 21px);
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.greeting-text {
  font-size: clamp(14px, 0.95vw, 17px);
  line-height: 1.25;
  color: #E2E8F0;
}

.greeting-text strong {
  color: #FFFFFF;
}

.btn-logout {
  background: transparent;
  color: #FFFFFF;
  border: 1px solid rgba(255, 255, 255, 0.7);
  padding: clamp(8px, 0.6vw, 11px) clamp(16px, 1.2vw, 22px);
  border-radius: 6px;
  font-size: clamp(13px, 0.9vw, 16px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #FFFFFF;
}

.navbar-light {
  background-color: #FFFFFF;
  border-bottom: 1px solid var(--color-border);
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--color-navy);
  text-decoration: none;
}

.brand-logo .icon-cap {
  width: clamp(38px, 2.6vw, 48px);
  height: clamp(38px, 2.6vw, 48px);
}

.brand-logo .brand-text {
  font-size: clamp(17px, 1.1vw, 21px);
  font-weight: 800;
  line-height: 1.15;
}

.nav-links {
  display: flex;
  gap: clamp(28px, 2.6vw, 52px);
}

.nav-link {
  color: #0B2A4A;
  font-size: clamp(15px, 1vw, 19px);
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s;
}

.nav-link:hover, .nav-link.active {
  color: #14A098;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.btn-back-home {
  color: var(--color-navy);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.btn-back-home:hover {
  color: var(--color-primary);
}

.btn-login-outline {
  color: #154C86;
  border: 2px solid #154C86;
  padding: clamp(8px, 0.6vw, 11px) clamp(20px, 1.5vw, 28px);
  border-radius: 10px;
  font-size: clamp(14px, 0.95vw, 18px);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-login-outline:hover {
  background-color: #154C86;
  color: white;
}

.btn-register-solid {
  background-color: #154C86;
  color: white;
  border: 2px solid #154C86;
  padding: clamp(8px, 0.6vw, 11px) clamp(20px, 1.5vw, 28px);
  border-radius: 10px;
  font-size: clamp(14px, 0.95vw, 18px);
  font-weight: 600;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-register-solid:hover {
  background-color: #0F3A68;
}

.main-content {
  flex: 1;
}

@media (max-width: 900px) {
  .nav-links,
  .nav-links-white {
    display: none;
  }
  .nav-actions .btn-icon {
    display: none;
  }
  .btn-login-outline,
  .btn-register-solid {
    padding: 7px 12px;
    font-size: 13px;
  }
}
</style>
