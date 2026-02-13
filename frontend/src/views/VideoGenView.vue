<template>
  <div
    class="video-gen"
    @dragenter.prevent="onDragEnter"
    @dragover.prevent="onDragOver"
    @dragleave.prevent="onDragLeave"
    @drop.prevent="onDrop"
  >
    <!-- 拖拽遮罩 -->
    <div v-if="isDragging" class="drag-overlay">
      <div class="drag-hint">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" />
        </svg>
        <span>拖放图片以创建图生视频任务</span>
      </div>
    </div>

    <!-- 顶部标题栏 -->
    <header class="view-header">
      <h1 class="view-title">视频生成</h1>
      <div class="header-actions">
        <button class="btn btn-ghost" @click="showImgDialog = true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
            <circle cx="8.5" cy="8.5" r="1.5" /><polyline points="21 15 16 10 5 21" />
          </svg>
          图生视频
        </button>
        <button class="btn btn-primary" @click="showTextDialog = true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          文生视频
        </button>
      </div>
    </header>

    <!-- 任务列表 -->
    <div class="task-list-area">
      <div class="task-list-header">
        <span class="task-count">{{ tasks.length }} 个任务</span>
        <button v-if="hasDoneTasks" class="btn-text-danger" @click="clearDoneTasks">清除已完成</button>
      </div>

      <div class="task-list" v-if="tasks.length > 0">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="task-card"
          :class="[`status-${task.status}`]"
          @click="toggleExpand(task.id)"
        >
          <div class="task-status-icon">
            <svg v-if="task.status === 'pending'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-pending">
              <circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" />
            </svg>
            <span v-else-if="task.status === 'running'" class="spinner-task"></span>
            <svg v-else-if="task.status === 'done'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="icon-done">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            <svg v-else-if="task.status === 'error'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-error">
              <circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-cancelled">
              <circle cx="12" cy="12" r="10" /><line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
            </svg>
          </div>
          <div class="task-info">
            <div class="task-prompt">{{ task.prompt }}</div>
            <div class="task-meta">
              <span class="task-model">{{ formatModel(task.model) }}</span>
              <span class="task-mode-badge">{{ task.mode === 'img2video' ? '图生视频' : '文生视频' }}</span>
              <span v-if="task.status === 'running' && task.progress.length" class="task-progress-text">
                {{ task.progress[task.progress.length - 1] }}
              </span>
              <span v-else-if="task.status === 'error'" class="task-error-text">{{ task.error }}</span>
              <span v-else-if="task.status === 'done' && task.file_path" class="task-saved-text">已保存</span>
            </div>
          </div>
          <div v-if="task.status === 'done' && task.result_video" class="task-thumb">
            <div class="task-thumb-video">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3" />
              </svg>
            </div>
          </div>
          <div class="task-actions" @click.stop>
            <button v-if="task.status === 'error'" class="action-btn action-retry" title="重试" @click="retryTask(task.id)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 4 23 10 17 10" />
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
              </svg>
            </button>
            <button v-if="task.status === 'pending'" class="action-btn" title="取消" @click="cancelTask(task.id)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
            <button v-if="task.status === 'done'" class="action-btn" title="保存" @click="saveTaskVideo(task.id)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" /><line x1="12" y1="15" x2="12" y2="3" />
              </svg>
            </button>
            <button v-if="task.status !== 'running'" class="action-btn" title="删除" @click="deleteTask(task.id)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.2">
          <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18" />
          <line x1="7" y1="2" x2="7" y2="22" />
          <line x1="17" y1="2" x2="17" y2="22" />
          <line x1="2" y1="12" x2="22" y2="12" />
        </svg>
        <p class="empty-text">点击右上角添加任务，或拖拽图片创建图生视频任务</p>
        <p class="empty-hint">支持文生视频和图生视频，拖拽多张图片可批量创建</p>
      </div>
    </div>

    <!-- 视频预览 -->
    <div v-if="expandedTask && expandedTask.status === 'done'" class="preview-overlay" @click="expandedId = null">
      <div class="preview-container" @click.stop>
        <video :src="expandedTask.result_video" controls autoplay class="preview-video"></video>
        <div class="preview-actions">
          <button class="btn btn-secondary" @click="saveTaskVideo(expandedTask.id)">保存视频</button>
          <button class="btn btn-secondary" @click="expandedId = null">关闭</button>
        </div>
      </div>
    </div>

    <!-- ============ 文生视频 Dialog ============ -->
    <div v-if="showTextDialog" class="dialog-overlay" @click.self="showTextDialog = false">
      <div class="dialog">
        <div class="dialog-header">
          <h2 class="dialog-title">添加文生视频任务</h2>
          <button class="dialog-close" @click="showTextDialog = false">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
        <div class="dialog-body">
          <label class="label">提示词（一行一个）</label>
          <textarea
            v-model="textPrompts"
            class="textarea"
            placeholder="一行一个提示词，每行生成一个视频任务..."
            rows="6"
          ></textarea>
          <label class="label" style="margin-top: 12px;">模型</label>
          <div class="custom-select" @click.stop>
            <button class="custom-select-btn" @click="textModelOpen = !textModelOpen">
              <span>{{ formatModel(textModel) }}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>
            <div v-if="textModelOpen" class="custom-select-dropdown">
              <button
                v-for="m in T2V_MODELS"
                :key="m.value"
                class="select-option"
                :class="{ selected: textModel === m.value }"
                @click="textModel = m.value; textModelOpen = false"
              >{{ m.label }}</button>
            </div>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn btn-secondary" @click="showTextDialog = false">取消</button>
          <button class="btn btn-primary" :disabled="!textPrompts.trim()" @click="submitTextTasks">添加</button>
        </div>
      </div>
    </div>

    <!-- ============ 图生视频 Dialog ============ -->
    <div v-if="showImgDialog" class="dialog-overlay" @click.self="showImgDialog = false">
      <div class="dialog dialog-wide">
        <div class="dialog-header">
          <h2 class="dialog-title">添加图生视频任务</h2>
          <button class="dialog-close" @click="showImgDialog = false">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
        <div class="dialog-body img-dialog-body">
          <!-- 上传按钮 -->
          <div v-if="imgEntries.length === 0" class="img-upload-area" @click="triggerFileInput">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" />
            </svg>
            <span class="upload-text">点击选择图片或拖拽图片到页面</span>
            <input ref="fileInput" type="file" accept="image/*" multiple style="display: none" @change="onFileSelect" />
          </div>

          <!-- 图片条目列表 -->
          <div v-for="(img, idx) in imgEntries" :key="idx" class="img-entry">
            <img :src="img.preview" class="img-entry-thumb" />
            <div class="img-entry-fields">
              <input
                v-model="img.prompt"
                class="input"
                placeholder="描述视频内容..."
              />
              <div class="custom-select custom-select-sm" @click.stop>
                <button class="custom-select-btn" @click="img.modelOpen = !img.modelOpen">
                  <span>{{ formatModel(img.model) }}</span>
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="6 9 12 15 18 9" />
                  </svg>
                </button>
                <div v-if="img.modelOpen" class="custom-select-dropdown">
                  <button
                    v-for="m in I2V_MODELS"
                    :key="m.value"
                    class="select-option"
                    :class="{ selected: img.model === m.value }"
                    @click="img.model = m.value; img.modelOpen = false"
                  >{{ m.label }}</button>
                </div>
              </div>
            </div>
            <button class="action-btn" @click="imgEntries.splice(idx, 1)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <!-- 追加更多图片 -->
          <button v-if="imgEntries.length > 0" class="btn-add-more" @click="triggerFileInput">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            添加更多图片
            <input ref="fileInput" type="file" accept="image/*" multiple style="display: none" @change="onFileSelect" />
          </button>
        </div>
        <div class="dialog-footer">
          <button class="btn btn-secondary" @click="showImgDialog = false">取消</button>
          <button class="btn btn-primary" :disabled="!canSubmitImg" @click="submitImgTasks">添加 {{ imgEntries.length }} 个任务</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useToast } from '../composables/useToast.js'

const toast = useToast()
const tasks = ref([])
const expandedId = ref(null)
const isDragging = ref(false)
let dragCounter = 0

// ========== 文生视频 Dialog ==========
const showTextDialog = ref(false)
const textPrompts = ref('')
const textModel = ref('veo_3_1_t2v_fast_landscape')
const textModelOpen = ref(false)

// ========== 图生视频 Dialog ==========
const showImgDialog = ref(false)
const imgEntries = ref([])
const fileInput = ref(null)

// ========== 模型定义 ==========
const T2V_MODELS = [
  { value: 'veo_3_1_t2v_fast_landscape', label: '横屏' },
  { value: 'veo_3_1_t2v_fast_portrait', label: '竖屏' },
]

const I2V_MODELS = [
  { value: 'veo_3_1_i2v_s_fast_fl', label: '横屏' },
  { value: 'veo_3_1_i2v_s_fast_portrait_fl', label: '竖屏' },
]

const ALL_MODELS = [...T2V_MODELS, ...I2V_MODELS]
const MODEL_LABELS = {}
ALL_MODELS.forEach(m => MODEL_LABELS[m.value] = m.label)

function formatModel(model) { return MODEL_LABELS[model] || model }

const hasDoneTasks = computed(() =>
  tasks.value.some(t => t.status === 'done' || t.status === 'error' || t.status === 'cancelled')
)

const expandedTask = computed(() =>
  expandedId.value ? tasks.value.find(t => t.id === expandedId.value) : null
)

const canSubmitImg = computed(() =>
  imgEntries.value.length > 0 && imgEntries.value.every(e => e.prompt.trim())
)

// ========== 拖拽处理 ==========

function onDragEnter(e) {
  dragCounter++
  if (e.dataTransfer?.types?.includes('Files')) isDragging.value = true
}

function onDragOver() {}

function onDragLeave() {
  dragCounter--
  if (dragCounter <= 0) {
    dragCounter = 0
    isDragging.value = false
  }
}

function onDrop(e) {
  dragCounter = 0
  isDragging.value = false
  const files = Array.from(e.dataTransfer?.files || []).filter(f => f.type.startsWith('image/'))
  if (files.length === 0) return
  processImageFiles(files)
}

function triggerFileInput() {
  // 找到离得最近的 file input
  const inputs = document.querySelectorAll('input[type="file"]')
  if (inputs.length > 0) {
    inputs[inputs.length - 1].click()
  }
}

function onFileSelect(e) {
  const files = Array.from(e.target.files || []).filter(f => f.type.startsWith('image/'))
  if (files.length === 0) return
  processImageFiles(files)
  e.target.value = '' // 重置，允许重复选择
}

function processImageFiles(files) {
  const entries = []
  let loaded = 0
  files.forEach(file => {
    const reader = new FileReader()
    reader.onload = (ev) => {
      entries.push(reactive({
        preview: ev.target.result,
        base64: ev.target.result.split(',')[1],
        prompt: '',
        model: 'veo_3_1_i2v_s_fast_fl',
        modelOpen: false,
      }))
      loaded++
      if (loaded === files.length) {
        imgEntries.value = [...imgEntries.value, ...entries]
        showImgDialog.value = true
      }
    }
    reader.readAsDataURL(file)
  })
}

// ========== 提交任务 ==========

async function submitTextTasks() {
  const lines = textPrompts.value.split('\n').map(l => l.trim()).filter(Boolean)
  if (lines.length === 0) return

  let count = 0
  for (const line of lines) {
    try {
      const task = await window.pywebview.api.add_video_task(line, textModel.value, 'text2video', '', '')
      tasks.value.unshift(task)
      count++
    } catch (e) {
      toast.error(`添加失败: ${line.substring(0, 20)}`)
    }
  }
  toast.success(`已添加 ${count} 个文生视频任务`)
  textPrompts.value = ''
  showTextDialog.value = false
}

async function submitImgTasks() {
  if (!canSubmitImg.value) return
  let count = 0
  for (const entry of imgEntries.value) {
    try {
      const task = await window.pywebview.api.add_video_task(
        entry.prompt, entry.model, 'img2video', entry.base64, ''
      )
      tasks.value.unshift(task)
      count++
    } catch (e) {
      toast.error(`添加失败: ${entry.prompt.substring(0, 20)}`)
    }
  }
  toast.success(`已添加 ${count} 个图生视频任务`)
  imgEntries.value = []
  showImgDialog.value = false
}

// ========== 任务操作 ==========

async function cancelTask(id) {
  try {
    await window.pywebview.api.cancel_video_task(id)
    const task = tasks.value.find(t => t.id === id)
    if (task) task.status = 'cancelled'
  } catch (e) { toast.error('取消失败') }
}

async function retryTask(id) {
  try {
    const updated = await window.pywebview.api.retry_video_task(id)
    if (updated && updated.id) {
      const task = tasks.value.find(t => t.id === id)
      if (task) {
        task.status = 'pending'
        task.progress = []
        task.result_video = ''
        task.error = ''
        task.file_path = ''
      }
      toast.success('任务已重新提交')
    }
  } catch (e) { toast.error('重试失败') }
}

async function deleteTask(id) {
  try {
    await window.pywebview.api.delete_video_task(id)
    tasks.value = tasks.value.filter(t => t.id !== id)
    if (expandedId.value === id) expandedId.value = null
  } catch (e) { toast.error('删除失败') }
}

async function clearDoneTasks() {
  try {
    await window.pywebview.api.clear_done_video_tasks()
    tasks.value = tasks.value.filter(t => t.status !== 'done' && t.status !== 'error' && t.status !== 'cancelled')
    expandedId.value = null
    toast.success('已清除')
  } catch (e) { toast.error('清除失败') }
}

async function saveTaskVideo(id) {
  try {
    const path = await window.pywebview.api.save_task_video(id)
    if (path) toast.success('视频已保存')
  } catch (e) { toast.error('保存失败') }
}

function toggleExpand(id) {
  expandedId.value = expandedId.value === id ? null : id
}

// ========== 任务更新回调 ==========

function onVideoTaskUpdate(data) {
  const idx = tasks.value.findIndex(t => t.id === data.task_id)
  if (idx === -1) return
  const task = tasks.value[idx]
  if (data.type === 'status') task.status = data.status
  else if (data.type === 'progress') { task.status = 'running'; task.progress.push(data.progress_text) }
  else if (data.type === 'done') { task.status = 'done'; task.result_video = data.result_video; task.file_path = data.file_path || '' }
  else if (data.type === 'error') { task.status = 'error'; task.error = data.error }
  else if (data.type === 'cancelled') task.status = 'cancelled'
}

onMounted(async () => {
  window.__onVideoTaskUpdate = onVideoTaskUpdate
  document.addEventListener('click', closeAllDropdowns)
  try {
    const list = await window.pywebview.api.get_all_video_tasks()
    if (list && list.length) tasks.value = list
  } catch (e) { /* ignore */ }
})

onUnmounted(() => {
  delete window.__onVideoTaskUpdate
  document.removeEventListener('click', closeAllDropdowns)
})

function closeAllDropdowns() {
  textModelOpen.value = false
  imgEntries.value.forEach(e => e.modelOpen = false)
}
</script>

<style scoped>
.video-gen {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* 拖拽遮罩 */
.drag-overlay {
  position: absolute;
  inset: 0;
  background: rgba(91, 91, 214, 0.08);
  border: 2px dashed var(--accent);
  border-radius: var(--radius-lg);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drag-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: var(--accent);
  font-size: var(--font-size-base);
  font-weight: 500;
}

/* 顶部 */
.view-header {
  padding: 20px 28px 16px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.view-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.3px;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.btn-ghost {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-normal);
  white-space: nowrap;
}
.btn-ghost:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
  border-color: var(--border-strong);
}

/* 任务列表 */
.task-list-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0 28px;
}

.task-list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 10px;
  flex-shrink: 0;
}

.task-count { font-size: var(--font-size-xs); color: var(--text-tertiary); font-weight: 500; }

.btn-text-danger {
  background: none; border: none; color: var(--text-tertiary);
  font-family: var(--font-family); font-size: var(--font-size-xs);
  cursor: pointer; padding: 2px 6px; border-radius: var(--radius-sm);
  transition: all var(--transition-normal);
}
.btn-text-danger:hover { color: var(--error); background: rgba(229, 72, 77, 0.08); }

.task-list {
  flex: 1; overflow-y: auto;
  display: flex; flex-direction: column; gap: 6px; padding-bottom: 20px;
}

/* 任务卡片 */
.task-card {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 14px; background: var(--bg-secondary);
  border: 1px solid var(--border); border-radius: var(--radius-md);
  cursor: pointer; transition: all var(--transition-normal); min-height: 52px;
}
.task-card:hover { background: var(--bg-tertiary); border-color: var(--border-strong); }
.task-card.status-running { border-color: rgba(91, 91, 214, 0.3); }
.task-card.status-done { border-color: rgba(48, 164, 108, 0.2); }
.task-card.status-error { border-color: rgba(229, 72, 77, 0.2); }

.task-status-icon { flex-shrink: 0; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; }
.icon-pending { color: var(--text-tertiary); }
.icon-done { color: var(--success); }
.icon-error { color: var(--error); }
.icon-cancelled { color: var(--text-tertiary); }

.spinner-task {
  width: 18px; height: 18px;
  border: 2px solid var(--border-strong); border-top-color: var(--accent);
  border-radius: 50%; animation: spin 0.7s linear infinite;
}

.task-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
.task-prompt { font-size: var(--font-size-sm); color: var(--text-primary); font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.task-meta { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.task-model { font-size: var(--font-size-xs); color: var(--text-tertiary); }
.task-mode-badge { font-size: 10px; color: var(--text-tertiary); background: var(--bg-elevated); padding: 1px 6px; border-radius: 8px; }
.task-progress-text { font-size: var(--font-size-xs); color: var(--accent); animation: fadeIn 0.2s ease; }
.task-error-text { font-size: var(--font-size-xs); color: var(--error); }
.task-saved-text { font-size: var(--font-size-xs); color: var(--success); }

.task-thumb { flex-shrink: 0; }
.task-thumb-video {
  width: 40px; height: 40px; border-radius: var(--radius-sm);
  border: 1px solid var(--border); background: var(--bg-tertiary);
  display: flex; align-items: center; justify-content: center;
  color: var(--success);
}

.task-actions { display: flex; gap: 4px; flex-shrink: 0; }
.action-btn {
  width: 28px; height: 28px; border: none; border-radius: var(--radius-sm);
  background: transparent; color: var(--text-tertiary);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all var(--transition-fast);
}
.action-btn:hover { background: var(--bg-hover); color: var(--text-primary); }
.action-retry { color: var(--accent); }
.action-retry:hover { background: rgba(91, 91, 214, 0.1); color: var(--accent-hover); }

/* 空状态 */
.empty-state { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; }
.empty-text { color: var(--text-tertiary); font-size: var(--font-size-sm); }
.empty-hint { color: var(--text-placeholder); font-size: var(--font-size-xs); }

/* 视频预览 */
.preview-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.75); display: flex; align-items: center; justify-content: center; z-index: 100; animation: fadeIn 0.2s ease; }
.preview-container { display: flex; flex-direction: column; align-items: center; gap: 16px; max-width: 90vw; max-height: 90vh; }
.preview-video { max-width: 100%; max-height: calc(90vh - 60px); border-radius: var(--radius-md); background: #000; }
.preview-actions { display: flex; gap: 8px; }

/* ========== Dialog 通用 ========== */
.dialog-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center; z-index: 200;
  animation: fadeIn 0.15s ease;
}

.dialog {
  background: var(--bg-secondary); border: 1px solid var(--border);
  border-radius: var(--radius-lg); width: 480px; max-height: 80vh;
  display: flex; flex-direction: column;
  box-shadow: var(--shadow-lg);
}

.dialog-wide { width: 580px; }

.dialog-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 20px 0;
}

.dialog-title { font-size: var(--font-size-lg); font-weight: 600; color: var(--text-primary); }

.dialog-close {
  width: 28px; height: 28px; border: none; border-radius: var(--radius-sm);
  background: transparent; color: var(--text-tertiary);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all var(--transition-fast);
}
.dialog-close:hover { background: var(--bg-hover); color: var(--text-primary); }

.dialog-body { padding: 16px 20px; overflow-y: auto; flex: 1; }

.dialog-footer {
  padding: 12px 20px 16px; display: flex; justify-content: flex-end; gap: 8px;
  border-top: 1px solid var(--border);
}

/* ========== 图生视频 Dialog ========== */
.img-dialog-body { display: flex; flex-direction: column; gap: 12px; }

.img-upload-area {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 10px; padding: 32px; border: 2px dashed var(--border);
  border-radius: var(--radius-md); cursor: pointer;
  transition: all var(--transition-normal);
}
.img-upload-area:hover { border-color: var(--accent); background: rgba(91, 91, 214, 0.04); }
.upload-text { font-size: var(--font-size-sm); color: var(--text-tertiary); }

.img-entry {
  display: flex; align-items: center; gap: 12px;
  padding: 10px; background: var(--bg-tertiary); border-radius: var(--radius-md);
}

.img-entry-thumb {
  width: 56px; height: 56px; border-radius: var(--radius-sm);
  object-fit: cover; border: 1px solid var(--border); flex-shrink: 0;
}

.img-entry-fields { flex: 1; display: flex; flex-direction: column; gap: 6px; min-width: 0; }
.img-entry-fields .input { font-size: var(--font-size-sm); padding: 6px 10px; }

.btn-add-more {
  display: flex; align-items: center; justify-content: center; gap: 6px;
  padding: 8px; border: 1px dashed var(--border); border-radius: var(--radius-md);
  background: transparent; color: var(--text-tertiary);
  font-family: var(--font-family); font-size: var(--font-size-sm);
  cursor: pointer; transition: all var(--transition-normal);
}
.btn-add-more:hover { border-color: var(--accent); color: var(--accent); }

/* ========== 自定义下拉框 ========== */
.custom-select { position: relative; }
.custom-select-sm { width: 100%; }

.custom-select-btn {
  display: flex; align-items: center; justify-content: space-between;
  width: 100%; padding: 7px 12px;
  background: var(--bg-tertiary); border: 1px solid var(--border);
  border-radius: var(--radius-md); color: var(--text-primary);
  font-family: var(--font-family); font-size: var(--font-size-sm);
  cursor: pointer; transition: border-color var(--transition-normal);
}
.custom-select-btn:hover { border-color: var(--border-strong); }

.custom-select-dropdown {
  position: absolute; top: calc(100% + 4px); left: 0; right: 0;
  background: var(--bg-elevated); border: 1px solid var(--border-strong);
  border-radius: var(--radius-md); padding: 4px;
  z-index: 300; box-shadow: var(--shadow-md);
  max-height: 240px; overflow-y: auto;
  animation: dropdownIn 0.12s ease;
}

.select-option {
  display: block; width: 100%; text-align: left;
  padding: 6px 10px; border: none; border-radius: 6px;
  background: transparent; color: var(--text-secondary);
  font-family: var(--font-family); font-size: var(--font-size-sm);
  cursor: pointer; transition: all var(--transition-fast);
}
.select-option:hover { background: var(--bg-hover); color: var(--text-primary); }
.select-option.selected { background: var(--accent-subtle); color: var(--accent); }

@keyframes dropdownIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
</style>
