<template>
  <div class="event-detail-modal">
    <div class="modal-overlay" @click="close">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <button class="close-btn" @click="close">✕</button>
          <div class="event-header">
            <div class="event-type-badge" :class="event.type">
              {{ event.type === 'concerts' ? '🎤 Концерт' : '🎪 Фестиваль' }}
            </div>
            <h2>{{ event.title }}</h2>
            <p class="event-artist">
              Исполнитель: <strong>{{ event.artist }}</strong>
            </p>
          </div>
        </div>

        <div class="modal-body">
          <div class="event-main-info">
            <div class="event-image">
              <img :src="event.image" :alt="event.title" />
              <div class="event-date-overlay">
                <div class="event-date-display">
                  <span class="date-day">{{ formatDay(event.date) }}</span>
                  <span class="date-month">{{ formatMonth(event.date) }}</span>
                </div>
                <div class="event-time">{{ event.time }}</div>
              </div>
            </div>
            <div class="event-details">
              <div class="detail-section">
                <h3>Дата и время</h3>
                <p class="detail-value">{{ formatDateFull(event.date) }}</p>
                <p class="detail-subtext">{{ event.time }}</p>
              </div>
              <div class="detail-section">
                <h3>Место проведения</h3>
                <p class="detail-value">{{ event.venue }}</p>
                <p class="detail-subtext">{{ event.city }}, {{ event.country }}</p>
                <p v-if="event.address" class="detail-address">{{ event.address }}</p>
              </div>
              <div class="detail-section">
                <h3>Билеты</h3>
                <div class="ticket-info">
                  <span class="ticket-price">{{ event.price }}</span>
                  <span class="ticket-availability">
                    {{ event.availableTickets }} билетов осталось
                  </span>
                </div>
                <p class="detail-subtext">Быстро раскупаются</p>
              </div>
              <div class="detail-section">
                <h3>Участники</h3>
                <div class="attending-count">
                  <span class="count-value">{{ event.attending }}</span>
                  <span class="count-label">идут на событие</span>
                </div>
                <div class="attending-faces">
                  <img
                    v-for="avatar in event.attendingAvatars"
                    :key="avatar"
                    :src="avatar"
                    class="attending-avatar"
                    alt="Attendee"
                  />
                  <span v-if="event.attending > event.attendingAvatars.length" class="more-count">
                    +{{ event.attending - event.attendingAvatars.length }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="event-description">
            <h3>О событии</h3>
            <p>{{ event.description }}</p>
            <div v-if="event.lineup.length" class="event-lineup">
              <h4>Состав</h4>
              <div class="lineup-artists">
                <span v-for="artist in event.lineup" :key="artist" class="lineup-artist">
                  {{ artist }}
                </span>
              </div>
            </div>
          </div>

          <div v-if="event.schedule.length" class="event-schedule">
            <h3>Расписание</h3>
            <div class="schedule-timeline">
              <div v-for="item in event.schedule" :key="item.time" class="schedule-item">
                <div class="schedule-time">{{ item.time }}</div>
                <div class="schedule-content">
                  <h4>{{ item.title }}</h4>
                  <p>{{ item.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="event-location">
            <h3>Как добраться</h3>
            <div class="location-map">
              <div class="map-placeholder">
                <div class="map-icon">🗺️</div>
                <p>{{ event.venue }}, {{ event.city }}</p>
                <small>{{
                  event.address || 'Точный адрес будет отправлен после покупки билета'
                }}</small>
              </div>
              <div class="location-directions">
                <div class="direction">
                  <span class="direction-icon"></span>
                  <div class="direction-info">
                    <strong>Метро</strong>
                    <p>Станция «{{ event.metro || 'Центральная' }}», 5 минут пешком</p>
                  </div>
                </div>
                <div class="direction">
                  <span class="direction-icon"></span>
                  <div class="direction-info">
                    <strong>Автомобиль</strong>
                    <p>
                      Парковка на {{ event.parking || '500' }} мест,
                      {{ event.parkingPrice || '300 ₽/час' }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="event-tickets">
            <h3>Выберите билет</h3>
            <div class="ticket-options">
              <div
                v-for="ticket in event.ticketOptions"
                :key="ticket.type"
                class="ticket-option"
                :class="{ recommended: ticket.recommended }"
              >
                <div class="ticket-header">
                  <h4>{{ ticket.name }}</h4>
                  <span v-if="ticket.recommended" class="recommended-badge">⭐ Рекомендуем</span>
                </div>
                <p class="ticket-description">{{ ticket.description }}</p>
                <div class="ticket-features">
                  <span v-for="feature in ticket.features" :key="feature" class="ticket-feature">
                    ✓ {{ feature }}
                  </span>
                </div>
                <div class="ticket-footer">
                  <div class="ticket-price">
                    <span class="price">{{ ticket.price }} ₽</span>
                    <span v-if="ticket.originalPrice" class="original-price">
                      {{ ticket.originalPrice }} ₽
                    </span>
                  </div>
                  <button
                    class="btn btn-small"
                    :class="ticket.recommended ? 'btn-primary' : 'btn-secondary'"
                    @click="selectTicket(ticket)"
                  >
                    {{ ticket.available ? 'Выбрать' : 'Распродано' }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="event-social-proof">
            <h3>Кто идет?</h3>
            <div class="attendees-list">
              <div v-for="attendee in event.attendees" :key="attendee.id" class="attendee">
                <img :src="attendee.avatar" class="attendee-avatar" alt="Avatar" />
                <div class="attendee-info">
                  <h4>{{ attendee.name }}</h4>
                  <p>{{ attendee.bio }}</p>
                  <div class="attendee-tags">
                    <span class="tag">{{ attendee.genre }}</span>
                    <span class="tag">{{ attendee.city }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="event.previousReviews.length" class="event-reviews">
            <h3>Отзывы о предыдущих концертах</h3>
            <div class="reviews-carousel">
              <div v-for="review in event.previousReviews" :key="review.id" class="review-card">
                <div class="review-header">
                  <img :src="review.avatar" class="review-avatar" alt="Avatar" />
                  <div class="reviewer-info">
                    <h4>{{ review.name }}</h4>
                    <div class="review-rating">
                      <span class="stars">★★★★★</span>
                      <span class="review-date">{{ review.date }}</span>
                    </div>
                  </div>
                </div>
                <p class="review-text">"{{ review.text }}"</p>
                <div class="review-photos">
                  <img
                    v-for="photo in review.photos"
                    :key="photo"
                    :src="photo"
                    class="review-photo"
                    alt="Photo"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <div class="event-actions">
            <div class="action-buttons">
              <button class="btn btn-secondary" @click="saveEvent">
                {{ event.isSaved ? '💾 Сохранено' : '💾 Сохранить' }}
              </button>
              <button class="btn btn-secondary" @click="shareEvent">↪️ Поделиться</button>
              <button class="btn btn-secondary" @click="addToCalendar">В календарь</button>
              <button
                class="btn"
                :class="event.isGoing ? 'btn-primary' : 'btn-secondary'"
                @click="toggleGoing"
              >
                {{ event.isGoing ? '✅ Я иду' : '👋 Я пойду' }}
              </button>
            </div>
            <div class="buy-ticket-section">
              <div class="selected-ticket" v-if="selectedTicket">
                <h4>Выбранный билет:</h4>
                <div class="ticket-summary">
                  <span class="ticket-name">{{ selectedTicket.name }}</span>
                  <span class="ticket-price">{{ selectedTicket.price }} ₽</span>
                </div>
              </div>
              <button class="btn btn-primary btn-large" @click="buyTickets">Купить билеты</button>
              <p class="secure-payment">Безопасная оплата • Возврат билетов • Электронные билеты</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EventDetailModal',
  props: {
    event: {
      type: Object,
      required: true,
      default: () => ({
        id: 1,
        title: 'Miyagi & Andy Panda Live',
        artist: 'Miyagi & Andy Panda',
        description:
          'Грандиозный концерт культовой группы с программой из лучших хитов. Уникальное световое шоу и живой звук. На концерте будет представлена новая программа, а также классические треки, которые полюбились миллионам поклонников.',
        type: 'concerts',
        date: '2024-12-15',
        time: '19:00',
        venue: 'VTB Арена',
        city: 'Москва',
        country: 'Россия',
        address: 'ул. Лужники, 24',
        metro: 'Спортивная',
        parking: 500,
        parkingPrice: '300 ₽/час',
        price: 'от 2000 ₽',
        availableTickets: 245,
        attending: 1245,
        isGoing: false,
        isSaved: false,
        image: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&h=400&fit=crop',
        attendingAvatars: [
          'https://i.pravatar.cc/150?img=1',
          'https://i.pravatar.cc/150?img=2',
          'https://i.pravatar.cc/150?img=3',
          'https://i.pravatar.cc/150?img=4',
          'https://i.pravatar.cc/150?img=5',
        ],
        lineup: ['Miyagi', 'Andy Panda', 'Специальные гости', 'DJ-сет'],
        schedule: [
          {
            time: '18:00',
            title: 'Начало',
            description: 'Открытие дверей, welcome-зона',
          },
          {
            time: '19:30',
            title: 'Открывающий артист',
            description: 'Выступление специального гостя',
          },
          {
            time: '20:30',
            title: 'Основное выступление',
            description: 'Miyagi & Andy Panda - лучшие хиты',
          },
          {
            time: '22:00',
            title: 'Энкор',
            description: 'Дополнительный сет по просьбам зрителей',
          },
        ],
        ticketOptions: [
          {
            type: 'standard',
            name: 'Стандарт',
            description: 'Основная зона, сидячие места',
            price: 2000,
            originalPrice: 2500,
            features: ['Основная зона', 'Сидячее место', 'Общая гардеробная'],
            available: true,
            recommended: false,
          },
          {
            type: 'vip',
            name: '⭐ VIP',
            description: 'Партер, фан-зона, мерч',
            price: 5000,
            originalPrice: 6000,
            features: ['Партер', 'Фан-зона', 'Мерч-пакет', 'Отдельный вход'],
            available: true,
            recommended: true,
          },
          {
            type: 'premium',
            name: 'Премиум',
            description: 'Первые ряды, meet & greet',
            price: 10000,
            originalPrice: 12000,
            features: ['Первые ряды', 'Meet & greet', 'Фото с артистами', 'VIP-бар'],
            available: false,
            recommended: false,
          },
        ],
        attendees: [
          {
            id: 1,
            name: 'Алексей',
            avatar: 'https://i.pravatar.cc/150?img=12',
            bio: 'Фанат хип-хопа, жду этот концерт весь год!',
            genre: 'Хип-хоп',
            city: 'Москва',
          },
          {
            id: 2,
            name: 'Мария',
            avatar: 'https://i.pravatar.cc/150?img=5',
            bio: 'Люблю живые концерты, это будет мой 3-й раз на Miyagi',
            genre: 'Поп',
            city: 'Санкт-Петербург',
          },
          {
            id: 3,
            name: 'Дмитрий',
            avatar: 'https://i.pravatar.cc/150?img=8',
            bio: 'Еду специально из Казани на этот концерт',
            genre: 'Рок',
            city: 'Казань',
          },
        ],
        previousReviews: [
          {
            id: 1,
            name: 'Иван',
            avatar: 'https://i.pravatar.cc/150?img=3',
            date: 'Май 2023',
            text: 'Лучший концерт в жизни! Энергия зашкаливала, ребята отыграли на максимум.',
            photos: [
              'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=200&h=150&fit=crop',
              'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=200&h=150&fit=crop',
            ],
          },
          {
            id: 2,
            name: 'Анна',
            avatar: 'https://i.pravatar.cc/150?img=6',
            date: 'Июнь 2023',
            text: 'Организация на высшем уровне, звук чистый, световое шоу нереальное!',
            photos: [
              'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=200&h=150&fit=crop',
            ],
          },
        ],
      }),
    },
  },
  emits: ['close', 'save', 'going', 'buy-tickets'],
  data() {
    return {
      selectedTicket: null,
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },

    saveEvent() {
      this.event.isSaved = !this.event.isSaved
      this.$emit('save', this.event)
    },

    shareEvent() {
      const shareText = `Смотри ${this.event.artist} в ${this.event.city} ${this.formatDateFull(this.event.date)}! 🎤`
      const shareUrl = window.location.href

      if (navigator.share) {
        navigator.share({
          title: this.event.title,
          text: shareText,
          url: shareUrl,
        })
      } else {
        navigator.clipboard.writeText(`${shareText}\n${shareUrl}`)
        alert('Информация о событии скопирована!')
      }
    },

    addToCalendar() {
      alert('Событие добавлено в ваш календарь')
    },

    toggleGoing() {
      this.event.isGoing = !this.event.isGoing
      if (this.event.isGoing) {
        this.event.attending++
      } else {
        this.event.attending--
      }
      this.$emit('going', this.event)
    },

    selectTicket(ticket) {
      if (ticket.available) {
        this.selectedTicket = ticket
      }
    },

    buyTickets() {
      if (!this.selectedTicket) {
        alert('Пожалуйста, выберите тип билета')
        return
      }

      this.$emit('buy-tickets', {
        event: this.event,
        ticket: this.selectedTicket,
      })
    },

    formatDay(dateString) {
      const date = new Date(dateString)
      return date.getDate()
    },

    formatMonth(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU', { month: 'short' })
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
  },
}
</script>

<style scoped>
.event-detail-modal {
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
  border-radius: 20px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  padding: 2rem 2rem 1.5rem;
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.1), rgba(75, 0, 130, 0.1));
  border-radius: 20px 20px 0 0;
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

.event-header {
  text-align: center;
}

.event-type-badge {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 600;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
}

.event-type-badge.concerts {
  background: rgba(255, 71, 87, 0.2);
  color: #ff4757;
}

.event-type-badge.festivals {
  background: rgba(30, 144, 255, 0.2);
  color: #1e90ff;
}

.modal-header h2 {
  font-size: 2rem;
  color: white;
  margin-bottom: 0.5rem;
}

.event-artist {
  color: #b0b0b0;
  font-size: 1.1rem;
}

.modal-body {
  padding: 2rem;
}

.event-main-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}

.event-image {
  position: relative;
  border-radius: 15px;
  overflow: hidden;
  height: 300px;
}

.event-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.event-date-overlay {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 1rem;
  border-radius: 10px;
  text-align: center;
  min-width: 80px;
}

.event-date-display {
  margin-bottom: 0.5rem;
}

.date-day {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  line-height: 1;
}

.date-month {
  font-size: 1rem;
  text-transform: uppercase;
}

.event-time {
  font-size: 0.9rem;
  color: #8a2be2;
  font-weight: 500;
}

.event-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-section {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.detail-section h3 {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-value {
  color: white;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  display: block;
}

.detail-subtext {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.detail-address {
  color: #888;
  font-size: 0.9rem;
  font-style: italic;
}

.ticket-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.ticket-price {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.ticket-availability {
  color: #2ed573;
  font-size: 0.9rem;
  font-weight: 500;
}

.attending-count {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.count-value {
  font-size: 2rem;
  font-weight: bold;
  color: #8a2be2;
}

.count-label {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.attending-faces {
  display: flex;
  align-items: center;
}

.attending-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #1e1e2e;
  margin-left: -10px;
}

.attending-avatar:first-child {
  margin-left: 0;
}

.more-count {
  margin-left: 10px;
  color: #888;
  font-size: 0.9rem;
}

.event-description {
  margin-bottom: 3rem;
}

.event-description h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.event-description p {
  color: #b0b0b0;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.event-lineup {
  margin-top: 1.5rem;
}

.event-lineup h4 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.lineup-artists {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.lineup-artist {
  padding: 0.5rem 1rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 20px;
  font-size: 0.9rem;
}

.event-schedule {
  margin-bottom: 3rem;
}

.event-schedule h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.schedule-timeline {
  position: relative;
  padding-left: 2rem;
}

.schedule-timeline::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: rgba(138, 43, 226, 0.3);
}

.schedule-item {
  position: relative;
  margin-bottom: 2rem;
  padding-left: 1.5rem;
}

.schedule-item:last-child {
  margin-bottom: 0;
}

.schedule-item::before {
  content: '';
  position: absolute;
  left: -5px;
  top: 5px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #8a2be2;
  border: 2px solid #1e1e2e;
}

.schedule-time {
  color: #8a2be2;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.schedule-content {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1rem;
}

.schedule-content h4 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.schedule-content p {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.event-location {
  margin-bottom: 3rem;
}

.event-location h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.location-map {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 15px;
  overflow: hidden;
}

.map-placeholder {
  height: 200px;
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.1), rgba(75, 0, 130, 0.1));
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
}

.map-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.map-placeholder p {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.map-placeholder small {
  color: #888;
  font-size: 0.9rem;
}

.location-directions {
  padding: 1.5rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.direction {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.direction-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.direction-info strong {
  display: block;
  color: white;
  margin-bottom: 0.3rem;
  font-size: 1rem;
}

.direction-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.event-tickets {
  margin-bottom: 3rem;
}

.event-tickets h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.ticket-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.ticket-option {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1.5rem;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.ticket-option:hover {
  background: rgba(255, 255, 255, 0.05);
}

.ticket-option.recommended {
  border-color: #8a2be2;
  background: rgba(138, 43, 226, 0.1);
  position: relative;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.ticket-header h4 {
  color: white;
  font-size: 1.2rem;
}

.recommended-badge {
  background: #8a2be2;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 500;
}

.ticket-description {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.ticket-features {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.ticket-feature {
  color: #888;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.ticket-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ticket-price {
  display: flex;
  flex-direction: column;
}

.ticket-price .price {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.ticket-price .original-price {
  color: #888;
  text-decoration: line-through;
  font-size: 0.9rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
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

.event-social-proof {
  margin-bottom: 3rem;
}

.event-social-proof h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.attendees-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.attendee {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.attendee-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.attendee-info h4 {
  color: white;
  margin-bottom: 0.3rem;
  font-size: 1.1rem;
}

.attendee-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.attendee-tags {
  display: flex;
  gap: 0.5rem;
}

.attendee-tags .tag {
  padding: 0.2rem 0.6rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 15px;
  font-size: 0.8rem;
}

.event-reviews {
  margin-bottom: 3rem;
}

.event-reviews h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.reviews-carousel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.review-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1.5rem;
}

.review-header {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

.review-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.reviewer-info h4 {
  color: white;
  margin-bottom: 0.2rem;
  font-size: 1rem;
}

.review-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.review-rating .stars {
  color: #ffd700;
  font-size: 0.9rem;
}

.review-date {
  color: #888;
  font-size: 0.8rem;
}

.review-text {
  color: #b0b0b0;
  font-style: italic;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.review-photos {
  display: flex;
  gap: 0.5rem;
}

.review-photo {
  width: 60px;
  height: 60px;
  border-radius: 5px;
  object-fit: cover;
}

.modal-footer {
  padding: 2rem;
  border-top: 1px solid #333;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0 0 20px 20px;
}

.event-actions {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.buy-ticket-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.selected-ticket {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(138, 43, 226, 0.1);
  border-radius: 10px;
  width: 100%;
  justify-content: center;
}

.selected-ticket h4 {
  color: white;
  font-size: 1rem;
  margin: 0;
}

.ticket-summary {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.ticket-name {
  color: white;
  font-weight: 500;
}

.ticket-price {
  color: #8a2be2;
  font-weight: bold;
  font-size: 1.2rem;
}

.btn-large {
  padding: 1.2rem 3rem;
  font-size: 1.1rem;
}

.secure-payment {
  color: #888;
  font-size: 0.9rem;
  text-align: center;
}

@media (max-width: 768px) {
  .event-main-info {
    grid-template-columns: 1fr;
  }

  .location-directions {
    grid-template-columns: 1fr;
  }

  .ticket-options {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    justify-content: center;
  }

  .modal-header h2 {
    font-size: 1.5rem;
  }

  .modal-body {
    padding: 1rem;
  }
}
</style>
