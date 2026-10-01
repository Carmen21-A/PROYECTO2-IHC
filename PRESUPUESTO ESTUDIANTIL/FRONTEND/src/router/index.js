import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import RecuperarView from '../views/RecuperarView.vue'
import MovimientosView from '../views/MovimientosView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { public: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { public: true }
  },
  {
    path: '/registro',
    name: 'Registro',
    component: RegisterView,
    meta: { public: true }
  },
  {
    path: '/recuperar',
    name: 'Recuperar',
    component: RecuperarView,
    meta: { public: true }
  },
  {
    path: '/movimientos',
    name: 'Movimientos',
    component: MovimientosView,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})

async function validarSesion(token) {
  try {
    const res = await fetch('http://localhost:8000/auth/me', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) return false
    localStorage.setItem('usuario', JSON.stringify(await res.json()))
    window.dispatchEvent(new Event('usuario-autenticado'))
    return true
  } catch (e) {
    return false
  }
}

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth) {
    if (token && await validarSesion(token)) {
      next()
    } else {
      localStorage.removeItem('token')
      localStorage.removeItem('usuario')
      next({ name: 'Login', query: { redirect: to.fullPath } })
    }
  } else if ((to.name === 'Login' || to.name === 'Registro') && token) {
    next({ name: 'Movimientos' })
  } else {
    next()
  }
})

export default router
