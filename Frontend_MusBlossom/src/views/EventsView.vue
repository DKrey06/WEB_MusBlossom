<template>
  <div class="events-view">
    <div class="events-header">
      <h1>Музыкальные события</h1>
      <p>Концерты, фестивали и встречи в вашем городе</p>
    </div>

    <div class="events-container">
      <div class="events-filters">
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск событий, артистов, городов..."
            @input="searchEvents"
          />
          <span class="search-icon">🔍</span>
        </div>

        <div class="filter-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="filter-options">
          <div class="filter-group">
            <label>Город:</label>
            <select v-model="selectedCity" @change="filterEvents">
              <option value="">Все города</option>
              <option v-for="city in cities" :key="city" :value="city">
                {{ city }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Месяц:</label>
            <select v-model="selectedMonth" @change="filterEvents">
              <option value="">Все месяцы</option>
              <option v-for="month in months" :key="month.value" :value="month.value">
                {{ month.label }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Жанр:</label>
            <select v-model="selectedGenre" @change="filterEvents">
              <option value="">Все жанры</option>
              <option v-for="genre in genres" :key="genre" :value="genre">
                {{ genre }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Загрузка событий...</p>
      </div>

      <div v-else class="events-content">
        <div class="featured-event" v-if="featuredEvent">
          <div
            class="featured-bg"
            :style="{ backgroundImage: `url(${featuredEvent.image})` }"
          ></div>
          <div class="featured-overlay">
            <div class="featured-content">
              <span class="featured-badge">🔥 Событие месяца</span>
              <h2>{{ featuredEvent.title }}</h2>
              <div class="featured-details">
                <span class="detail">📅 {{ featuredEvent.date }}</span>
                <span class="detail">📍 {{ featuredEvent.location }}</span>
                <span class="detail">🎵 {{ featuredEvent.genre }}</span>
              </div>
              <p class="featured-description">{{ featuredEvent.description }}</p>
              <div class="featured-actions">
                <button class="btn btn-primary" @click="viewEvent(featuredEvent)">Подробнее</button>
                <button class="btn btn-secondary" @click="saveEvent(featuredEvent)">
                  💾 Сохранить
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="events-grid">
          <div
            v-for="event in filteredEvents"
            :key="event.id"
            class="event-card"
            @click="viewEvent(event)"
          >
            <div class="event-image">
              <img :src="event.image" :alt="event.title" />
              <div class="event-date">
                <span class="day">{{ formatDay(event.date) }}</span>
                <span class="month">{{ formatMonth(event.date) }}</span>
              </div>
            </div>
            <div class="event-info">
              <h3>{{ event.title }}</h3>
              <div class="event-meta">
                <span class="meta-item">📍 {{ event.city }}</span>
                <span class="meta-item">🎵 {{ event.genre }}</span>
                <span class="meta-item">🎫 {{ event.price }}</span>
              </div>
              <p class="event-description">{{ event.description }}</p>
              <div class="event-stats">
                <span class="stat">👥 {{ event.attending }} идут</span>
                <span class="stat">💬 {{ event.comments }} обсуждения</span>
              </div>
              <div class="event-actions">
                <button
                  class="btn btn-small"
                  :class="{ 'btn-primary': event.isGoing }"
                  @click.stop="toggleGoing(event)"
                >
                  {{ event.isGoing ? '✅ Я иду' : 'Я пойду' }}
                </button>
                <button class="btn btn-small btn-secondary" @click.stop="shareEvent(event)">
                  ↪️ Поделиться
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredEvents.length === 0" class="no-events">
          <div class="no-events-icon">📅</div>
          <h3>Событий не найдено</h3>
          <p>Попробуйте изменить параметры поиска</p>
        </div>
      </div>

      <div class="upcoming-section">
        <h2>📅 Ближайшие события</h2>
        <div class="upcoming-list">
          <div
            v-for="event in upcomingEvents"
            :key="event.id"
            class="upcoming-card"
            @click="viewEvent(event)"
          >
            <div class="upcoming-date">
              <span class="upcoming-day">{{ formatDay(event.date) }}</span>
              <span class="upcoming-month">{{ formatMonth(event.date) }}</span>
            </div>
            <div class="upcoming-info">
              <h4>{{ event.title }}</h4>
              <p>{{ event.city }}, {{ event.venue }}</p>
              <span class="upcoming-time">{{ event.time }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <EventDetailModal
      v-if="selectedEvent"
      :event="selectedEvent"
      @close="selectedEvent = null"
      @save="saveEvent"
      @going="toggleGoing"
    />
  </div>
</template>

<script>
import EventDetailModal from '@/components/EventDetailModal.vue'

export default {
  name: 'EventsView',
  components: {
    EventDetailModal,
  },
  data() {
    return {
      searchQuery: '',
      activeTab: 'concerts',
      selectedCity: '',
      selectedMonth: '',
      selectedGenre: '',
      loading: false,
      events: [],
      selectedEvent: null,
      tabs: [
        { id: 'concerts', label: 'Концерты' },
        { id: 'festivals', label: 'Фестивали' },
        { id: 'meetups', label: 'Встречи' },
        { id: 'workshops', label: 'Мастер-классы' },
        { id: 'saved', label: 'Сохраненные' },
      ],
      cities: [
        'Москва',
        'Санкт-Петербург',
        'Новосибирск',
        'Екатеринбург',
        'Казань',
        'Нижний Новгород',
        'Краснодар',
        'Сочи',
        'Владивосток',
      ],
      months: [
        { value: '01', label: 'Январь' },
        { value: '02', label: 'Февраль' },
        { value: '03', label: 'Март' },
        { value: '04', label: 'Апрель' },
        { value: '05', label: 'Май' },
        { value: '06', label: 'Июнь' },
        { value: '07', label: 'Июль' },
        { value: '08', label: 'Август' },
        { value: '09', label: 'Сентябрь' },
        { value: '10', label: 'Октябрь' },
        { value: '11', label: 'Ноябрь' },
        { value: '12', label: 'Декабрь' },
      ],
      genres: [
        'Рок',
        'Поп',
        'Хип-хоп',
        'Джаз',
        'Классика',
        'Электроника',
        'Метал',
        'Инди',
        'Фолк',
        'R&B',
        'Соул',
      ],
    }
  },
  computed: {
    featuredEvent() {
      return this.events.find((e) => e.featured) || this.events[0]
    },
    filteredEvents() {
      let filtered = this.events

      if (this.activeTab === 'saved') {
        const savedEvents = JSON.parse(localStorage.getItem('saved_events') || '[]')
        filtered = this.events.filter((e) => savedEvents.includes(e.id))
      } else if (this.activeTab !== 'all') {
        filtered = filtered.filter((e) => e.type === this.activeTab)
      }

      if (this.selectedCity) {
        filtered = filtered.filter((e) => e.city === this.selectedCity)
      }

      if (this.selectedMonth) {
        filtered = filtered.filter((e) => e.date.includes(`-${this.selectedMonth}-`))
      }

      if (this.selectedGenre) {
        filtered = filtered.filter((e) => e.genre === this.selectedGenre)
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(
          (e) =>
            e.title.toLowerCase().includes(query) ||
            e.description.toLowerCase().includes(query) ||
            e.artist.toLowerCase().includes(query) ||
            e.city.toLowerCase().includes(query),
        )
      }

      return filtered
    },
    upcomingEvents() {
      const now = new Date()
      return this.events
        .filter((e) => new Date(e.date) > now)
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(0, 5)
    },
  },
  async mounted() {
    await this.loadEvents()
  },
  methods: {
    async loadEvents() {
      this.loading = true
      try {
        const response = await fetch('/api/events')
        const data = await response.json()

        if (data.success) {
          this.events = data.events
        } else {
          this.events = this.getMockEvents()
        }
      } catch (error) {
        console.error('Error loading events:', error)
        this.events = this.getMockEvents()
      } finally {
        this.loading = false
      }
    },

    getMockEvents() {
      return [
        {
          id: 1,
          title: 'Miyagi & Andy Panda Live',
          artist: 'Miyagi & Andy Panda',
          description: 'Грандиозный концерт культовой группы',
          date: '2024-12-15',
          time: '19:00',
          city: 'Москва',
          venue: 'VTB Арена',
          genre: 'Хип-хоп',
          type: 'concerts',
          price: 'от 2000 ₽',
          attending: 1245,
          comments: 89,
          isGoing: false,
          featured: true,
          image:
            'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&h=400&fit=crop',
        },
        {
          id: 2,
          title: 'ROCK FEST 2024',
          artist: 'Разные исполнители',
          description: 'Крупнейший рок-фестиваль года',
          date: '2024-07-20',
          time: '12:00',
          city: 'Санкт-Петербург',
          venue: 'Парк 300-летия',
          genre: 'Рок',
          type: 'festivals',
          price: 'от 3000 ₽',
          attending: 5680,
          comments: 234,
          isGoing: true,
          image:
            'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=600&h=400&fit=crop',
        },
        {
          id: 3,
          title: 'Джаз в Гнесинке',
          artist: 'Московский джаз-оркестр',
          description: 'Вечер классического джаза',
          date: '2024-06-10',
          time: '20:00',
          city: 'Москва',
          venue: 'Концертный зал Гнесинки',
          genre: 'Джаз',
          type: 'concerts',
          price: 'от 1500 ₽',
          attending: 320,
          comments: 45,
          isGoing: false,
          image:
            'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600&h=400&fit=crop',
        },
        {
          id: 4,
          title: 'Музыкальный воркшоп',
          artist: 'Профессиональные музыканты',
          description: 'Мастер-класс по игре на гитаре',
          date: '2024-05-25',
          time: '14:00',
          city: 'Екатеринбург',
          venue: 'Арт-пространство "Волна"',
          genre: 'Разное',
          type: 'workshops',
          price: 'Бесплатно',
          attending: 45,
          comments: 12,
          isGoing: false,
          image:
            'https://images.unsplash.com/photo-1525201548942-d8732f6617a0?w=600&h=400&fit=crop',
        },
        {
          id: 5,
          title: 'HIP-HOP NIGHT',
          artist: 'Лучшие диджеи города',
          description: 'Ночная вечеринка для любителей хип-хопа',
          date: '2024-08-05',
          time: '23:00',
          city: 'Казань',
          venue: 'Клуб "База"',
          genre: 'Хип-хоп',
          type: 'meetups',
          price: 'от 500 ₽',
          attending: 890,
          comments: 67,
          isGoing: false,
          image:
            'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop',
        },
      ]
    },

    formatDay(dateString) {
      const date = new Date(dateString)
      return date.getDate()
    },

    formatMonth(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU', { month: 'short' })
    },

    viewEvent(event) {
      this.selectedEvent = event
    },

    toggleGoing(event) {
      event.isGoing = !event.isGoing
      if (event.isGoing) {
        event.attending++
      } else {
        event.attending--
      }
    },

    saveEvent(event) {
      const savedEvents = JSON.parse(localStorage.getItem('saved_events') || '[]')
      if (!savedEvents.includes(event.id)) {
        savedEvents.push(event.id)
        localStorage.setItem('saved_events', JSON.stringify(savedEvents))
        alert('Событие сохранено!')
      } else {
        alert('Событие уже сохранено')
      }
    },

    shareEvent(event) {
      const text = `Смотри ${event.title} в ${event.city} ${event.date}! 🎤`
      if (navigator.share) {
        navigator.share({
          title: event.title,
          text: text,
          url: window.location.href,
        })
      } else {
        navigator.clipboard.writeText(text)
        alert('Информация о событии скопирована!')
      }
    },

    searchEvents() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {}, 300)
    },

    filterEvents() {},
  },
}
</script>

<style scoped>
.events-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.events-header {
  text-align: center;
  margin: 2rem 0 3rem;
}

.events-header h1 {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.events-header p {
  color: #b0b0b0;
  font-size: 1.2rem;
}

.events-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.events-filters {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
}

.search-box {
  position: relative;
  margin-bottom: 1.5rem;
}

.search-box input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 3rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.filter-tabs button {
  padding: 0.8rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.3s;
}

.filter-tabs button:hover {
  background: rgba(138, 43, 226, 0.1);
  border-color: #8a2be2;
}

.filter-tabs button.active {
  background: rgba(138, 43, 226, 0.2);
  border-color: #8a2be2;
  color: #8a2be2;
}

.filter-options {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.filter-group select {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  min-width: 150px;
}

.loading {
  text-align: center;
  padding: 4rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(138, 43, 226, 0.3);
  border-radius: 50%;
  border-top-color: #8a2be2;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.featured-event {
  position: relative;
  height: 400px;
  border-radius: 15px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.featured-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-size: cover;
  background-position: center;
  filter: brightness(0.6);
}

.featured-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to right, rgba(0, 0, 0, 0.8), transparent);
  display: flex;
  align-items: center;
  padding: 3rem;
}

.featured-content {
  max-width: 600px;
}

.featured-badge {
  display: inline-block;
  background: #ff4757;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.featured-content h2 {
  font-size: 2.5rem;
  color: white;
  margin-bottom: 1rem;
}

.featured-details {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
  color: #b0b0b0;
}

.featured-description {
  color: #b0b0b0;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.featured-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
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

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.event-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.event-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
}

.event-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.event-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.event-date {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.5rem;
  border-radius: 10px;
  text-align: center;
  min-width: 50px;
}

.day {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
}

.month {
  font-size: 0.9rem;
}

.event-info {
  padding: 1.5rem;
}

.event-info h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.event-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  color: #888;
  font-size: 0.9rem;
  flex-wrap: wrap;
}

.event-description {
  color: #b0b0b0;
  margin-bottom: 1rem;
  line-height: 1.5;
  font-size: 0.95rem;
}

.event-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.event-actions {
  display: flex;
  gap: 0.5rem;
}

.no-events {
  text-align: center;
  padding: 4rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 15px;
}

.no-events-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.no-events h3 {
  color: white;
  margin-bottom: 0.5rem;
}

.no-events p {
  color: #b0b0b0;
}

.upcoming-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
}

.upcoming-section h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.upcoming-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.upcoming-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s;
}

.upcoming-card:hover {
  background: rgba(255, 255, 255, 0.05);
}

.upcoming-date {
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  padding: 0.8rem;
  border-radius: 10px;
  text-align: center;
  min-width: 60px;
}

.upcoming-day {
  display: block;
  font-size: 1.2rem;
  font-weight: bold;
}

.upcoming-month {
  font-size: 0.8rem;
}

.upcoming-info {
  flex: 1;
}

.upcoming-info h4 {
  color: white;
  margin-bottom: 0.3rem;
  font-size: 1.1rem;
}

.upcoming-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.upcoming-time {
  color: #8a2be2;
  font-size: 0.9rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .featured-event {
    height: 300px;
  }

  .featured-overlay {
    padding: 1.5rem;
  }

  .featured-content h2 {
    font-size: 1.8rem;
  }

  .events-grid {
    grid-template-columns: 1fr;
  }

  .filter-options {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-group select {
    width: 100%;
  }
}
</style>
