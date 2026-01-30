<template>
  <div class="concert-detail-modal">
    <div class="modal-overlay" @click="close">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <button class="close-btn" @click="close">✕</button>
          <div class="concert-header">
            <div class="artist-info">
              <h2>{{ concert.artist_name }}</h2>
              <div class="concert-meta">
                <span class="meta-item"> {{ concert.venue }}</span>
                <span class="meta-item"> {{ concert.city }}, {{ concert.country }}</span>
              </div>
            </div>
            <div class="concert-date">
              <div class="date-large">
                {{ formatDate(concert.date).day }} {{ formatDate(concert.date).month }}
              </div>
              <div class="time">{{ formatTime(concert.date) }}</div>
            </div>
          </div>
        </div>

        <div class="modal-body">
          <div class="concert-image">
            <img :src="concert.image_url || defaultImage" :alt="concert.artist_name" />
          </div>

          <div class="concert-details">
            <div class="detail-section">
              <h3>О событии</h3>
              <p v-if="concert.description">{{ concert.description }}</p>
              <p v-else class="no-description">Описание события скоро появится</p>
            </div>

            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label"> Место</span>
                <span class="detail-value">{{ concert.venue }}</span>
                <small>{{ concert.address || 'Адрес уточняется' }}</small>
              </div>

              <div class="detail-item">
                <span class="detail-label">Дата</span>
                <span class="detail-value">{{ formatDateFull(concert.date) }}</span>
                <small>{{ formatTime(concert.date) }}</small>
              </div>

              <div class="detail-item">
                <span class="detail-label">Цены</span>
                <span class="detail-value">{{ concert.price_range || 'от 1000 ₽' }}</span>
                <small>Билеты от партнеров</small>
              </div>

              <div class="detail-item">
                <span class="detail-label">Доступно</span>
                <span class="detail-value">{{ availableTickets }} билетов</span>
                <small>Быстро раскупаются</small>
              </div>
            </div>

            <div v-if="lineup.length" class="detail-section">
              <h3>Состав</h3>
              <div class="lineup">
                <div v-for="artist in lineup" :key="artist" class="lineup-item">
                  {{ artist }}
                </div>
              </div>
            </div>

            <div class="detail-section">
              <h3>Билеты</h3>
              <div class="ticket-options">
                <div class="ticket-option">
                  <div class="ticket-info">
                    <h4>Стандарт</h4>
                    <p>Основная зона, сидячие места</p>
                  </div>
                  <div class="ticket-price">
                    <span class="price">2000 ₽</span>
                    <button class="btn btn-small" @click="buyTicket('standard')">Купить</button>
                  </div>
                </div>

                <div class="ticket-option recommended">
                  <div class="ticket-info">
                    <h4>VIP</h4>
                    <p>Партер, фан-зона, мерч</p>
                  </div>
                  <div class="ticket-price">
                    <span class="price">5000 ₽</span>
                    <button class="btn btn-small btn-primary" @click="buyTicket('vip')">
                      Купить
                    </button>
                  </div>
                </div>

                <div class="ticket-option">
                  <div class="ticket-info">
                    <h4>Премиум</h4>
                    <p>Первые ряды, meet & greet</p>
                  </div>
                  <div class="ticket-price">
                    <span class="price">10000 ₽</span>
                    <button class="btn btn-small" @click="buyTicket('premium')">Купить</button>
                  </div>
                </div>
              </div>
            </div>

            <div class="map-section" v-if="concert.venue">
              <h3>🗺️ Как добраться</h3>
              <div class="map-placeholder">
                <div class="map-icon">🗺️</div>
                <p>Карта локации: {{ concert.venue }}, {{ concert.city }}</p>
                <small>Точный адрес будет отправлен после покупки билета</small>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn btn-secondary" @click="saveConcert">💾 Сохранить</button>
          <button class="btn btn-secondary" @click="shareConcert">↪️ Поделиться</button>
          <button class="btn btn-primary" @click="buyTickets">🎫 Купить билеты</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConcertDetailModal',
  props: {
    concert: {
      type: Object,
      required: true,
    },
  },
  emits: ['close', 'buy-tickets'],
  data() {
    return {
      defaultImage:
        'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=400&fit=crop',
      lineup: ['Основной артист', 'Специальные гости', 'Ди-джей сет'],
      availableTickets: Math.floor(Math.random() * 100) + 20,
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      const day = date.getDate()
      const month = date.toLocaleString('ru-RU', { month: 'short' })
      return { day, month }
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit',
      })
    },

    formatDateFull(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      })
    },

    buyTickets() {
      this.$emit('buy-tickets', this.concert)
    },

    buyTicket(ticketType) {
      alert(`Вы выбрали билет типа: ${ticketType}`)
      this.buyTickets()
    },

    saveConcert() {
      const saved = JSON.parse(localStorage.getItem('saved_concerts') || '[]')
      if (!saved.find((c) => c.id === this.concert.id)) {
        saved.push(this.concert)
        localStorage.setItem('saved_concerts', JSON.stringify(saved))
        alert('Концерт сохранен в избранное!')
      } else {
        alert('Концерт уже сохранен')
      }
    },

    shareConcert() {
      const text = `Смотри ${this.concert.artist_name} в ${this.concert.city} ${this.formatDateFull(this.concert.date)}! 🎤`
      if (navigator.share) {
        navigator.share({
          title: this.concert.artist_name,
          text: text,
          url: window.location.href,
        })
      } else {
        navigator.clipboard.writeText(text)
        alert('Информация о концерте скопирована!')
      }
    },
  },
}
</script>

<style scoped>
.concert-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
}

.modal-overlay {
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 1rem;
}

.modal-content {
  background: #1e1e2e;
  border-radius: 15px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.2), rgba(75, 0, 130, 0.2));
  border-radius: 15px 15px 0 0;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.concert-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.artist-info h2 {
  font-size: 2rem;
  color: white;
  margin-bottom: 0.5rem;
}

.concert-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  color: #b0b0b0;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.concert-date {
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  min-width: 120px;
}

.date-large {
  font-size: 1.8rem;
  font-weight: bold;
  color: white;
  margin-bottom: 0.3rem;
}

.time {
  color: #8a2be2;
  font-weight: 500;
}

.modal-body {
  padding: 2rem;
}

.concert-image {
  width: 100%;
  height: 300px;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.concert-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.concert-details {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.detail-section h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-section p {
  color: #b0b0b0;
  line-height: 1.6;
}

.no-description {
  color: #666;
  font-style: italic;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.detail-item {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-label {
  color: #888;
  font-size: 0.9rem;
  font-weight: 500;
}

.detail-value {
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
}

.detail-item small {
  color: #666;
  font-size: 0.8rem;
}

.lineup {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.lineup-item {
  padding: 0.5rem 1rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 20px;
  font-size: 0.9rem;
}

.ticket-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ticket-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid #444;
  transition: all 0.3s;
}

.ticket-option:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: #555;
}

.ticket-option.recommended {
  border: 2px solid #8a2be2;
  background: rgba(138, 43, 226, 0.1);
  position: relative;
}

.ticket-option.recommended::before {
  content: '⭐ Рекомендуем';
  position: absolute;
  top: -10px;
  left: 1rem;
  background: #8a2be2;
  color: white;
  padding: 0.2rem 0.8rem;
  border-radius: 10px;
  font-size: 0.8rem;
}

.ticket-info h4 {
  color: white;
  margin-bottom: 0.3rem;
  font-size: 1.1rem;
}

.ticket-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.ticket-price {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
}

.btn {
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
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

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.map-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1.5rem;
}

.map-placeholder {
  text-align: center;
  padding: 2rem;
}

.map-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.map-placeholder p {
  color: white;
  margin-bottom: 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #333;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0 0 15px 15px;
}

.modal-actions .btn {
  flex: 1;
}

@media (max-width: 768px) {
  .concert-header {
    flex-direction: column;
    gap: 1rem;
  }

  .concert-date {
    align-self: flex-start;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .ticket-option {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .ticket-price {
    width: 100%;
    justify-content: space-between;
  }

  .modal-actions {
    flex-direction: column;
  }
}
</style>
