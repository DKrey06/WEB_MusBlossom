<template>
  <div class="post-card" :class="{ featured: post.isFeatured }">
    <div class="post-header">
      <div class="author-avatar-placeholder" :style="getAvatarStyle(post.author)">
        {{ getAuthorInitial(post.author) }}
      </div>

      <div class="post-meta">
        <div class="author-info">
          <span class="author-name">{{ getAuthorDisplayName(post.author) }}</span>
          <span class="author-badge" v-if="isAuthorVerified(post.author)">✓</span>
        </div>
        <span class="post-time">{{ formatTime(post.created_at) }}</span>
      </div>
      <button class="more-btn" @click="toggleOptions">⋮</button>
    </div>

    <div class="post-content">
      <h3 class="post-title">{{ post.title || 'Без названия' }}</h3>
      <p class="post-text">{{ post.content || '' }}</p>

      <div v-if="hasTrack" class="track-preview">
        <div class="track-info">
          <div class="album-art-placeholder">🎵</div>
          <div class="track-details">
            <strong>{{ getTrackName(post) }}</strong>
            <span>{{ getTrackArtist(post) }}</span>
          </div>
        </div>
        <button class="play-btn" @click="playTrack(post)">▶️</button>
      </div>

      <div class="post-tags">
        <span class="post-type">{{ getPostType(post) }}</span>
        <span class="tag" v-for="tag in getPostTags(post)" :key="tag"> #{{ tag }} </span>
      </div>

      <div v-if="getPostMedia(post)" class="post-media">
        <img :src="getPostMedia(post)" alt="Media" @click="showMedia" />
      </div>
    </div>

    <div class="post-actions">
      <button class="action-btn like-btn" @click="toggleLike" :class="{ liked: getIsLiked(post) }">
        ❤️ {{ getLikesCount(post) }}
      </button>
      <button class="action-btn comment-btn" @click="toggleComments">
        💬 {{ getCommentsCount(post) }}
      </button>
      <button class="action-btn share-btn" @click="sharePost">↪️ Поделиться</button>
      <button class="action-btn save-btn" @click="toggleSave" :class="{ saved: getIsSaved(post) }">
        {{ getIsSaved(post) ? '★' : '☆' }}
      </button>
    </div>

    <div v-if="showComments" class="comments-section">
      <div class="comments-list">
        <div v-for="comment in getPostComments(post)" :key="comment.id" class="comment">
          <div class="comment-avatar-placeholder" :style="getAvatarStyle(comment.author)">
            {{ getAuthorInitial(comment.author) }}
          </div>
          <div class="comment-content">
            <div class="comment-header">
              <span class="comment-author">{{ getAuthorDisplayName(comment.author) }}</span>
              <span class="comment-time">{{ getCommentTime(comment) }}</span>
            </div>
            <p class="comment-text">{{ comment.text || comment.content || '' }}</p>
          </div>
        </div>
      </div>
      <div class="add-comment">
        <input
          type="text"
          v-model="newComment"
          placeholder="Напишите комментарий..."
          @keyup.enter="addComment"
        />
        <button @click="addComment">Отправить</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PostCard',
  props: {
    post: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },
  data() {
    return {
      showComments: false,
      newComment: '',
    }
  },
  computed: {
    hasTrack() {
      const post = this.post || {}
      return post.track_name || post.track?.name || post.artist_name || post.track?.artist
    },
  },
  methods: {
    getAuthorDisplayName(author) {
      if (!author) return 'Аноним'

      return author.name || author.username || author.author_name || 'Аноним'
    },

    getAuthorInitial(author) {
      const name = this.getAuthorDisplayName(author)
      return name.charAt(0).toUpperCase()
    },

    isAuthorVerified(author) {
      if (!author) return false
      return author.isVerified || author.is_verified || false
    },

    getAvatarStyle(author) {
      const name = this.getAuthorDisplayName(author)
      const colors = [
        'linear-gradient(135deg, #8a2be2, #4b0082)', // Фиолетовый
        'linear-gradient(135deg, #1e90ff, #00bfff)', // Синий
        'linear-gradient(135deg, #ff4757, #ff3838)', // Красный
        'linear-gradient(135deg, #2ed573, #1dd1a1)', // Зеленый
        'linear-gradient(135deg, #ffa502, #ff9f1a)', // Оранжевый
        'linear-gradient(135deg, #7158e2, #574b90)', // Темно-фиолетовый
      ]

      // Простой хэш для выбора цвета
      let hash = 0
      for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash)
      }
      const colorIndex = Math.abs(hash) % colors.length

      return {
        background: colors[colorIndex],
      }
    },

    getTrackName(post) {
      return post.track?.name || post.track_name || 'Неизвестный трек'
    },

    getTrackArtist(post) {
      return post.track?.artist || post.artist_name || 'Неизвестный исполнитель'
    },

    getPostType(post) {
      const typeMap = {
        thought: 'Мысли',
        review: 'Рецензия',
        news: 'Новости',
        quote: 'Цитата',
        photo: 'Фото',
      }
      const type = post.type || post.post_type || 'thought'
      return typeMap[type] || type
    },

    getPostTags(post) {
      return post.tags || []
    },

    getPostMedia(post) {
      return post.media || post.media_url || null
    },

    getLikesCount(post) {
      return post.likes_count || post.likesCount || 0
    },

    getCommentsCount(post) {
      return post.comments_count || post.commentsCount || 0
    },

    getIsLiked(post) {
      return post.is_liked || post.isLiked || false
    },

    getIsSaved(post) {
      return post.is_saved || post.isSaved || false
    },

    getIsFeatured(post) {
      return post.is_featured || post.isFeatured || false
    },

    getPostComments(post) {
      return post.comments || []
    },

    formatTime(timestamp) {
      if (!timestamp) return 'недавно'

      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date

      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)

      if (minutes < 1) return 'только что'
      if (minutes < 60) return `${minutes} мин назад`
      if (hours < 24) return `${hours} ч назад`
      if (days < 7) return `${days} д назад`

      return date.toLocaleDateString('ru-RU')
    },

    getCommentTime(comment) {
      return comment.time || this.formatTime(comment.created_at) || 'недавно'
    },

    toggleLike() {
      this.$emit('like', this.post.id)
    },

    toggleComments() {
      this.showComments = !this.showComments
      if (!this.showComments) {
        this.$emit('comment', this.post.id)
      }
    },

    sharePost() {
      if (navigator.share) {
        navigator.share({
          title: this.post.title,
          text: this.post.content,
          url: window.location.href,
        })
      } else {
        navigator.clipboard.writeText(window.location.href)
        alert('Ссылка скопирована в буфер обмена!')
      }
    },

    toggleSave() {
      this.$emit('save', this.post.id)
    },

    playTrack(post) {
      const trackData = {
        name: this.getTrackName(post),
        artist: this.getTrackArtist(post),
        album_art: post.track?.album_art || post.album_art_url,
      }
      this.$emit('play', trackData)
    },

    showMedia() {
      const mediaUrl = this.getPostMedia(this.post)
      if (mediaUrl) {
        this.$emit('show-media', mediaUrl)
      }
    },

    addComment() {
      if (this.newComment.trim()) {
        this.$emit('comment', {
          postId: this.post.id,
          content: this.newComment,
        })
        this.newComment = ''
      }
    },

    toggleOptions() {
      this.$emit('options', this.post.id)
    },
  },
}
</script>

<style scoped>
.post-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.3s;
}

.post-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.post-card.featured {
  border: 2px solid #8a2be2;
  background: rgba(138, 43, 226, 0.05);
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.author-avatar-placeholder {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 1rem;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.post-meta {
  flex: 1;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.author-name {
  font-weight: 600;
  color: white;
}

.author-badge {
  color: #1e90ff;
  font-size: 0.8rem;
}

.post-time {
  color: #888;
  font-size: 0.9rem;
}

.more-btn {
  background: transparent;
  border: none;
  color: #888;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 5px;
}

.more-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.post-content {
  margin-bottom: 1.5rem;
}

.post-title {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.post-text {
  color: #b0b0b0;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.track-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1rem;
  margin: 1rem 0;
}

.track-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.album-art-placeholder {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  background: rgba(138, 43, 226, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.track-details {
  display: flex;
  flex-direction: column;
}

.track-details strong {
  color: white;
}

.track-details span {
  color: #888;
  font-size: 0.9rem;
}

.play-btn {
  background: rgba(138, 43, 226, 0.2);
  border: 1px solid #8a2be2;
  color: #8a2be2;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.play-btn:hover {
  background: rgba(138, 43, 226, 0.3);
  transform: scale(1.1);
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0;
}

.post-type {
  background: rgba(255, 71, 87, 0.2);
  color: #ff4757;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
}

.tag {
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
}

.post-media img {
  width: 100%;
  max-height: 400px;
  border-radius: 10px;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.3s;
  margin-top: 1rem;
}

.post-media img:hover {
  transform: scale(1.02);
}

.post-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.action-btn {
  flex: 1;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.95rem;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.like-btn:hover,
.like-btn.liked {
  background: rgba(255, 71, 87, 0.1);
  border-color: #ff4757;
  color: #ff4757;
}

.comment-btn:hover {
  background: rgba(30, 144, 255, 0.1);
  border-color: #1e90ff;
  color: #1e90ff;
}

.share-btn:hover {
  background: rgba(46, 213, 115, 0.1);
  border-color: #2ed573;
  color: #2ed573;
}

.save-btn:hover,
.save-btn.saved {
  background: rgba(255, 165, 2, 0.1);
  border-color: #ffa502;
  color: #ffa502;
}

.comments-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.comments-list {
  margin-bottom: 1rem;
}

.comment {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 0.8rem;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
}

.comment-avatar-placeholder {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.3rem;
}

.comment-author {
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
}

.comment-time {
  color: #888;
  font-size: 0.8rem;
}

.comment-text {
  color: #b0b0b0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.add-comment {
  display: flex;
  gap: 0.5rem;
}

.add-comment input {
  flex: 1;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: white;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.add-comment input:focus {
  outline: none;
  border-color: #8a2be2;
  background: rgba(255, 255, 255, 0.1);
}

.add-comment button {
  padding: 0.8rem 1.5rem;
  background: #8a2be2;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: opacity 0.3s;
  font-weight: 500;
}

.add-comment button:hover {
  opacity: 0.9;
}
</style>
