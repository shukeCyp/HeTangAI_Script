<template>
  <div class="settings-view">
    <header class="view-header">
      <h1 class="view-title">设置</h1>
    </header>

    <div class="settings-body">
      <!-- 官网 -->
      <section class="settings-section">
        <h2 class="section-title">官网</h2>
        <div class="setting-item">
          <button class="website-link" @click="openWebsite">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
            <span>打开荷塘AI官网（注册/获取API Key）</span>
          </button>
        </div>
      </section>

      <!-- API 配置 -->
      <section class="settings-section">
        <h2 class="section-title">API 配置</h2>

        <div class="setting-item">
          <label class="label">API Key</label>
          <div class="input-group">
            <input
              v-model="settings.api_key"
              :type="showApiKey ? 'text' : 'password'"
              class="input"
              placeholder="请输入 API Key"
              @blur="saveSetting('api_key')"
            />
            <button class="btn-icon" @click="showApiKey = !showApiKey" :title="showApiKey ? '隐藏' : '显示'">
              <!-- Eye icon -->
              <svg v-if="!showApiKey" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
              <!-- Eye off icon -->
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                <line x1="1" y1="1" x2="23" y2="23" />
              </svg>
            </button>
          </div>
        </div>

      </section>

      <!-- 任务设置 -->
      <section class="settings-section">
        <h2 class="section-title">任务设置</h2>

        <div class="setting-item">
          <label class="label">并发线程数 (1-10)</label>
          <input
            v-model="settings.thread_pool_size"
            class="input"
            type="number"
            min="1"
            max="10"
            @blur="saveSetting('thread_pool_size')"
          />
        </div>

        <div class="setting-item">
          <label class="label">自动下载</label>
          <div class="toggle-row">
            <button
              class="toggle"
              :class="{ on: settings.auto_download === 'true' }"
              @click="toggleAutoDownload"
            >
              <span class="toggle-knob"></span>
            </button>
            <span class="toggle-label">{{ settings.auto_download === 'true' ? '已开启' : '已关闭' }}</span>
          </div>
        </div>

        <div class="setting-item">
          <label class="label">下载路径</label>
          <div class="input-group">
            <input
              v-model="settings.download_path"
              class="input"
              placeholder="选择图片保存目录"
              readonly
            />
            <button class="btn-icon" @click="selectDownloadPath" title="选择目录">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
              </svg>
            </button>
          </div>
        </div>
      </section>

      <!-- 文件状态 -->
      <section class="settings-section">
        <h2 class="section-title">数据与日志</h2>

        <div class="file-status-card">
          <div class="status-row">
            <div class="status-info">
              <span class="status-label">数据库</span>
              <span class="status-path">{{ fileStatus.db_path }}</span>
            </div>
            <span class="status-size">{{ formatSize(fileStatus.db_size) }}</span>
          </div>

          <div class="status-divider"></div>

          <div class="status-row">
            <div class="status-info">
              <span class="status-label">日志目录</span>
              <span class="status-path">{{ fileStatus.log_dir }}</span>
            </div>
            <div class="status-right">
              <span class="status-badge">{{ fileStatus.log_file_count }} 个文件</span>
              <span class="status-size">{{ formatSize(fileStatus.log_total_size) }}</span>
            </div>
          </div>

          <div class="status-divider"></div>

          <div class="status-row">
            <div class="status-info">
              <span class="status-label">当前日志</span>
              <span class="status-path">{{ fileStatus.log_current_file }}</span>
            </div>
          </div>
        </div>

        <button class="btn btn-danger" @click="clearLogs" :disabled="clearingLogs">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6" />
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
          </svg>
          {{ clearingLogs ? '清理中...' : '清理旧日志' }}
        </button>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const settings = reactive({
  api_key: '',
  thread_pool_size: '2',
  auto_download: 'false',
  download_path: '',
})

const WEBSITE_URL = 'https://hetang.lyvideo.top/register?aff=7yl6'

const showApiKey = ref(false)
const clearingLogs = ref(false)

const fileStatus = reactive({
  log_dir: '',
  log_current_file: '',
  log_file_count: 0,
  log_total_size: 0,
  db_path: '',
  db_size: 0,
})

onMounted(async () => {
  await loadSettings()
  await loadFileStatus()
})

async function loadSettings() {
  try {
    const all = await window.pywebview.api.get_all_settings()
    Object.assign(settings, all)
  } catch (err) {
    console.error('加载设置失败', err)
  }
}

async function saveSetting(key) {
  try {
    await window.pywebview.api.set_setting(key, settings[key])
  } catch (err) {
    console.error('保存设置失败', err)
  }
}

async function loadFileStatus() {
  try {
    const status = await window.pywebview.api.get_file_status()
    Object.assign(fileStatus, status)
  } catch (err) {
    console.error('获取文件状态失败', err)
  }
}

async function clearLogs() {
  clearingLogs.value = true
  try {
    await window.pywebview.api.clear_logs()
    await loadFileStatus()
  } catch (err) {
    console.error('清理日志失败', err)
  } finally {
    clearingLogs.value = false
  }
}

async function toggleAutoDownload() {
  settings.auto_download = settings.auto_download === 'true' ? 'false' : 'true'
  await saveSetting('auto_download')
}

async function selectDownloadPath() {
  try {
    const path = await window.pywebview.api.select_download_path()
    if (path) {
      settings.download_path = path
      await saveSetting('download_path')
    }
  } catch (err) {
    console.error('选择目录失败', err)
  }
}

async function openWebsite() {
  try {
    await window.pywebview.api.open_external_url(WEBSITE_URL)
  } catch (err) {
    console.error('打开网页失败', err)
  }
}

function formatSize(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB']
  let i = 0
  let size = bytes
  while (size >= 1024 && i < units.length - 1) {
    size /= 1024
    i++
  }
  return `${size.toFixed(i === 0 ? 0 : 1)} ${units[i]}`
}
</script>

<style scoped>
.settings-view {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.view-header {
  padding: 20px 28px 0;
  flex-shrink: 0;
}

.view-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.3px;
}

.settings-body {
  flex: 1;
  padding: 20px 28px 28px;
  overflow-y: auto;
  max-width: 640px;
}

.settings-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}

.setting-item {
  margin-bottom: 16px;
}

.input-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

.input-group .input {
  flex: 1;
}

.btn-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
  flex-shrink: 0;
}

.btn-icon:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

/* 文件状态卡片 */
.file-status-card {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 4px 0;
  margin-bottom: 16px;
}

.status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  gap: 12px;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.status-label {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.status-path {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.status-size {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  font-weight: 500;
  flex-shrink: 0;
}

.status-badge {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  background: var(--bg-elevated);
  padding: 2px 8px;
  border-radius: 10px;
}

.status-divider {
  height: 1px;
  background: var(--border);
  margin: 0 14px;
}

/* Toggle 开关 */
.toggle-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.toggle {
  width: 40px;
  height: 22px;
  border-radius: 11px;
  border: none;
  background: var(--bg-elevated);
  cursor: pointer;
  position: relative;
  transition: background var(--transition-normal);
  padding: 0;
}

.toggle.on {
  background: var(--accent);
}

.toggle-knob {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  transition: transform var(--transition-normal);
}

.toggle.on .toggle-knob {
  transform: translateX(18px);
}

.toggle-label {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

/* 官网链接 */
.website-link {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--accent);
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-normal);
}
.website-link:hover {
  background: rgba(91, 91, 214, 0.08);
  border-color: rgba(91, 91, 214, 0.3);
}
.website-link svg {
  flex-shrink: 0;
}
</style>
