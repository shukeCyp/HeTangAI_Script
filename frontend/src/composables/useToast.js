import { reactive } from 'vue'

const toasts = reactive([])
let _id = 0

export function useToast() {
  function show(message, type = 'success', duration = 3000) {
    const id = ++_id
    toasts.push({ id, message, type })
    setTimeout(() => {
      const idx = toasts.findIndex(t => t.id === id)
      if (idx !== -1) toasts.splice(idx, 1)
    }, duration)
  }

  return {
    toasts,
    success: (msg, dur) => show(msg, 'success', dur),
    error: (msg, dur) => show(msg, 'error', dur),
    warning: (msg, dur) => show(msg, 'warning', dur),
  }
}
