<template>
  <div class="feedback-view">
    <div class="feedback-header">
      <h1>Обратная связь</h1>
      <p>Мы ценим ваше мнение. Пожалуйста, заполните форму ниже</p>
    </div>

    <div class="feedback-container">
      <div class="feedback-form">
        <form @submit.prevent="submitFeedback">
          <div class="form-group">
            <label for="name">Имя *</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              placeholder="Ваше имя"
              required
              :disabled="form.submitting"
            />
          </div>

          <div class="form-group">
            <label for="email">Email *</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="your@email.com"
              required
              :disabled="form.submitting"
            />
          </div>

          <div class="form-group">
            <label>Тип обращения *</label>
            <div class="type-options">
              <label class="type-option">
                <input
                  type="radio"
                  v-model="form.type"
                  value="suggestion"
                  :disabled="form.submitting"
                />
                <span>Предложение</span>
              </label>
              <label class="type-option">
                <input type="radio" v-model="form.type" value="bug" :disabled="form.submitting" />
                <span>Ошибка</span>
              </label>
              <label class="type-option">
                <input
                  type="radio"
                  v-model="form.type"
                  value="question"
                  :disabled="form.submitting"
                />
                <span>Вопрос</span>
              </label>
              <label class="type-option">
                <input type="radio" v-model="form.type" value="other" :disabled="form.submitting" />
                <span>Другое</span>
              </label>
            </div>
          </div>

          <div class="form-group">
            <label for="subject">Тема *</label>
            <input
              id="subject"
              v-model="form.subject"
              type="text"
              placeholder="Краткое описание"
              required
              :disabled="form.submitting"
            />
          </div>

          <div class="form-group">
            <label for="message">Сообщение *</label>
            <textarea
              id="message"
              v-model="form.message"
              placeholder="Подробно опишите ваше обращение..."
              rows="6"
              required
              :disabled="form.submitting"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="attachment-label">
              <input
                type="file"
                ref="fileInput"
                @change="handleFileUpload"
                :disabled="form.submitting"
                style="display: none"
              />
              <span class="attachment-btn">Прикрепить файл</span>
              <span v-if="form.attachment" class="attachment-name">
                {{ form.attachment.name }}
              </span>
            </label>
            <small>Максимальный размер файла: 5MB</small>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="form.submitting || !formValid">
              <span v-if="form.submitting" class="loading">Отправка...</span>
              <span v-else>Отправить</span>
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              @click="resetForm"
              :disabled="form.submitting"
            >
              Очистить
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'FeedbackView',
  data() {
    return {
      form: {
        name: '',
        email: '',
        type: 'suggestion',
        subject: '',
        message: '',
        attachment: null,
        submitting: false,
      },
      successMessage: '',
      errorMessage: '',
    }
  },
  computed: {
    formValid() {
      return (
        this.form.name.trim() &&
        this.form.email.trim() &&
        this.form.subject.trim() &&
        this.form.message.trim() &&
        this.validateEmail(this.form.email)
      )
    },
  },
  methods: {
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return re.test(email)
    },
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          this.errorMessage = 'Файл слишком большой. Максимальный размер: 5MB'
          this.$refs.fileInput.value = ''
          return
        }
        this.form.attachment = file
      }
    },
    async submitFeedback() {
      if (!this.formValid) {
        this.errorMessage = 'Заполните все обязательные поля правильно'
        return
      }

      this.form.submitting = true
      this.successMessage = ''
      this.errorMessage = ''

      const formData = new FormData()
      formData.append('name', this.form.name)
      formData.append('email', this.form.email)
      formData.append('type', this.form.type)
      formData.append('subject', this.form.subject)
      formData.append('message', this.form.message)
      if (this.form.attachment) {
        formData.append('attachment', this.form.attachment)
      }

      try {
        const response = await fetch('/api/feedback', {
          method: 'POST',
          body: formData,
        })

        const data = await response.json()

        if (data.success) {
          this.successMessage = 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.'
          this.resetForm()
        } else {
          this.errorMessage = data.error || 'Произошла ошибка при отправке'
        }
      } catch (error) {
        console.error('Feedback submission error:', error)
        this.errorMessage = 'Ошибка соединения. Пожалуйста, попробуйте позже.'
      } finally {
        this.form.submitting = false
      }
    },
    resetForm() {
      this.form.name = ''
      this.form.email = ''
      this.form.type = 'suggestion'
      this.form.subject = ''
      this.form.message = ''
      this.form.attachment = null
      this.form.submitting = false
      this.errorMessage = ''
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
    },
  },
}
</script>

<style scoped>
.feedback-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.feedback-header {
  text-align: center;
  margin-bottom: 2rem;
}

.feedback-header h1 {
  font-size: 2.5rem;
  color: white;
  margin-bottom: 0.5rem;
}

.feedback-header p {
  color: #b0b0b0;
  font-size: 1.1rem;
}

.feedback-form {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  color: white;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-family: inherit;
  font-size: 1rem;
}

.form-group input:disabled,
.form-group textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.type-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.type-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  cursor: pointer;
}

.type-option:hover {
  background: rgba(255, 255, 255, 0.08);
}

.type-option input {
  width: auto;
  margin: 0;
}

.type-option span {
  color: #b0b0b0;
}

.type-option input:checked + span {
  color: white;
  font-weight: 500;
}

textarea {
  resize: vertical;
}

.attachment-label {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
}

.attachment-btn {
  padding: 0.5rem 1rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 10px;
  font-weight: 500;
}

.attachment-name {
  color: #b0b0b0;
  font-size: 0.9rem;
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.form-group small {
  display: block;
  color: #888;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.8rem 2rem;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  font-size: 1rem;
  flex: 1;
}

.btn-primary {
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border: 1px solid #444;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.success-message,
.error-message {
  margin-top: 2rem;
  padding: 1rem;
  border-radius: 10px;
  text-align: center;
  font-weight: 500;
}

.success-message {
  background: rgba(46, 213, 115, 0.1);
  color: #2ed573;
  border: 1px solid rgba(46, 213, 115, 0.3);
}

.error-message {
  background: rgba(255, 71, 87, 0.1);
  color: #ff4757;
  border: 1px solid rgba(255, 71, 87, 0.3);
}

@media (max-width: 768px) {
  .feedback-view {
    padding: 1rem;
  }

  .feedback-form {
    padding: 1.5rem;
  }

  .type-options {
    flex-direction: column;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
