<template>
  <div class="friends-view">
    <div class="friends-header">
      <h1>Друзья</h1>
      <p>Находи единомышленников и общайтесь о музыке</p>
    </div>

    <div class="friends-container">
      <div class="friends-stats">
        <div class="stats-card">
          <div class="stat">
            <span class="stat-value">{{ stats.friends }}</span>
            <span class="stat-label">Друзей</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ stats.followers }}</span>
            <span class="stat-label">Подписчиков</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ stats.following }}</span>
            <span class="stat-label">Подписок</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ stats.requests }}</span>
            <span class="stat-label">Запросы</span>
          </div>
        </div>
      </div>

      <div class="friends-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
          <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
        </button>
      </div>

      <div class="search-friends">
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск по имени, интересам..."
            @input="searchFriends"
          />
          <span class="search-icon">🔍</span>
        </div>

        <div class="suggestions">
          <h3>💡 Возможные друзья</h3>
          <div class="suggestions-list">
            <div v-for="user in suggestedUsers" :key="user.id" class="suggestion-card">
              <img :src="user.avatar" class="user-avatar" alt="Avatar" />
              <div class="user-info">
                <h4>{{ user.username }}</h4>
                <p class="user-bio">{{ user.bio }}</p>
                <div class="user-genres">
                  <span class="genre-tag" v-for="genre in user.genres" :key="genre">
                    {{ genre }}
                  </span>
                </div>
                <div class="mutual-friends">
                  <span>👥 {{ user.mutual }} общих друзей</span>
                </div>
              </div>
              <div class="friend-actions">
                <button class="btn btn-primary btn-small" @click="addFriend(user.id)">
                  Добавить
                </button>
                <button class="btn btn-secondary btn-small" @click="viewProfile(user)">
                  Профиль
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="friends-content">
        <div v-if="activeTab === 'requests'" class="requests-section">
          <h3>📥 Запросы в друзья</h3>
          <div v-if="friendRequests.length" class="requests-list">
            <div v-for="request in friendRequests" :key="request.id" class="request-card">
              <div class="request-user">
                <img :src="request.user.avatar" class="user-avatar" alt="Avatar" />
                <div class="request-info">
                  <h4>{{ request.user.username }}</h4>
                  <p>{{ request.user.bio }}</p>
                  <span class="request-time">{{ request.time }} назад</span>
                </div>
              </div>
              <div class="request-actions">
                <button class="btn btn-primary btn-small" @click="acceptRequest(request.id)">
                  Принять
                </button>
                <button class="btn btn-secondary btn-small" @click="declineRequest(request.id)">
                  Отклонить
                </button>
              </div>
            </div>
          </div>
          <div v-else class="no-requests">
            <p>Нет новых запросов в друзья</p>
          </div>
        </div>

        <div v-if="activeTab === 'all'" class="all-friends">
          <div class="friends-list">
            <div
              v-for="friend in filteredFriends"
              :key="friend.id"
              class="friend-card"
              @click="viewProfile(friend)"
            >
              <div class="friend-header">
                <img :src="friend.avatar" class="friend-avatar" alt="Avatar" />
                <div class="friend-status" :class="{ online: friend.isOnline }"></div>
                <div class="friend-info">
                  <h4>{{ friend.username }}</h4>
                  <p v-if="friend.isOnline" class="online-status">В сети</p>
                  <p v-else class="last-seen">Был(а) {{ friend.lastSeen }}</p>
                </div>
              </div>
              <div class="friend-genres">
                <span class="genre-tag" v-for="genre in friend.genres" :key="genre">
                  {{ genre }}
                </span>
              </div>
              <div class="friend-actions">
                <button class="btn btn-small" @click.stop="sendMessage(friend)">
                  💬 Сообщение
                </button>
                <button class="btn btn-small btn-secondary" @click.stop="removeFriend(friend.id)">
                  Удалить
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'followers'" class="followers-section">
          <div class="followers-list">
            <div v-for="follower in followers" :key="follower.id" class="follower-card">
              <div class="follower-user">
                <img :src="follower.avatar" class="user-avatar" alt="Avatar" />
                <div class="follower-info">
                  <h4>{{ follower.username }}</h4>
                  <p>{{ follower.bio }}</p>
                  <span class="followers-count">👥 {{ follower.followers }} подписчиков</span>
                </div>
              </div>
              <div class="follower-actions">
                <button
                  v-if="!follower.isFollowing"
                  class="btn btn-primary btn-small"
                  @click="followUser(follower.id)"
                >
                  Подписаться
                </button>
                <button
                  v-else
                  class="btn btn-secondary btn-small"
                  @click="unfollowUser(follower.id)"
                >
                  Отписаться
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'following'" class="following-section">
          <div class="following-list">
            <div v-for="followingUser in following" :key="followingUser.id" class="following-card">
              <div class="following-user">
                <img :src="followingUser.avatar" class="user-avatar" alt="Avatar" />
                <div class="following-info">
                  <h4>{{ followingUser.username }}</h4>
                  <p>{{ followingUser.bio }}</p>
                  <div class="following-stats">
                    <span>🎵 {{ followingUser.posts }} постов</span>
                    <span>👥 {{ followingUser.followers }} подписчиков</span>
                  </div>
                </div>
              </div>
              <div class="following-actions">
                <button class="btn btn-secondary btn-small" @click="unfollowUser(followingUser.id)">
                  Отписаться
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="music-groups">
        <h3>🎵 Музыкальные группы</h3>
        <p>Присоединяйтесь к группам по интересам</p>
        <div class="groups-grid">
          <div v-for="group in musicGroups" :key="group.id" class="group-card">
            <div class="group-icon">{{ group.icon }}</div>
            <h4>{{ group.name }}</h4>
            <p>{{ group.description }}</p>
            <div class="group-members">👥 {{ group.members }} участников</div>
            <button
              class="btn btn-small"
              :class="{ 'btn-primary': !group.isMember, 'btn-secondary': group.isMember }"
              @click="toggleGroupMembership(group)"
            >
              {{ group.isMember ? 'Вы в группе' : 'Присоединиться' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FriendsView',
  data() {
    return {
      activeTab: 'all',
      searchQuery: '',
      stats: {
        friends: 42,
        followers: 156,
        following: 87,
        requests: 3,
      },
      tabs: [
        { id: 'all', label: 'Все друзья' },
        { id: 'requests', label: 'Запросы', badge: 3 },
        { id: 'followers', label: 'Подписчики' },
        { id: 'following', label: 'Подписки' },
      ],
      suggestedUsers: [],
      friendRequests: [],
      friends: [],
      followers: [],
      following: [],
      musicGroups: [
        {
          id: 1,
          name: 'Рок-энтузиасты',
          icon: '🎸',
          description: 'Обсуждение рок-музыки всех времен',
          members: 1245,
          isMember: true,
        },
        {
          id: 2,
          name: 'Хип-хоп культура',
          icon: '🎤',
          description: 'Новинки и классика хип-хопа',
          members: 892,
          isMember: false,
        },
        {
          id: 3,
          name: 'Джаз-любители',
          icon: '🎷',
          description: 'Классический и современный джаз',
          members: 567,
          isMember: false,
        },
        {
          id: 4,
          name: 'Электронная музыка',
          icon: '🎧',
          description: 'EDM, техно, хаус и не только',
          members: 1234,
          isMember: true,
        },
      ],
    }
  },
  computed: {
    filteredFriends() {
      if (!this.searchQuery) return this.friends
      const query = this.searchQuery.toLowerCase()
      return this.friends.filter(
        (friend) =>
          friend.username.toLowerCase().includes(query) ||
          friend.bio.toLowerCase().includes(query) ||
          friend.genres.some((genre) => genre.toLowerCase().includes(query)),
      )
    },
  },
  async mounted() {
    await this.loadFriendsData()
    this.loadSuggestedUsers()
  },
  methods: {
    async loadFriendsData() {
      try {
        const response = await fetch('/api/friends')
        const data = await response.json()

        if (data.success) {
          this.friends = data.friends
          this.followers = data.followers
          this.following = data.following
          this.stats = data.stats
        } else {
          this.loadMockData()
        }
      } catch (error) {
        console.error('Error loading friends:', error)
        this.loadMockData()
      }
    },

    loadMockData() {
      this.friends = [
        {
          id: 1,
          username: 'Алексей Рокер',
          avatar: 'https://i.pravatar.cc/150?img=12',
          bio: 'Люблю рок и метал',
          genres: ['Рок', 'Метал', 'Альтернатива'],
          isOnline: true,
          lastSeen: 'только что',
          posts: 45,
          followers: 234,
        },
        {
          id: 2,
          username: 'Мария Меломана',
          avatar: 'https://i.pravatar.cc/150?img=5',
          bio: 'Слушаю все, что нравится',
          genres: ['Поп', 'Инди', 'Фолк'],
          isOnline: false,
          lastSeen: '2 часа назад',
          posts: 32,
          followers: 189,
        },
        {
          id: 3,
          username: 'DJ Петрович',
          avatar: 'https://i.pravatar.cc/150?img=8',
          bio: 'EDM продюсер и диджей',
          genres: ['Электроника', 'Техно', 'Хаус'],
          isOnline: true,
          lastSeen: 'онлайн',
          posts: 28,
          followers: 156,
        },
      ]

      this.friendRequests = [
        {
          id: 1,
          user: {
            id: 4,
            username: 'Иван Гитарист',
            avatar: 'https://i.pravatar.cc/150?img=3',
            bio: 'Играю на гитаре 10 лет',
          },
          time: '5 минут',
        },
        {
          id: 2,
          user: {
            id: 5,
            username: 'Анна Вокалистка',
            avatar: 'https://i.pravatar.cc/150?img=6',
            bio: 'Пою в местной группе',
          },
          time: '1 час',
        },
      ]

      this.followers = [
        {
          id: 6,
          username: 'Сергей Бас-гитарист',
          avatar: 'https://i.pravatar.cc/150?img=9',
          bio: 'Играю в рок-группе',
          followers: 78,
          isFollowing: true,
        },
        {
          id: 7,
          username: 'Ольга Клавишница',
          avatar: 'https://i.pravatar.cc/150?img=4',
          bio: 'Клавишные и синтезаторы',
          followers: 45,
          isFollowing: false,
        },
      ]

      this.following = [
        {
          id: 8,
          username: 'Музыкальный критик',
          avatar: 'https://i.pravatar.cc/150?img=11',
          bio: 'Пишу рецензии на альбомы',
          posts: 67,
          followers: 890,
        },
        {
          id: 9,
          username: 'Звукорежиссер',
          avatar: 'https://i.pravatar.cc/150?img=7',
          bio: 'Записываю и свожу треки',
          posts: 23,
          followers: 156,
        },
      ]
    },

    loadSuggestedUsers() {
      this.suggestedUsers = [
        {
          id: 10,
          username: 'Джазовый саксофонист',
          avatar: 'https://i.pravatar.cc/150?img=13',
          bio: 'Играю джаз на саксофоне',
          genres: ['Джаз', 'Блюз', 'Соул'],
          mutual: 3,
        },
        {
          id: 11,
          username: 'Хип-хоп продюсер',
          avatar: 'https://i.pravatar.cc/150?img=14',
          bio: 'Делаю биты для рэперов',
          genres: ['Хип-хоп', 'R&B', 'Трэп'],
          mutual: 5,
        },
        {
          id: 12,
          username: 'Классический пианист',
          avatar: 'https://i.pravatar.cc/150?img=15',
          bio: 'Консерватория, 15 лет за роялем',
          genres: ['Классика', 'Барокко', 'Романтизм'],
          mutual: 2,
        },
      ]
    },

    searchFriends() {},

    addFriend(userId) {
      const user = this.suggestedUsers.find((u) => u.id === userId)
      if (user) {
        this.friendRequests.push({
          id: Date.now(),
          user: user,
          time: 'только что',
        })
        this.suggestedUsers = this.suggestedUsers.filter((u) => u.id !== userId)
        this.stats.requests++
        alert(`Запрос в друзья отправлен ${user.username}`)
      }
    },

    acceptRequest(requestId) {
      const request = this.friendRequests.find((r) => r.id === requestId)
      if (request) {
        this.friends.push({
          ...request.user,
          isOnline: Math.random() > 0.5,
          lastSeen: 'недавно',
          genres: ['Разное'],
          posts: 0,
          followers: 0,
        })
        this.friendRequests = this.friendRequests.filter((r) => r.id !== requestId)
        this.stats.friends++
        this.stats.requests--
        alert(`Вы добавили в друзья ${request.user.username}`)
      }
    },

    declineRequest(requestId) {
      const request = this.friendRequests.find((r) => r.id === requestId)
      if (request) {
        this.friendRequests = this.friendRequests.filter((r) => r.id !== requestId)
        this.stats.requests--
        alert(`Запрос от ${request.user.username} отклонен`)
      }
    },

    removeFriend(friendId) {
      if (confirm('Удалить из друзей?')) {
        const friend = this.friends.find((f) => f.id === friendId)
        if (friend) {
          this.friends = this.friends.filter((f) => f.id !== friendId)
          this.stats.friends--
          alert(`${friend.username} удален из друзей`)
        }
      }
    },

    followUser(userId) {
      const user = this.followers.find((f) => f.id === userId)
      if (user) {
        user.isFollowing = true
        this.stats.following++
        alert(`Вы подписались на ${user.username}`)
      }
    },

    unfollowUser(userId) {
      const user =
        this.following.find((f) => f.id === userId) || this.followers.find((f) => f.id === userId)
      if (user) {
        if ('isFollowing' in user) {
          user.isFollowing = false
        }
        this.following = this.following.filter((f) => f.id !== userId)
        this.stats.following--
        alert(`Вы отписались от ${user.username}`)
      }
    },

    viewProfile(user) {
      this.$router.push(`/profile/${user.username}`)
    },

    sendMessage(friend) {
      alert(`Открыть чат с ${friend.username}`)
    },

    toggleGroupMembership(group) {
      group.isMember = !group.isMember
      if (group.isMember) {
        group.members++
        alert(`Вы присоединились к группе "${group.name}"`)
      } else {
        group.members--
        alert(`Вы покинули группу "${group.name}"`)
      }
    },
  },
}
</script>

<style scoped>
.friends-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.friends-header {
  text-align: center;
  margin: 2rem 0 3rem;
}

.friends-header h1 {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.friends-header p {
  color: #b0b0b0;
  font-size: 1.2rem;
}

.friends-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.friends-stats {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
}

.stats-card {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

@media (max-width: 768px) {
  .stats-card {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat {
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  color: #8a2be2;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.friends-tabs {
  display: flex;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 0.5rem;
}

.friends-tabs button {
  flex: 1;
  padding: 1rem;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  font-weight: 500;
  position: relative;
  transition: all 0.3s;
}

.friends-tabs button:hover {
  background: rgba(255, 255, 255, 0.05);
}

.friends-tabs button.active {
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
}

.tab-badge {
  position: absolute;
  top: 5px;
  right: 10px;
  background: #ff4757;
  color: white;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
}

.search-friends {
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

.suggestions h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.suggestion-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.user-info h4 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.user-bio {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.user-genres {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.5rem;
}

.genre-tag {
  padding: 0.2rem 0.6rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 15px;
  font-size: 0.8rem;
}

.mutual-friends {
  color: #888;
  font-size: 0.9rem;
}

.friend-actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
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

.friends-content {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
}

.friends-content h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}

.requests-section,
.all-friends,
.followers-section,
.following-section {
  margin-bottom: 2rem;
}

.requests-list,
.followers-list,
.following-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.request-card,
.follower-card,
.following-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.request-user,
.follower-user,
.following-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.request-info h4,
.follower-info h4,
.following-info h4 {
  color: white;
  margin-bottom: 0.3rem;
  font-size: 1.1rem;
}

.request-info p,
.follower-info p,
.following-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.request-time {
  color: #888;
  font-size: 0.8rem;
}

.followers-count,
.following-stats {
  color: #888;
  font-size: 0.9rem;
}

.following-stats {
  display: flex;
  gap: 1rem;
}

.request-actions,
.follower-actions,
.following-actions {
  display: flex;
  gap: 0.5rem;
}

.no-requests {
  text-align: center;
  padding: 2rem;
  color: #888;
}

.friends-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.friend-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
}

.friend-card:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-3px);
}

.friend-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  position: relative;
}

.friend-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.friend-status {
  position: absolute;
  bottom: 5px;
  left: 45px;
  width: 12px;
  height: 12px;
  background: #888;
  border-radius: 50%;
  border: 2px solid #1a1a2e;
}

.friend-status.online {
  background: #2ed573;
}

.friend-info h4 {
  color: white;
  margin-bottom: 0.2rem;
  font-size: 1.1rem;
}

.online-status {
  color: #2ed573;
  font-size: 0.9rem;
}

.last-seen {
  color: #888;
  font-size: 0.9rem;
}

.friend-genres {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.friend-actions {
  display: flex;
  gap: 0.5rem;
}

.music-groups {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
}

.music-groups h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.3rem;
}

.music-groups p {
  color: #b0b0b0;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.group-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
}

.group-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.group-card h4 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.group-card p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.group-members {
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .friends-list,
  .groups-grid {
    grid-template-columns: 1fr;
  }

  .request-card,
  .follower-card,
  .following-card {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .request-actions,
  .follower-actions,
  .following-actions {
    justify-content: center;
  }
}
</style>
