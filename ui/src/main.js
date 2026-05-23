import './style.css'

const app = document.querySelector('#app')

app.innerHTML = `
  <div class="app-shell">
    <div class="app-main">
      <aside class="sidebar left" aria-label="AI 组织架构与资源调度矩阵">
        <div class="sidebar-top">
          <div>
            <p class="eyebrow">左侧边栏</p>
            <h2>AI 组织架构与资源调度矩阵</h2>
          </div>
          <button class="ghost-button" data-action="toggle-left">左手扇巴掌 · 收起</button>
        </div>
        <div class="sidebar-tabs" role="tablist">
          <button class="tab is-active" role="tab" aria-selected="true" data-tab="workstation">🟢 工位页</button>
          <button class="tab" role="tab" aria-selected="false" data-tab="log">🟡 流水日志</button>
          <button class="tab" role="tab" aria-selected="false" data-tab="task">🟣 事务大厅</button>
        </div>
        <div class="sidebar-panels">
          <section class="panel is-active" role="tabpanel" data-panel="workstation">
            <div class="ai-card">
              <div class="avatar">④</div>
              <div class="ai-info">
                <h3>⑤ Coder-02</h3>
                <p>前端工程师 · 接力中</p>
              </div>
              <div class="ai-actions">
                <button class="icon-button">⑥ ⚙️</button>
                <button class="icon-button">⑦ 🧰</button>
              </div>
              <div class="status">
                <span class="status-dot busy"></span>
                <span>⑧ 忙碌</span>
              </div>
            </div>
            <div class="ai-card">
              <div class="avatar">④</div>
              <div class="ai-info">
                <h3>⑤ Artist-08</h3>
                <p>视觉设计 · 待命</p>
              </div>
              <div class="ai-actions">
                <button class="icon-button">⑥ ⚙️</button>
                <button class="icon-button">⑦ 🧰</button>
              </div>
              <div class="status">
                <span class="status-dot idle"></span>
                <span>⑧ 空闲</span>
              </div>
            </div>
            <div class="ai-card">
              <div class="avatar">④</div>
              <div class="ai-info">
                <h3>⑤ Planner-01</h3>
                <p>调度规划 · 思考中</p>
              </div>
              <div class="ai-actions">
                <button class="icon-button">⑥ ⚙️</button>
                <button class="icon-button">⑦ 🧰</button>
              </div>
              <div class="status">
                <span class="status-dot thinking"></span>
                <span>⑧ 思考</span>
              </div>
            </div>
          </section>
          <section class="panel" role="tabpanel" data-panel="log">
            <div class="log-entry">EA-141 正在生产图片 · 12:30</div>
            <div class="log-entry">Coder-02 正在检索 GitHub · 12:31</div>
            <div class="log-entry">Planner-01 完成任务拆解 · 12:33</div>
            <div class="log-entry">Writer-05 打包交付至办公桌面 · 12:34</div>
          </section>
          <section class="panel" role="tabpanel" data-panel="task">
            <div class="task-card">
              <h3>UI 壳子搭建</h3>
              <p>吉祥物拆解：布局 + 交互骨架 + 视觉气氛。</p>
              <div class="task-meta">#1_implementation_needed</div>
            </div>
            <div class="task-card">
              <h3>插件投放矩阵</h3>
              <p>输出到 GitHub、画廊、办公桌面。</p>
              <div class="task-meta">#2_analysis_required</div>
            </div>
          </section>
        </div>
      </aside>

      <main class="canvas" aria-label="大管家沟通画布">
        <div class="mascot-strip">
          <div class="mascot-card">
            <div class="mascot-avatar">⑨</div>
            <div>
              <h2>吉祥物 · 主控交互体</h2>
              <p>中央对话对象，负责调度整个系统。</p>
            </div>
            <div class="mascot-actions">
              <button class="hand-button" data-action="toggle-left">左手扇巴掌</button>
              <button class="hand-button" data-action="toggle-right">右手抓取</button>
            </div>
          </div>
          <div class="emotion-card">
            <p class="eyebrow">⑩ 情绪牌</p>
            <h3>“天气有点热，考虑来个冰激凌？”</h3>
            <p>点击后放大到⑯页面进行设置。</p>
          </div>
        </div>
        <section class="chat-canvas">
          <header>
            <h2>⑯ 大管家沟通画布</h2>
            <p>日常对话 / #号触发宏观指令</p>
          </header>
          <div class="chat-stream">
            <div class="bubble mascot">今天想让工厂处理什么大目标？</div>
            <div class="bubble user">先把 UI 壳子搭出来。</div>
            <div class="bubble mascot">已拆解任务并投放到事务大厅。</div>
          </div>
        </section>
      </main>

      <aside class="sidebar right" aria-label="交付终端与插件生态">
        <div class="sidebar-top">
          <div>
            <p class="eyebrow">右侧边栏</p>
            <h2>交付终端与插件生态</h2>
          </div>
          <button class="ghost-button" data-action="toggle-right">右手抓取 · 收起</button>
        </div>
        <div class="plugin-grid">
          <div class="plugin-card">
            <h3>GitHub 网页插件</h3>
            <p>程序员提交代码的终点。</p>
          </div>
          <div class="plugin-card">
            <h3>画廊展览馆</h3>
            <p>美术交付设计图。</p>
          </div>
          <div class="plugin-card">
            <h3>办公桌面</h3>
            <p>文案报告与资料归档。</p>
          </div>
          <div class="plugin-card">
            <h3>自定义插件</h3>
            <p>可扩展的接收矩阵。</p>
          </div>
        </div>
      </aside>
    </div>

    <footer class="input-bar" aria-label="底部输入控制区">
      <div class="input-main">
        <div class="input-field">
          <label>⑫ 主文本输入框</label>
          <input type="text" placeholder="对吉祥物说点什么..." />
        </div>
        <div class="input-actions">
          <button class="action-button" data-action="toggle-models">⑬ 模型切换</button>
          <button class="action-button">14 上传</button>
          <button class="action-button voice" data-action="toggle-voice">⑮ 多态语音按键</button>
        </div>
      </div>
      <div class="model-panel">
        <div class="model-panel-header">
          <h3>模型配置表</h3>
          <button class="ghost-button" data-action="toggle-models">返回输入</button>
        </div>
        <div class="model-list">
          <button class="model-chip">Gemini Ultra</button>
          <button class="model-chip">Claude 3.5</button>
          <button class="model-chip">GPT-5</button>
          <button class="model-chip">定制 Agent</button>
        </div>
      </div>
      <div class="voice-status">实时待机监听模式已激活</div>
    </footer>
  </div>
`

const shell = app.querySelector('.app-shell')
const leftSidebar = shell.querySelector('.sidebar.left')
const rightSidebar = shell.querySelector('.sidebar.right')
const inputBar = shell.querySelector('.input-bar')

const setActiveTab = (tabName) => {
  const tabs = shell.querySelectorAll('.tab')
  const panels = shell.querySelectorAll('.panel')
  tabs.forEach((tab) => {
    const isActive = tab.dataset.tab === tabName
    tab.classList.toggle('is-active', isActive)
    tab.setAttribute('aria-selected', isActive ? 'true' : 'false')
  })
  panels.forEach((panel) => {
    panel.classList.toggle('is-active', panel.dataset.panel === tabName)
  })
}

shell.addEventListener('click', (event) => {
  const actionButton = event.target.closest('[data-action]')
  if (actionButton) {
    const { action } = actionButton.dataset
    if (action === 'toggle-left') {
      shell.classList.toggle('left-collapsed')
      leftSidebar.classList.toggle('is-collapsed')
    }
    if (action === 'toggle-right') {
      shell.classList.toggle('right-collapsed')
      rightSidebar.classList.toggle('is-collapsed')
    }
    if (action === 'toggle-models') {
      inputBar.classList.toggle('is-models')
    }
    if (action === 'toggle-voice') {
      inputBar.classList.toggle('is-listening')
    }
  }

  const tabButton = event.target.closest('[data-tab]')
  if (tabButton) {
    setActiveTab(tabButton.dataset.tab)
  }
})
