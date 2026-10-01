<template>
  <div class="home-page">

    <section class="hero-section" id="inicio">
      <div class="container hero-inner">
        <div class="hero-content">
          <h1 class="hero-title">
            Toma el control de tu <br />
            dinero universitario
          </h1>
          <p class="hero-subtitle">
            Registra tus gastos en comida, transporte y materiales,
            y haz rendir tu presupuesto sin complicaciones
          </p>

          <div class="hero-actions">
            <router-link to="/registro" class="btn-primary-hero">Empezar Gratis</router-link>
            <router-link to="/login?demo=1" class="btn-demo-hero">
              Ver Demo
              <span class="play-circle">▶</span>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <section class="container features-grid" id="funcionalidades">
      <div class="feature-card">
        <img :src="iconBilletera" alt="" class="feature-icon" />
        <h3 class="feature-title">Control de Gastos</h3>
        <p class="feature-desc">
          Registra cada gasto fácilmente. Categoriza tus compras al instante.
        </p>
      </div>

      <div class="feature-card">
        <img :src="iconHistorial" alt="" class="feature-icon" />
        <h3 class="feature-title">Historial Detallado</h3>
        <p class="feature-desc">
          Visualiza tus patrones de consumo mensuales. Historial claro y organizado.
        </p>
      </div>

      <div class="feature-card">
        <img :src="iconAlertas" alt="" class="feature-icon" />
        <h3 class="feature-title">Alertas de Ahorro</h3>
        <p class="feature-desc">
          Recibe notificaciones y sugerencias para ahorrar dinero. Alcanza tus metas financieras.
        </p>
      </div>
    </section>

  </div>
</template>

<script setup>
import iconBilletera from '../assets/icon-billetera.png'
import iconHistorial from '../assets/icon-historial.png'
import iconAlertas from '../assets/icon-alertas.png'
</script>

<style scoped>
.home-page {
  background-color: #FFFFFF;
  min-height: calc(100vh - 75px);
  padding-bottom: 80px;
}

.hero-section {
  background-color: #C6ECF0;
  background-image: url('../assets/hero-banner.png');
  background-size: cover;
  background-position: right center;
  background-repeat: no-repeat;
}

.hero-inner {
  min-height: clamp(400px, 27vw, 620px);
  display: flex;
  align-items: center;
}

.hero-content {
  max-width: clamp(560px, 42vw, 820px);
  padding: 48px 0;
}

.hero-title {
  font-size: clamp(40px, 3.4vw, 68px);
  font-weight: 800;
  color: #0B2A4A;
  line-height: 1.15;
  margin-bottom: 18px;
}

.hero-subtitle {
  font-size: clamp(17px, 1.25vw, 24px);
  color: #1E293B;
  line-height: 1.55;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-primary-hero {
  background-color: #154C86;
  color: #FFFFFF;
  padding: clamp(14px, 0.9vw, 18px) clamp(34px, 2.4vw, 46px);
  border-radius: 999px;
  font-size: clamp(16px, 1.05vw, 20px);
  font-weight: 700;
  box-shadow: 0 6px 16px rgba(21, 76, 134, 0.3);
  transition: all 0.2s;
}

.btn-primary-hero:hover {
  background-color: #0F3A68;
  transform: translateY(-2px);
}

.btn-demo-hero {
  background-color: rgba(255, 255, 255, 0.7);
  color: #0F766E;
  border: 2px solid #14A098;
  padding: clamp(11px, 0.75vw, 15px) clamp(22px, 1.5vw, 28px) clamp(11px, 0.75vw, 15px) clamp(28px, 2vw, 38px);
  border-radius: 999px;
  font-size: clamp(16px, 1.05vw, 20px);
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
}

.btn-demo-hero:hover {
  background-color: #FFFFFF;
}

.play-circle {
  width: clamp(24px, 1.5vw, 28px);
  height: clamp(24px, 1.5vw, 28px);
  border: 2px solid #14A098;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  padding-left: 2px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: clamp(28px, 2.6vw, 48px);
  margin-top: clamp(40px, 2.6vw, 56px);
}

.feature-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: clamp(26px, 1.8vw, 36px) clamp(26px, 1.8vw, 36px) clamp(30px, 2vw, 40px);
  box-shadow: 0 6px 20px rgba(11, 42, 74, 0.1);
  border: 1px solid #EEF2F6;
  transition: transform 0.25s, box-shadow 0.25s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(11, 42, 74, 0.14);
}

.feature-icon {
  width: clamp(60px, 4vw, 80px);
  height: clamp(60px, 4vw, 80px);
  display: block;
  margin-bottom: 16px;
}

.feature-title {
  font-size: clamp(20px, 1.35vw, 26px);
  font-weight: 800;
  color: #0B2A4A;
  margin-bottom: 8px;
}

.feature-desc {
  font-size: clamp(15px, 0.95vw, 18px);
  color: #334155;
  line-height: 1.5;
}

@media (max-width: 900px) {
  .hero-section {
    background-position: 75% center;
  }
  .hero-content {
    background: rgba(255, 255, 255, 0.75);
    border-radius: 16px;
    padding: 28px 22px;
    margin: 32px 0;
  }
  .hero-title {
    font-size: 34px;
  }
  .hero-actions {
    flex-wrap: wrap;
  }
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
