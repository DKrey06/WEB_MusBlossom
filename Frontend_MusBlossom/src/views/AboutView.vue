<template>
  <div class="about-view">
    <div class="about-hero">
      <h1>О проекте MusBlossom</h1>
      <p>Музыкальная социальная платформа</p>
    </div>

    <div class="about-content">
      <section class="about-section">
        <h2>Наша платформа</h2>
        <p>
          MusBlossom создан для объединения любителей музыки в одном месте, где можно делиться
          впечатлениями, открывать новые треки, находить друзей по музыкальным вкусам и развиваться
          вместе.
        </p>
      </section>

      <section class="about-section">
        <h2>Разработчик</h2>
        <p>
          Кретов Дмитрий Алексеевич - студент Дальневосточного федерального университета, группа
          Б9124-01.03.02сп
        </p>
        <img src="@/assets/images/Creator_MusBlossom.jpg" alt="Разработчик - Кретов Дмитрий" />
      </section>

      <section class="about-section">
        <h2>Контакты</h2>
        <p>Есть вопросы или предложения? Пишите нам:</p>
        <div class="social-links">
          <a href="https://vk.com/dkrey_06" target="_blank" class="social-link vk">
            <span class="social-icon">VK</span>
            <span>ВКонтакте</span>
          </a>
          <a href="https://t.me/DKrey_06" target="_blank" class="social-link telegram">
            <span class="social-icon">TG</span>
            <span>Telegram</span>
          </a>
          <div class="social-link email">
            <span class="social-icon">@</span>
            <span>mrdmitry2006@mail.ru</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
}
</script>

<style scoped>
.about-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.about-hero {
  text-align: center;
  margin-bottom: 3rem;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.1), rgba(75, 0, 130, 0.1));
  border-radius: 20px;
}

.about-hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.about-hero p {
  color: #b0b0b0;
  font-size: 1.2rem;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.about-section h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.about-section p {
  color: #b0b0b0;
  line-height: 1.6;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.about-section a {
  color: #8a2be2;
  text-decoration: none;
}

.about-section a:hover {
  text-decoration: underline;
}

.social-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}

.social-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 12px;
  text-decoration: none;
  color: white;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.05);
}

.social-link:hover {
  transform: translateX(5px);
  background: rgba(255, 255, 255, 0.1);
}

.social-link.email {
  cursor: default;
  opacity: 0.8;
}

.social-link.email:hover {
  transform: none;
  background: rgba(255, 255, 255, 0.05);
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 0.9rem;
}

.vk .social-icon {
  background: #4c75a3;
  color: white;
}

.telegram .social-icon {
  background: #0088cc;
  color: white;
}

.email .social-icon {
  background: #8a2be2;
  color: white;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 1rem;
}

.feature {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  transition: transform 0.3s;
}

.feature:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature h3 {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
}

.feature p {
  color: #b0b0b0;
  font-size: 1rem;
}
</style>
