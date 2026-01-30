<template>
  <div class="concerts-view">
    <div class="concerts-header">
      <h1>🎤 Концерты и события</h1>
      <p>Будь в курсе всех музыкальных событий в твоем городе</p>
    </div>

    <div class="concerts-controls">
      <div class="search-filter">
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск исполнителей, мест, городов..."
            @input="searchConcerts"
          />
          <span class="search-icon">🔍</span>
        </div>

        <div class="filter-buttons">
          <button
            v-for="filter in filters"
            :key="filter.id"
            class="filter-btn"
            :class="{ active: activeFilter === filter.id }"
            @click="applyFilter(filter.id)"
          >
            {{ filter.label }}
          </button>
        </div>
      </div>

      <div class="location-selector">
        <select v-model="selectedCity" @change="loadConcerts">
          <option value="">Все города</option>
          <option v-for="city in cities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
        <select v-model="selectedMonth" @change="loadConcerts">
          <option value="">Все месяцы</option>
          <option v-for="month in months" :key="month.value" :value="month.value">
            {{ month.label }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>

    <div v-else class="concerts-content">
      <section v-if="featuredConcerts.length" class="featured-concerts">
        <h2>🔥 Рекомендуем посетить</h2>
        <div class="featured-slider">
          <div
            v-for="concert in featuredConcerts"
            :key="concert.id"
            class="featured-card"
            :style="{
              backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url(${concert.image_url || defaultConcertImage})`,
            }"
          >
            <div class="featured-content">
              <div class="concert-date">
                <span class="date-day">{{ formatDate(concert.date).day }}</span>
                <span class="date-month">{{ formatDate(concert.date).month }}</span>
              </div>
              <h3>{{ concert.artist_name }}</h3>
              <p class="concert-venue">{{ concert.venue }}</p>
              <p class="concert-location">{{ concert.city }}, {{ concert.country }}</p>
              <div class="concert-price" v-if="concert.price_range">
                {{ concert.price_range }}
              </div>
              <button class="btn btn-primary" @click="buyTickets(concert)">Купить билеты</button>
            </div>
          </div>
        </div>
      </section>

      <section class="all-concerts">
        <div class="section-header">
          <h2>Все концерты</h2>
          <div class="view-toggle">
            <button :class="{ active: viewMode === 'grid' }" @click="viewMode = 'grid'">
              🗂️ Сетка
            </button>
            <button :class="{ active: viewMode === 'list' }" @click="viewMode = 'list'">
              📋 Список
            </button>
          </div>
        </div>

        <div v-if="concerts.length" :class="['concerts-container', viewMode]">
          <div
            v-for="concert in concerts"
            :key="concert.id"
            class="concert-card"
            @click="showConcertDetails(concert)"
          >
            <div class="concert-image">
              <img :src="concert.image_url || defaultConcertImage" :alt="concert.artist_name" />
              <div class="concert-date-badge">
                {{ formatDateShort(concert.date) }}
              </div>
            </div>

            <div class="concert-info">
              <h3>{{ concert.artist_name }}</h3>
              <div class="concert-meta">
                <span class="meta-item">📍 {{ concert.venue }}</span>
                <span class="meta-item">🏙️ {{ concert.city }}</span>
                <span v-if="concert.price_range" class="meta-item">
                  💰 {{ concert.price_range }}
                </span>
              </div>

              <p v-if="concert.description" class="concert-description">
                {{ concert.description.substring(0, 100) }}...
              </p>

              <div class="concert-actions">
                <button class="btn btn-small" @click.stop="buyTickets(concert)">Билеты</button>
                <button class="btn btn-small btn-secondary" @click.stop="saveConcert(concert)">
                  💾 Сохранить
                </button>
                <button class="btn btn-small btn-secondary" @click.stop="shareConcert(concert)">
                  ↪️ Поделиться
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <div class="empty-icon">🎤</div>
          <h3>Концертов не найдено</h3>
          <p>Попробуйте изменить фильтры поиска</p>
        </div>
      </section>

      <section class="calendar-section">
        <h2>🗓️ Календарь событий</h2>
        <div class="calendar">
          <div class="calendar-header">
            <button @click="prevMonth">←</button>
            <h3>{{ currentMonth }} {{ currentYear }}</h3>
            <button @click="nextMonth">→</button>
          </div>
          <div class="calendar-grid">
            <div
              v-for="day in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']"
              :key="day"
              class="calendar-day-header"
            >
              {{ day }}
            </div>
            <div
              v-for="day in calendarDays"
              :key="day.date"
              class="calendar-day"
              :class="{
                today: day.isToday,
                'has-events': day.hasEvents,
                'other-month': !day.isCurrentMonth,
              }"
              @click="showDayEvents(day)"
            >
              <span class="day-number">{{ day.day }}</span>
              <div v-if="day.hasEvents" class="events-indicator">
                <span class="event-dot"></span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="cities-section">
        <h2>🎸 Популярные города</h2>
        <div class="cities-grid">
          <div
            v-for="city in popularCities"
            :key="city.name"
            class="city-card"
            @click="selectCity(city.name)"
          >
            <div class="city-image" :style="{ backgroundImage: `url(${city.image})` }"></div>
            <div class="city-info">
              <h3>{{ city.name }}</h3>
              <span class="city-count">{{ city.count }} событий</span>
            </div>
          </div>
        </div>
      </section>
    </div>

    <ConcertDetailModal
      v-if="selectedConcert"
      :concert="selectedConcert"
      @close="selectedConcert = null"
      @buy-tickets="buyTickets"
    />
  </div>
</template>

<script>
import ConcertDetailModal from '@/components/ConcertDetailModal.vue'

export default {
  name: 'ConcertsView',
  components: {
    ConcertDetailModal,
  },
  data() {
    return {
      loading: false,
      concerts: [],
      featuredConcerts: [],
      searchQuery: '',
      selectedCity: '',
      selectedMonth: '',
      activeFilter: 'upcoming',
      viewMode: 'grid',
      selectedConcert: null,
      filters: [
        { id: 'upcoming', label: 'Предстоящие' },
        { id: 'popular', label: 'Популярные' },
        { id: 'nearby', label: 'Рядом' },
        { id: 'festivals', label: 'Фестивали' },
      ],
      cities: [
        'Москва',
        'Санкт-Петербург',
        'Екатеринбург',
        'Новосибирск',
        'Казань',
        'Нижний Новгород',
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
      popularCities: [
        {
          name: 'Москва',
          count: 42,
          image:
            'https://images.unsplash.com/photo-1513326738677-b964603b136d?w=400&h-300&fit=crop',
        },
        {
          name: 'Санкт-Петербург',
          count: 28,
          image: 'https://images.unsplash.com/photo-1556543697-2fb00d31948a?w=400&h=300&fit=crop',
        },
        {
          name: 'Екатеринбург',
          count: 15,
          image:
            'https://images.unsplash.com/photo-1590411509327-1e2a8e4d02f3?w=400&h=300&fit=crop',
        },
        {
          name: 'Новосибирск',
          count: 12,
          image:
            'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=400&h=300&fit=crop',
        },
      ],
      calendarDays: [],
      currentDate: new Date(),
      defaultConcertImage:
        'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=400&fit=crop',
    }
  },
  computed: {
    currentMonth() {
      return this.currentDate.toLocaleString('ru-RU', { month: 'long' })
    },
    currentYear() {
      return this.currentDate.getFullYear()
    },
  },
  async mounted() {
    await this.loadConcerts()
    this.generateCalendar()
  },
  methods: {
    async loadConcerts() {
      this.loading = true
      try {
        let url = '/api/concerts'
        const params = []

        if (this.selectedCity) params.push(`city=${this.selectedCity}`)
        if (this.selectedMonth) params.push(`month=${this.selectedMonth}`)
        if (this.activeFilter === 'popular') params.push('sort=popular')
        if (this.activeFilter === 'nearby') params.push('nearby=true')

        if (params.length > 0) {
          url += '?' + params.join('&')
        }

        const response = await fetch(url)
        const data = await response.json()

        if (data.success) {
          this.concerts = data.concerts
          this.featuredConcerts = data.concerts.slice(0, 3)
        }
      } catch (error) {
        console.error('Error loading concerts:', error)
        this.concerts = this.getMockConcerts()
        this.featuredConcerts = this.concerts.slice(0, 3)
      } finally {
        this.loading = false
      }
    },

    getMockConcerts() {
      return [
        {
          id: 1,
          artist_name: 'Miyagi & Andy Panda',
          venue: 'VTB Арена',
          city: 'Москва',
          country: 'Россия',
          date: '2024-12-15T20:00:00',
          ticket_url: 'https://example.com/tickets',
          image_url:
            'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&h=400&fit=crop',
          description: 'Легендарный дуэт представляет новый альбом в рамках мирового турне',
          price_range: 'от 2000 ₽',
        },
        {
          id: 2,
          artist_name: 'Morgenshtern',
          venue: 'Сибур Арена',
          city: 'Санкт-Петербург',
          country: 'Россия',
          date: '2024-12-20T19:30:00',
          ticket_url: 'https://example.com/tickets',
          image_url:
            'https://images.unsplash.com/photo-1501281667305-0d4ebd5b1e35?w=800&h=400&fit=crop',
          description: 'Сольный концерт самого эпатажного рэпера страны',
          price_range: 'от 3000 ₽',
        },
        {
          id: 3,
          artist_name: 'The Weeknd',
          venue: 'Лужники',
          city: 'Москва',
          country: 'Россия',
          date: '2024-12-25T21:00:00',
          ticket_url: 'https://example.com/tickets',
          image_url:
            'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800&h=400&fit=crop',
          description: 'Мировое турне After Hours til Dawn',
          price_range: 'от 5000 ₽',
        },
      ]
    },

    searchConcerts() {
      clearTimeout(this.searchTimer)
      this.searchTimer = setTimeout(() => {
        this.loadConcerts()
      }, 300)
    },

    applyFilter(filterId) {
      this.activeFilter = filterId
      this.loadConcerts()
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      const day = date.getDate()
      const month = date.toLocaleString('ru-RU', { month: 'short' })
      return { day, month }
    },

    formatDateShort(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
      })
    },

    showConcertDetails(concert) {
      this.selectedConcert = concert
    },

    buyTickets(concert) {
      if (concert.ticket_url) {
        window.open(concert.ticket_url, '_blank')
      } else {
        alert('Ссылка на билеты скоро будет доступна')
      }
    },

    saveConcert(concert) {
      const saved = JSON.parse(localStorage.getItem('saved_concerts') || '[]')
      if (!saved.find((c) => c.id === concert.id)) {
        saved.push(concert)
        localStorage.setItem('saved_concerts', JSON.stringify(saved))
        alert('Концерт сохранен!')
      } else {
        alert('Концерт уже сохранен')
      }
    },

    shareConcert(concert) {
      const text = `Смотри концерт ${concert.artist_name} в ${concert.city}! 🎤`
      if (navigator.share) {
        navigator.share({
          title: concert.artist_name,
          text: text,
          url: window.location.href,
        })
      } else {
        navigator.clipboard.writeText(text)
        alert('Информация о концерте скопирована!')
      }
    },

    selectCity(cityName) {
      this.selectedCity = cityName
      this.loadConcerts()
    },

    generateCalendar() {
      const year = this.currentDate.getFullYear()
      const month = this.currentDate.getMonth()

      const firstDay = new Date(year, month, 1)
      const lastDay = new Date(year, month + 1, 0)

      const firstDayIndex = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1

      const lastDayIndex = lastDay.getDay() === 0 ? 6 : lastDay.getDay() - 1

      const prevMonthLastDay = new Date(year, month, 0).getDate()
      const prevMonthDays = []
      for (let i = firstDayIndex; i > 0; i--) {
        prevMonthDays.push({
          day: prevMonthLastDay - i + 1,
          date: new Date(year, month - 1, prevMonthLastDay - i + 1).toISOString(),
          isCurrentMonth: false,
          isToday: false,
          hasEvents: Math.random() > 0.7,
        })
      }

      const currentMonthDays = []
      const today = new Date()
      for (let i = 1; i <= lastDay.getDate(); i++) {
        const date = new Date(year, month, i)
        currentMonthDays.push({
          day: i,
          date: date.toISOString(),
          isCurrentMonth: true,
          isToday: date.toDateString() === today.toDateString(),
          hasEvents: Math.random() > 0.8,
        })
      }

      const nextMonthDays = []
      const daysNeeded = 42 - (prevMonthDays.length + currentMonthDays.length)
      for (let i = 1; i <= daysNeeded; i++) {
        nextMonthDays.push({
          day: i,
          date: new Date(year, month + 1, i).toISOString(),
          isCurrentMonth: false,
          isToday: false,
          hasEvents: Math.random() > 0.7,
        })
      }

      this.calendarDays = [...prevMonthDays, ...currentMonthDays, ...nextMonthDays]
    },

    prevMonth() {
      this.currentDate = new Date(
        this.currentDate.getFullYear(),
        this.currentDate.getMonth() - 1,
        1,
      )
      this.generateCalendar()
    },

    nextMonth() {
      this.currentDate = new Date(
        this.currentDate.getFullYear(),
        this.currentDate.getMonth() + 1,
        1,
      )
      this.generateCalendar()
    },

    showDayEvents(day) {
      if (day.hasEvents) {
        alert(`События на ${day.day} ${this.currentMonth}`)
      }
    },
  },
}
</script>

<style scoped>
.concerts-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.concerts-header {
  text-align: center;
  margin: 2rem 0 3rem;
}

.concerts-header h1 {
  font-size: 3rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.concerts-header p {
  color: #b0b0b0;
  font-size: 1.2rem;
}

.concerts-controls {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.search-filter {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-box {
  position: relative;
}

.search-box input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
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

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.5rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 20px;
  color: #b0b0b0;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-btn:hover {
  background: rgba(138, 43, 226, 0.1);
  border-color: #8a2be2;
}

.filter-btn.active {
  background: rgba(138, 43, 226, 0.2);
  border-color: #8a2be2;
  color: #8a2be2;
}

.location-selector {
  display: flex;
  gap: 1rem;
}

.location-selector select {
  flex: 1;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  cursor: pointer;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 4rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(138, 43, 226, 0.3);
  border-radius: 50%;
  border-top-color: #8a2be2;
  animation: spin 1s linear infinite;
}

.featured-concerts {
  margin-bottom: 3rem;
}

.featured-concerts h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.featured-slider {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.featured-card {
  background-size: cover;
  background-position: center;
  border-radius: 15px;
  padding: 2rem;
  min-height: 300px;
  display: flex;
  align-items: flex-end;
  position: relative;
  cursor: pointer;
  transition: transform 0.3s;
}

.featured-card:hover {
  transform: translateY(-5px);
}

.featured-content {
  position: relative;
  z-index: 2;
  width: 100%;
}

.concert-date {
  position: absolute;
  top: -4rem;
  left: 0;
  background: #8a2be2;
  color: white;
  padding: 1rem;
  border-radius: 10px;
  text-align: center;
  min-width: 60px;
}

.date-day {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
}

.date-month {
  font-size: 0.9rem;
  opacity: 0.9;
}

.featured-card h3 {
  font-size: 1.8rem;
  color: white;
  margin-bottom: 0.5rem;
}

.concert-venue {
  color: white;
  font-weight: 500;
  margin-bottom: 0.3rem;
}

.concert-location {
  color: #b0b0b0;
  margin-bottom: 1rem;
}

.concert-price {
  color: #ffa502;
  font-weight: bold;
  margin-bottom: 1rem;
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

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  color: white;
  font-size: 1.8rem;
}

.view-toggle {
  display: flex;
  gap: 0.5rem;
}

.view-toggle button {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 5px;
  color: #b0b0b0;
  cursor: pointer;
}

.view-toggle button.active {
  background: rgba(138, 43, 226, 0.2);
  border-color: #8a2be2;
  color: #8a2be2;
}

.concerts-container {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.concerts-container.grid {
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.concerts-container.list {
  grid-template-columns: 1fr;
}

.concert-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.concert-card:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.08);
}

.concert-image {
  height: 200px;
  position: relative;
  overflow: hidden;
}

.concert-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.concert-card:hover .concert-image img {
  transform: scale(1.05);
}

.concert-date-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #8a2be2;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.9rem;
}

.concert-info {
  padding: 1.5rem;
}

.concert-info h3 {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
}

.concert-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  color: #888;
  font-size: 0.9rem;
}

.concert-description {
  color: #b0b0b0;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.concert-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border: 1px solid #444;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.empty-state p {
  color: #b0b0b0;
}

.calendar-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 3rem;
}

.calendar-section h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.calendar {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1.5rem;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.calendar-header button {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-header button:hover {
  background: rgba(138, 43, 226, 0.1);
  border-color: #8a2be2;
}

.calendar-header h3 {
  color: white;
  font-size: 1.2rem;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
}

.calendar-day-header {
  text-align: center;
  color: #888;
  font-weight: 500;
  padding: 0.5rem;
  font-size: 0.9rem;
}

.calendar-day {
  aspect-ratio: 1;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.calendar-day:hover {
  background: rgba(255, 255, 255, 0.08);
}

.calendar-day.today {
  background: rgba(138, 43, 226, 0.2);
  border: 1px solid #8a2be2;
}

.calendar-day.has-events {
  border: 1px solid rgba(138, 43, 226, 0.5);
}

.calendar-day.other-month {
  opacity: 0.3;
}

.day-number {
  color: white;
  font-weight: 500;
}

.events-indicator {
  position: absolute;
  bottom: 5px;
}

.event-dot {
  display: block;
  width: 6px;
  height: 6px;
  background: #8a2be2;
  border-radius: 50%;
}

.cities-section {
  margin-bottom: 3rem;
}

.cities-section h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.cities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.city-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.city-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
}

.city-image {
  height: 150px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.city-info {
  padding: 1.5rem;
}

.city-info h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.city-count {
  color: #8a2be2;
  font-weight: 500;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .concerts-header h1 {
    font-size: 2rem;
  }

  .location-selector {
    flex-direction: column;
  }

  .featured-slider {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .calendar-grid {
    gap: 0.3rem;
  }

  .calendar-day {
    font-size: 0.8rem;
  }
}
</style>
