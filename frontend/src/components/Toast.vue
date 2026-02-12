<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="toast-item"
          :class="`toast-${toast.type}`"
        >
          <svg v-if="toast.type === 'success'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          <svg v-else-if="toast.type === 'error'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          <span class="toast-msg">{{ toast.message }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useToast } from '../composables/useToast.js'
const { toasts } = useToast()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}

.toast-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 13px;
  font-weight: 500;
  pointer-events: auto;
  backdrop-filter: blur(12px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  min-width: 200px;
  max-width: 360px;
}

.toast-success {
  background: rgba(48, 164, 108, 0.15);
  border: 1px solid rgba(48, 164, 108, 0.3);
  color: #30A46C;
}

.toast-error {
  background: rgba(229, 72, 77, 0.15);
  border: 1px solid rgba(229, 72, 77, 0.3);
  color: #E5484D;
}

.toast-warning {
  background: rgba(245, 166, 35, 0.15);
  border: 1px solid rgba(245, 166, 35, 0.3);
  color: #F5A623;
}

.toast-msg {
  flex: 1;
}

/* 动画 */
.toast-enter-active {
  animation: toastIn 0.25s ease;
}
.toast-leave-active {
  animation: toastOut 0.2s ease forwards;
}

@keyframes toastIn {
  from { opacity: 0; transform: translateX(40px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes toastOut {
  from { opacity: 1; transform: translateX(0); }
  to { opacity: 0; transform: translateX(40px); }
}
</style>
