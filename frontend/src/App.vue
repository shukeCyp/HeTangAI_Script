<template>
  <div class="app-layout">
    <Sidebar
      :active-view="activeView"
      @navigate="activeView = $event"
    />
    <main class="main-content">
      <ImageGenView v-if="activeView === 'image'" />
      <VideoGenView v-else-if="activeView === 'video'" />
      <SettingsView v-else-if="activeView === 'settings'" />
    </main>
  </div>
  <Toast />
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './components/Sidebar.vue'
import ImageGenView from './views/ImageGenView.vue'
import VideoGenView from './views/VideoGenView.vue'
import SettingsView from './views/SettingsView.vue'
import Toast from './components/Toast.vue'

const activeView = ref('image')
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: var(--bg-primary);
}

.main-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>
