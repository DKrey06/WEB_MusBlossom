<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>MusBlossom</h3>
        <p>Музыкальная социальная платформа</p>
      </div>
      <div class="footer-section">
        <h3>Ссылки</h3>
        <div class="footer-links">
          <router-link to="/about">О нас</router-link>
          <router-link to="/feedback">Обратная связь</router-link>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 MusBlossom. DKrey_06</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
}
</script>

<style scoped>
.footer {
  background-color: #1a1a2e;
  color: white;
  padding: 3rem 0 1.5rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: 3rem;
}

.footer-section {
  flex: 1;
  min-width: 250px;
  text-align: center;
}

.footer-section h3 {
  margin-bottom: 1.2rem;
  color: #8a2be2;
  font-size: 1.5rem;
}

.footer-section p {
  color: #b0b0b0;
  line-height: 1.6;
  max-width: 300px;
  margin: 0 auto;
}

.footer-links {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}

.footer-section a {
  color: #b0b0b0;
  text-decoration: none;
  transition:
    color 0.3s,
    transform 0.2s;
  padding: 0.3rem 0;
}

.footer-section a:hover {
  color: white;
  transform: translateX(5px);
}

.footer-bottom {
  text-align: center;
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid #2a2a3e;
  color: #b0b0b0;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 2rem;
  }

  .footer-section {
    width: 100%;
  }

  .footer-links {
    align-items: center;
  }
}
</style>
