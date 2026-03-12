<script lang="ts">
    import { onMount } from 'svelte';
    import { themeStore, presetThemes, defaultTheme }
        from '$lib/stores/themeStore'
    import type { Theme } from '$lib/stores/themeStore'
    import { Check, RotateCcw, Save, Palette,
             Type, Eye, EyeOff } from 'lucide-svelte'
    import AppSidebar from '$lib/components/AppSidebar.svelte';

    let theme: Theme
    let savedFeedback = false
    let showPreview = true
    let mounted = false

    themeStore.subscribe(t => theme = t)

    function handleFontChange(event: Event) {
        const target = event.target as HTMLSelectElement;
        themeStore.setToken('fontSans', target.value);
    }

    function handleColorChange(key: keyof Theme, value: string) {
        themeStore.setToken(key, value)
    }

    function handleTextInput(token: any, event: Event) {
        const target = event.target as HTMLInputElement;
        handleColorChange(token.key as keyof Theme, target.value);
    }

    function handleColorInput(token: any, event: Event) {
        const target = event.target as HTMLInputElement;
        handleColorChange(token.key as keyof Theme, target.value);
    }

    function handleRadiusChange(value: string) {
        themeStore.setToken('radiusCard', value);
    }

    function getThemeValue(tokenKey: string): string {
        return theme[tokenKey as keyof Theme] as string;
    }

    function setThemeValue(tokenKey: string, value: string) {
        themeStore.setToken(tokenKey as keyof Theme, value);
    }

    function handleSave() {
        themeStore.save(theme)
        savedFeedback = true
        setTimeout(() => savedFeedback = false, 2000)
    }

    function handleReset() {
        themeStore.reset()
    }

    function handlePreset(preset: Theme) {
        themeStore.applyPreset(preset)
    }

    onMount(() => {
        setTimeout(() => mounted = true, 500)
    })

    const colorGroups = [
        {
            label: 'BACKGROUNDS',
            tokens: [
                { key: 'bg',      label: 'Page Background' },
                { key: 'surface', label: 'Card Surface' }
            ]
        },
        {
            label: 'ACCENT',
            tokens: [
                { key: 'accent', label: 'Primary Accent' }
            ]
        },
        {
            label: 'TEXT',
            tokens: [
                { key: 'textPrimary', label: 'Primary Text' },
                { key: 'textMuted',   label: 'Muted Text' }
            ]
        },
        {
            label: 'STATUS',
            tokens: [
                { key: 'colorHard',   label: 'Hard Topics' },
                { key: 'colorMedium', label: 'Medium Topics' },
                { key: 'colorEasy',   label: 'Easy Topics' },
                { key: 'colorReview', label: 'Review Sessions' }
            ]
        }
    ]

    const radiusOptions = [
        { label: 'Sharp',   value: '4px'  },
        { label: 'Rounded', value: '10px' },
        { label: 'Pill',    value: '24px' }
    ]

    const fontOptions = [
        { label: 'Inter',         value: 'Inter, sans-serif'         },
        { label: 'Geist',         value: 'Geist, sans-serif'         },
        { label: 'DM Sans',       value: 'DM Sans, sans-serif'       },
        { label: 'Outfit',        value: 'Outfit, sans-serif'        },
        { label: 'Space Grotesk', value: 'Space Grotesk, sans-serif' }
    ]
</script>

<svelte:head>
  <title>Theme Editor — StudyVault</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link
    href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<div class="app-layout" class:mounted>
  <!-- Sidebar -->
  <AppSidebar />

  <!-- Main Content -->
  <div class="main-content">

    <!-- Meta row -->
    <div class="meta-row">
      <span class="meta-date">THEME EDITOR</span>
      <div class="priv-badge">
        <Palette size={10} strokeWidth={2.5} />
        Live Preview
      </div>
    </div>

    <!-- Header -->
    <header class="greet-row">
      <h1>Theme <span class="name-hi">Editor</span></h1>
      <div class="hdr-actions">
        <button class="ghost-btn" on:click={() => showPreview = !showPreview}>
          {#if showPreview}
            <EyeOff size={12} />
          {:else}
            <Eye size={12} />
          {/if}
          {showPreview ? 'Hide' : 'Show'} Preview
        </button>
        <button class="accent-btn" on:click={handleSave}>
          {#if savedFeedback}
            <Check size={12} />
            Saved!
          {:else}
            <Save size={12} />
            Save Theme
          {/if}
        </button>
      </div>
    </header>

    <!-- Editor Layout -->
    <div class="editor-layout" class:no-preview={!showPreview}>

      <!-- Left Panel - Controls -->
      <div class="editor-panel">

        <!-- Presets -->
        <div class="editor-section">
          <div class="section-header">
            <Palette size={14} />
            <span>Presets</span>
          </div>
          <div class="preset-grid">
            {#each Object.entries(presetThemes) as [name, preset]}
              <button class="preset-btn" on:click={() => handlePreset(preset)}>
                <span class="preset-dot" style="background: {preset.accent}"></span>
                {name}
              </button>
            {/each}
          </div>
        </div>

        <!-- Color Token Groups -->
        {#each colorGroups as group}
          <div class="editor-section">
            <span class="section-label">{group.label}</span>
            <div class="token-list">
              {#each group.tokens as token}
                <div class="token-item">
                  <span class="token-label">{token.label}</span>
                  <div class="token-controls">
                    <input
                      type="text"
                      value={getThemeValue(token.key)}
                      on:input={(e) => handleTextInput(token, e)}
                      class="hex-input"
                    />
                    <div class="color-picker-wrapper">
                      <div class="color-preview" style="background: {getThemeValue(token.key)}"></div>
                      <input
                        type="color"
                        value={getThemeValue(token.key)}
                        on:input={(e) => handleColorInput(token, e)}
                        class="color-input"
                      />
                    </div>
                  </div>
                </div>
              {/each}
            </div>
          </div>
        {/each}

        <!-- Border Radius -->
        <div class="editor-section">
          <span class="section-label">BORDER RADIUS</span>
          <div class="radius-group">
            {#each radiusOptions as option}
              <button
                class="radius-btn"
                class:selected={theme.radiusCard === option.value}
                style="border-radius: {option.value}"
                on:click={() => handleRadiusChange(option.value)}
              >
                {option.label}
              </button>
            {/each}
          </div>
        </div>

        <!-- Typography -->
        <div class="editor-section">
          <span class="section-label">TYPOGRAPHY</span>
          <div class="control-group">
            <label class="control-label" for="font-select">Font Family</label>
            <select
              id="font-select"
              value={theme.fontSans}
              on:change={handleFontChange}
              class="control-select"
            >
              {#each fontOptions as font}
                <option value={font.value}>{font.label}</option>
              {/each}
            </select>
          </div>
        </div>

        <!-- Reset -->
        <div class="editor-section">
          <button class="reset-btn" on:click={handleReset}>
            <RotateCcw size={14} />
            Reset to Default
          </button>
        </div>

      </div><!-- /editor-panel -->

      <!-- Right Panel - Preview -->
      {#if showPreview}
        <div class="preview-panel">
          <div class="preview-header">Live Preview</div>
          <div class="preview-content">

            <!-- Preview Card -->
            <div class="preview-card">
              <div class="preview-greeting">
                Good morning,
                <span style="color: var(--accent)">Student</span>
              </div>
              <p class="preview-subtext">4 sessions planned today</p>

              <div class="preview-stats">
                {#each [{ label: 'Sessions', value: '47' }, { label: 'Retention', value: '89%' }] as stat}
                  <div class="preview-stat-box">
                    <div class="stat-value">{stat.value}</div>
                    <div class="stat-label">{stat.label}</div>
                  </div>
                {/each}
              </div>

              <div class="preview-elements">
                {#each [
                  { topic: 'Data Structures', diff: 'hard'   },
                  { topic: 'Machine Learning', diff: 'medium' },
                  { topic: 'Review Session',   diff: 'review' }
                ] as session}
                  <div class="preview-item">
                    <div class="preview-diff" style="background: var(--color-{session.diff})"></div>
                    <span>{session.topic}</span>
                  </div>
                {/each}
              </div>

              <button class="preview-cta">Open Chat</button>

              <div class="preview-input">Message StudyVault AI...</div>
            </div>

            <!-- Accent Swatch -->
            <div class="accent-swatch" style="background: {theme.accent}">
              <p>Accent Color</p>
              <p class="accent-hex">{theme.accent}</p>
            </div>

          </div>
        </div>
      {/if}

    </div><!-- /editor-layout -->
  </div><!-- /main-content -->
</div><!-- /app-layout -->

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ── Global resets ─────────────────────────────────────── */
:global(body) {
  margin: 0;
  background: var(--bg);
  color: var(--text-primary);
  font-family: 'Syne', sans-serif;
  -webkit-font-smoothing: antialiased;
}

:global(*, *::before, *::after) {
  box-sizing: border-box;
}

:global(button) {
  font-family: inherit;
  cursor: pointer;
}

/* ── Design tokens (fallback values) ──────────────────── */
:root {
  --bg:            #060608;
  --surface:       #0c0c10;
  --panel:         #0c0c10;
  --accent:        #b5ff4d;
  --text-primary:  #ffffff;
  --text-muted:    rgba(255, 255, 255, 0.5);
  --border:        rgba(255, 255, 255, 0.07);
  --color-hard:    #ff5555;
  --color-medium:  #ff9500;
  --color-easy:    #b5ff4d;
  --color-review:  #c084fc;
  --radius-card:   10px;
  --radius-btn:    8px;
  --radius-input:  8px;
  --font-sans:     'Syne', sans-serif;
  --mono:          'Space Mono', monospace;
  --dim:           rgba(255, 255, 255, 0.38);
  --red:           #ff5555;
}

/* ── Layout ───────────────────────────────────────────── */
.app-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg);
  opacity: 0;
  transform: translateY(5px);
  transition: opacity 300ms ease, transform 300ms ease;
}

.app-layout.mounted {
  opacity: 1;
  transform: none;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 18px 26px 40px;
  max-width: 1440px;
  margin: 0 auto;
  min-width: 0;
}

/* ── Meta row ─────────────────────────────────────────── */
.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 5px;
}

.meta-date {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--dim);
  letter-spacing: 0.14em;
}

.priv-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(181, 255, 77, 0.07);
  border: 1px solid rgba(181, 255, 77, 0.18);
  border-radius: 20px;
  padding: 4px 12px;
  font-family: var(--mono);
  font-size: 9px;
  color: var(--accent);
}

/* ── Header ───────────────────────────────────────────── */
.greet-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 18px;
}

.greet-row h1 {
  font-size: clamp(20px, 3vw, 34px);
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0;
  color: #fff;
}

.name-hi { color: var(--accent); }

.hdr-actions {
  display: flex;
  gap: 8px;
}

.ghost-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  color: var(--dim);
  transition: border-color 0.15s, color 0.15s;
}

.ghost-btn:hover {
  border-color: rgba(255, 255, 255, 0.16);
  color: rgba(255, 255, 255, 0.7);
}

.accent-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 13px;
  background: var(--accent);
  border: none;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  color: #000;
  transition: filter 0.15s;
}

.accent-btn:hover { filter: brightness(1.08); }

/* ── Editor layout ────────────────────────────────────── */
.editor-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 16px;
}

.editor-layout.no-preview {
  grid-template-columns: 1fr;
}

.editor-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  max-height: calc(100vh - 160px);
  padding-right: 4px;
}

.preview-panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 13px;
  padding: 16px;
  position: sticky;
  top: 20px;
  max-height: calc(100vh - 160px);
  overflow-y: auto;
}

/* ── Editor sections ──────────────────────────────────── */
.editor-section {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 13px;
  padding: 16px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  color: var(--dim);
}

.section-header span,
.section-label {
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: var(--dim);
  display: block;
  margin-bottom: 12px;
}

.section-header span { margin-bottom: 0; }

/* ── Presets ──────────────────────────────────────────── */
.preset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 8px;
}

.preset-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 11px;
  color: var(--text-primary);
  transition: background 0.2s, border-color 0.2s;
}

.preset-btn:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.12);
}

.preset-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* ── Color tokens ─────────────────────────────────────── */
.token-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.token-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.token-label {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 500;
}

.token-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hex-input {
  width: 100px;
  height: 32px;
  padding: 6px 8px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-primary);
  text-align: right;
  outline: none;
  transition: border-color 0.15s;
}

.hex-input:focus { border-color: var(--accent); }

.color-picker-wrapper {
  position: relative;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid var(--border);
  cursor: pointer;
  flex-shrink: 0;
}

.color-preview {
  position: absolute;
  inset: 0;
}

.color-input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
  width: 100%;
  height: 100%;
}

/* ── Border radius picker ─────────────────────────────── */
.radius-group {
  display: flex;
  gap: 8px;
}

.radius-btn {
  flex: 1;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border);
  font-size: 11px;
  font-weight: 600;
  color: var(--text-primary);
  transition: all 0.15s;
}

.radius-btn.selected {
  background: var(--accent);
  border-color: var(--accent);
  color: #0a0a0b;
}

/* ── Typography / select ──────────────────────────────── */
.control-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-label {
  font-size: 12px;
  color: var(--text-primary);
  font-weight: 500;
}

.control-select {
  height: 36px;
  padding: 0 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 12px;
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.15s;
}

.control-select:focus { border-color: var(--accent); }

/* ── Reset button ─────────────────────────────────────── */
.reset-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 10px 16px;
  background: rgba(255, 85, 85, 0.1);
  border: 1px solid rgba(255, 85, 85, 0.2);
  border-radius: 8px;
  font-size: 12px;
  color: var(--red);
  transition: background 0.15s, border-color 0.15s;
}

.reset-btn:hover {
  background: rgba(255, 85, 85, 0.15);
  border-color: rgba(255, 85, 85, 0.3);
}

/* ── Preview panel ────────────────────────────────────── */
.preview-header {
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: var(--dim);
  margin-bottom: 16px;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.preview-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preview-greeting {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: var(--font-sans);
}

.preview-subtext {
  margin: -8px 0 0;
  font-size: 11px;
  color: var(--text-muted);
  font-family: var(--font-sans);
}

.preview-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.preview-stat-box {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-input);
  padding: 10px 12px;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--accent);
  font-family: var(--mono);
}

.stat-label {
  font-size: 10px;
  color: var(--text-muted);
  font-family: var(--mono);
  margin-top: 2px;
}

.preview-elements {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.preview-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border);
  border-radius: var(--radius-input);
  font-size: 12px;
  color: var(--text-primary);
  font-family: var(--font-sans);
}

.preview-diff {
  width: 4px;
  height: 32px;
  border-radius: 99px;
  flex-shrink: 0;
}

.preview-cta {
  width: 100%;
  height: 38px;
  background: var(--accent);
  border: none;
  border-radius: var(--radius-btn);
  font-size: 13px;
  font-weight: 700;
  color: #0a0a0b;
  transition: filter 0.15s;
}

.preview-cta:hover { filter: brightness(1.08); }

.preview-input {
  height: 38px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border);
  border-radius: var(--radius-input);
  font-size: 12px;
  color: var(--text-muted);
  font-family: var(--font-sans);
}

/* ── Accent swatch ────────────────────────────────────── */
.accent-swatch {
  border-radius: var(--radius-card);
  padding: 14px;
  text-align: center;
}

.accent-swatch p {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.8);
  font-family: var(--font-sans);
}

.accent-hex {
  font-family: var(--mono);
  font-size: 10px;
  color: rgba(0, 0, 0, 0.6);
  margin-top: 4px !important;
}

/* ── Responsive ───────────────────────────────────────── */
@media (max-width: 1024px) {
  .editor-layout {
    grid-template-columns: 1fr;
  }

  .preview-panel {
    position: relative;
    top: 0;
    max-height: none;
  }

  .editor-panel {
    max-height: none;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 10px 12px 22px;
  }

  .preset-grid {
    grid-template-columns: 1fr 1fr;
  }

  .preview-stats {
    grid-template-columns: 1fr 1fr;
  }
}
</style>