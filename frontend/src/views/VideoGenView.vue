<template>
  <div class="video-gen">
    <header class="view-header">
      <h1 class="view-title">视频生成</h1>
    </header>

    <div class="view-body">
      <div class="coming-soon">
        <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25">
          <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18" />
          <line x1="7" y1="2" x2="7" y2="22" />
          <line x1="17" y1="2" x2="17" y2="22" />
          <line x1="2" y1="12" x2="22" y2="12" />
          <line x1="2" y1="7" x2="7" y2="7" />
          <line x1="2" y1="17" x2="7" y2="17" />
          <line x1="17" y1="7" x2="22" y2="7" />
          <line x1="17" y1="17" x2="22" y2="17" />
        </svg>
        <h2 class="coming-title">即将推出</h2>
        <p class="coming-desc">视频生成功能正在开发中，敬请期待</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.video-gen {
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

.view-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.coming-soon {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.coming-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-secondary);
}

.coming-desc {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}
</style>
