<template>
  <div class="post-card" :class="{ featured: post.isFeatured }">
    <div class="post-header">
      <img :src="post.author.avatar" class="author-avatar" alt="Avatar" />
      <div class="post-meta">
        <div class="author-info">
          <span class="author-name">{{ post.author.name }}</span>
          <span class="author-badge" v-if="post.author.isVerified">✓</span>
        </div>
        <span class="post-time">{{ formatTime(post.created_at) }}</span>
      </div>
      <button class="more-btn" @click="toggleOptions">⋮</button>
    </div>

    <div class="post-content">
      <h3 class="post-title">{{ post.title }}</h3>
      <p class="post-text">{{ post.content }}</p>

      <div v-if="post.track" class="track-preview">
        <div class="track-info">
          <img :src="post.track.album_art" class="album-art" alt="Album" />
          <div class="track-details">
            <strong>{{ post.track.name }}</strong>
            <span>{{ post.track.artist }}</span>
          </div>
        </div>
        <button class="play-btn" @click="playTrack(post.track)">▶️</button>
      </div>

      <div class="post-tags">
        <span class="post-type">{{ post.type }}</span>
        <span class="tag" v-for="tag in post.tags" :key="tag">#{{ tag }}</span>
      </div>

      <div v-if="post.media" class="post-media">
        <img :src="post.media" alt="Media" @click="showMedia" />
      </div>
    </div>

    <div class="post-actions">
      <button class="action-btn like-btn" @click="toggleLike" :class="{ liked: post.isLiked }">
        ❤️ {{ post.likes_count }}
      </button>
      <button class="action-btn comment-btn" @click="toggleComments">
        💬 {{ post.comments_count }}
      </button>
      <button class="action-btn share-btn" @click="sharePost">↪️ Поделиться</button>
      <button class="action-btn save-btn" @click="toggleSave" :class="{ saved: post.isSaved }">
        {{ post.isSaved ? '★' : '☆' }}
      </button>
    </div>

    <div v-if="showComments" class="comments-section">
      <div class="comments-list">
        <div v-for="comment in post.comments" :key="comment.id" class="comment">
          <img :src="comment.author.avatar" class="comment-avatar" alt="Avatar" />
          <div class="comment-content">
            <div class="comment-header">
              <span class="comment-author">{{ comment.author.name }}</span>
              <span class="comment-time">{{ comment.time }}</span>
            </div>
            <p class="comment-text">{{ comment.text }}</p>
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
    },
  },
  data() {
    return {
      showComments: false,
      newComment: '',
    }
  },
  methods: {
    formatTime(timestamp) {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date

      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)

      if (minutes < 60) return `${minutes} мин назад`
      if (hours < 24) return `${hours} ч назад`
      if (days < 7) return `${days} д назад`

      return date.toLocaleDateString()
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
      this.post.isSaved = !this.post.isSaved
    },

    playTrack(track) {
      console.log('Playing:', track)
    },

    showMedia() {
      console.log('Show media')
    },

    addComment() {
      if (this.newComment.trim()) {
        const comment = {
          id: Date.now(),
          author: {
            name: 'Вы',
            avatar: 'https://i.pravatar.cc/150?img=1',
          },
          time: 'Только что',
          text: this.newComment,
        }

        this.post.comments.push(comment)
        this.post.comments_count++
        this.newComment = ''
      }
    },

    toggleOptions() {
      console.log('Show options')
    },
  },
}
</script>

<style scoped>
.post-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
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

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 1rem;
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

.album-art {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  object-fit: cover;
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
}

.post-media img:hover {
  transform: scale(1.02);
}

.post-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #333;
}

.action-btn {
  flex: 1;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
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
  border-top: 1px solid #333;
}

.comments-list {
  margin-bottom: 1rem;
}

.comment {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.comment-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  object-fit: cover;
}

.comment-content {
  flex: 1;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 0.8rem;
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
}

.add-comment {
  display: flex;
  gap: 0.5rem;
}

.add-comment input {
  flex: 1;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 0.9rem;
}

.add-comment input:focus {
  outline: none;
  border-color: #8a2be2;
}

.add-comment button {
  padding: 0.8rem 1.5rem;
  background: #8a2be2;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.add-comment button:hover {
  opacity: 0.9;
}
</style>
