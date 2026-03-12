<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { Timer, Headphones, Shield, Activity, X, Play, Pause, RotateCcw, Volume2, Info } from 'lucide-svelte';
  import { user } from '$lib/stores/auth';

  let time = 25 * 60;
  let isActive = false;
  let interval: any;
  let selectedSound = 'Silence';
  let blockStatus = 'Active';
  let mounted = false;
  let sessionCompleted = false;

  $: minutes = Math.floor(time / 60);
  $: seconds = time % 60;
  $: displayTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

  function toggleTimer() {
    isActive = !isActive;
    if (isActive) {
        interval = setInterval(() => {
            if (time > 0) {
                time--;
            } else {
                completeSession();
            }
        }, 1000);
    } else {
        clearInterval(interval);
    }
  }

  function resetTimer() {
    clearInterval(interval);
    isActive = false;
    time = 25 * 60;
  }

  function completeSession() {
    clearInterval(interval);
    isActive = false;
    sessionCompleted = true;
    // Notify sound etc.
  }

  onMount(() => {
    mounted = true;
  });

  onDestroy(() => {
    clearInterval(interval);
  });
</script>

<svelte:head>
  <title>Deep Work — {displayTime}</title>
</svelte:head>

<div class="deep-work-page" class:mounted>
  <div class="top-nav">
    <a href="/dashboard" class="back-link"><X size={18} /> Exit Deep Work</a>
    <div class="status-indicators">
        <div class="indicator">
            <Shield size={14} class="shield-icon" />
            <span>Blocker: {blockStatus}</span>
        </div>
        <div class="indicator">
            <Activity size={14} class="load-icon" />
            <span>Load: 42%</span>
        </div>
    </div>
  </div>

  <main class="focus-arena">
    <div class="focus-header">
        <h1 class="title">Deep Work</h1>
        <p class="subtitle">No distractions. Just performance.</p>
    </div>

    <div class="timer-orb">
        <div class="orb-inner">
            <div class="time-display">{displayTime}</div>
            <div class="session-label">Focus Flow</div>
        </div>
        <svg viewBox="0 0 100 100" class="timer-svg">
            <circle cx="50" cy="50" r="48" class="timer-track" />
            <circle cx="50" cy="50" r="48" class="timer-progress" style="stroke-dashoffset: {301.59 * (1 - time / (25 * 60))}px" />
        </svg>
    </div>

    <div class="controls">
        <button class="reset-btn" on:click={resetTimer}><RotateCcw size={20} /></button>
        <button class="main-btn" on:click={toggleTimer}>
            {#if isActive}
                <Pause size={24} fill="currentColor" />
            {:else}
                <Play size={24} fill="currentColor" />
            {/if}
        </button>
        <button class="settings-btn"><Info size={20} /></button>
    </div>

    <div class="soundscapes">
        {#each ['Silence', 'Lo-Fi', 'Rain', 'Forest', 'Static'] as sound}
            <button 
                class="sound-chip" 
                class:active={selectedSound === sound}
                on:click={() => selectedSound = sound}
            >
                <Headphones size={12} />
                {sound}
            </button>
        {/each}
    </div>
  </main>

  <div class="page-footer">
    <div class="footer-metric">
        <Volume2 size={16} />
        <input type="range" class="vol-slider" min="0" max="100" />
    </div>
    <div class="footer-center">
        <span>Deep work sessions contribute to your <strong>Resilience Score</strong>.</span>
    </div>
    <div class="footer-right">
        <span>Goal: 4/5h today</span>
    </div>
  </div>
</div>

{#if sessionCompleted}
<div class="completion-overlay">
    <div class="modal">
        <h2 class="modal-title">Session Complete</h2>
        <p class="modal-body">Great focus! Your cognitive load is recovering. Take 5 minutes to rest.</p>
        <button class="modal-btn" on:click={() => sessionCompleted = false}>Continue</button>
    </div>
</div>
{/if}

<style>
  .deep-work-page {
    position: fixed;
    inset: 0;
    background: var(--bg);
    display: flex;
    flex-direction: column;
    z-index: 1000;
    opacity: 0;
    transition: opacity 1s ease;
    font-family: var(--font-sans);
  }

  .deep-work-page.mounted { opacity: 1; }

  .top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 40px;
  }

  .back-link {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.2s;
  }

  .back-link:hover { color: var(--text-primary); }

  .status-indicators {
    display: flex;
    gap: 24px;
  }

  .indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
  }

  .shield-icon { color: var(--accent); }
  .load-icon { color: #f59e0b; }

  .focus-arena {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 48px;
  }

  .focus-header {
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .title {
    font-size: 32px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin: 0;
  }

  .subtitle {
    font-size: 14px;
    color: var(--text-muted);
    margin: 0;
  }

  .timer-orb {
    position: relative;
    width: 280px;
    height: 280px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .orb-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    z-index: 1;
  }

  .time-display {
    font-family: var(--font-mono);
    font-size: 72px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: .9;
  }

  .session-label {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent);
    opacity: 0.8;
  }

  .timer-svg {
    position: absolute;
    inset: -20px;
    width: calc(100% + 40px);
    height: calc(100% + 40px);
    transform: rotate(-90deg);
  }

  .timer-track {
    fill: none;
    stroke: rgba(255,255,255,0.03);
    stroke-width: 2;
  }

  .timer-progress {
    fill: none;
    stroke: var(--accent);
    stroke-width: 2;
    stroke-dasharray: 301.59;
    stroke-linecap: round;
    transition: stroke-dashoffset 1s linear;
    filter: drop-shadow(0 0 8px var(--accent-glow));
  }

  .controls {
    display: flex;
    align-items: center;
    gap: 32px;
  }

  .main-btn {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: var(--accent);
    color: var(--bg);
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 0 32px var(--accent-glow);
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .main-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 48px var(--accent-glow);
  }

  .reset-btn, .settings-btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
  }

  .reset-btn:hover, .settings-btn:hover {
    color: var(--text-primary);
    border-color: rgba(255,255,255,0.15);
  }

  .soundscapes {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
    max-width: 400px;
  }

  .sound-chip {
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 8px 16px;
    border-radius: 9999px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .sound-chip:hover {
    border-color: rgba(255,255,255,0.15);
  }

  .sound-chip.active {
    background: var(--accent-glow);
    border-color: var(--accent);
    color: var(--accent);
  }

  .page-footer {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    align-items: center;
    padding: 24px 40px;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 12px;
  }

  .footer-metric {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .vol-slider {
    width: 100px;
    accent-color: var(--accent);
  }

  .footer-center { text-align: center; }
  .footer-right { text-align: right; font-weight: 600; color: var(--text-primary); }

  /* Completion Modal */
  .completion-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.8);
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
  }

  .modal {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 40px;
    border-radius: 24px;
    max-width: 400px;
    width: 90%;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 16px;
    animation: zoomIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .modal-title { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0; }
  .modal-body { font-size: 15px; color: var(--text-muted); line-height: 1.6; margin: 0; }
  .modal-btn {
    background: var(--accent);
    color: var(--bg);
    border: none;
    padding: 12px;
    border-radius: 12px;
    font-weight: 700;
    cursor: pointer;
    margin-top: 8px;
  }

  @keyframes zoomIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
  }
</style>