<template>
  <aside class="sidebar">
    <!-- 顶部 Logo -->
    <div class="sidebar-header">
      <div class="logo">
        <svg class="logo-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
        </svg>
        <div class="logo-info">
          <span class="logo-text">荷塘AI生成器</span>
          <span class="logo-version">{{ version }}</span>
        </div>
      </div>
    </div>

    <!-- 导航项 -->
    <nav class="sidebar-nav">
      <button
        class="nav-item"
        :class="{ active: activeView === 'image' }"
        @click="$emit('navigate', 'image')"
      >
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
          <circle cx="8.5" cy="8.5" r="1.5" />
          <polyline points="21 15 16 10 5 21" />
        </svg>
        <span>图片生成</span>
      </button>

      <button
        class="nav-item"
        :class="{ active: activeView === 'video' }"
        @click="$emit('navigate', 'video')"
      >
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18" />
          <line x1="7" y1="2" x2="7" y2="22" />
          <line x1="17" y1="2" x2="17" y2="22" />
          <line x1="2" y1="12" x2="22" y2="12" />
          <line x1="2" y1="7" x2="7" y2="7" />
          <line x1="2" y1="17" x2="7" y2="17" />
          <line x1="17" y1="7" x2="22" y2="7" />
          <line x1="17" y1="17" x2="22" y2="17" />
        </svg>
        <span>视频生成</span>
      </button>
    </nav>

    <!-- 底部设置 -->
    <div class="sidebar-footer">
      <button
        class="nav-item"
        :class="{ active: activeView === 'settings' }"
        @click="$emit('navigate', 'settings')"
      >
        <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="3" />
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
        </svg>
        <span>设置</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineProps({
  activeView: {
    type: String,
    required: true,
  },
})

defineEmits(['navigate'])

const version = ref('')

onMounted(async () => {
  try {
    version.value = await window.pywebview.api.get_version()
  } catch (e) {
    version.value = ''
  }
})
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  height: 100vh;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 20px 16px 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  color: var(--accent);
  flex-shrink: 0;
}

.logo-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.logo-text {
  font-size: var(--font-size-base);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.3px;
  line-height: 1.2;
}

.logo-version {
  font-size: 10px;
  color: var(--text-tertiary);
  font-weight: 500;
}

.sidebar-nav {
  flex: 1;
  padding: 0 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sidebar-footer {
  padding: 8px;
  border-top: 1px solid var(--border);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px 12px;
  border: none;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-normal);
  text-align: left;
}

.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--accent-subtle);
  color: var(--accent);
}

.nav-item.active .nav-icon {
  color: var(--accent);
}

.nav-icon {
  flex-shrink: 0;
}
</style>
