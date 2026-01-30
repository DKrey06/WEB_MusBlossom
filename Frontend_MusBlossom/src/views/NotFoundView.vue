<template>
  <div class="not-found-view">
    <div class="not-found-container">
      <div class="not-found-content">
        <h1 class="error-code">404</h1>
        <h2 class="error-title">Страница не найдена</h2>
        <p class="error-description">Запрашиваемая страница не существует или была перемещена.</p>

        <div class="not-found-actions">
          <router-link to="/" class="btn btn-primary"> На главную </router-link>
          <button @click="goBack" class="btn btn-secondary">Назад</button>
        </div>
      </div>

      <div class="not-found-illustration">
        <div class="illustration">
          <div class="music-note note-1">♪</div>
          <div class="music-note note-2">♫</div>
          <div class="music-note note-3">♬</div>
          <div class="number">4</div>
          <div class="number">0</div>
          <div class="number">4</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView',
  data() {
    return {
      searchQuery: '',
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1)
    },
    performSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push({
          path: '/search',
          query: { q: this.searchQuery },
        })
      }
    },
  },
}
</script>

<style scoped>
.not-found-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.not-found-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  max-width: 1200px;
  width: 100%;
  align-items: center;
}

.not-found-content {
  text-align: left;
}

.error-code {
  font-size: 6rem;
  font-weight: 800;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
  line-height: 1;
}

.error-title {
  font-size: 2.5rem;
  color: white;
  margin-bottom: 1rem;
}

.error-description {
  color: #b0b0b0;
  font-size: 1.2rem;
  margin-bottom: 2rem;
  max-width: 500px;
  line-height: 1.6;
}

.not-found-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
}

.btn {
  display: inline-block;
  padding: 1rem 2rem;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border: 1px solid #444;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.not-found-search {
  margin-bottom: 3rem;
}

.not-found-search h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.search-box {
  display: flex;
  gap: 1rem;
}

.search-box input {
  flex: 1;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
}

.search-btn {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  font-size: 1rem;
}

.search-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.not-found-suggestions h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}

.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  text-decoration: none;
  color: #b0b0b0;
  transition: all 0.3s;
}

.suggestion-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
  transform: translateY(-2px);
}

.suggestion-icon {
  font-size: 1.5rem;
}

.suggestion-item span {
  font-size: 1rem;
  font-weight: 500;
}

.not-found-illustration {
  display: flex;
  justify-content: center;
  align-items: center;
}

.illustration {
  position: relative;
  width: 400px;
  height: 300px;
}

.number {
  position: absolute;
  font-size: 10rem;
  font-weight: 800;
  color: rgba(138, 43, 226, 0.1);
}

.number:nth-child(4) {
  left: 0;
  top: 50%;
  transform: translateY(-50%);
}

.number:nth-child(5) {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.number:nth-child(6) {
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

.music-note {
  position: absolute;
  font-size: 3rem;
  color: #8a2be2;
  animation: float 3s ease-in-out infinite;
}

.note-1 {
  top: 20px;
  left: 50px;
  animation-delay: 0s;
}

.note-2 {
  top: 100px;
  right: 80px;
  animation-delay: 1s;
}

.note-3 {
  bottom: 50px;
  left: 100px;
  animation-delay: 2s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(10deg);
  }
}

@media (max-width: 768px) {
  .not-found-container {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2rem;
  }

  .error-code {
    font-size: 4rem;
  }

  .error-title {
    font-size: 2rem;
  }

  .not-found-actions {
    flex-direction: column;
  }

  .suggestions-grid {
    grid-template-columns: 1fr;
  }

  .illustration {
    width: 300px;
    height: 200px;
  }

  .number {
    font-size: 7rem;
  }
}
</style>
