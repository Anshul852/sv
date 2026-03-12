<script lang="ts">
  import { AlertTriangle, Clock, Zap, Brain, Coffee, UserMinus, ShieldAlert, ArrowRight, Activity, Thermometer } from 'lucide-svelte';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';

  let subject = $page.url.searchParams.get('subject') || 'Final Exam';
  let hoursLeft = parseInt($page.url.searchParams.get('hours') || '24');
  let activated = false;
  let mounted = false;

  const crunchPlan = [
    { time: 'Next 4h', task: 'High-intensity Practice Papers', type: 'practice', icon: Zap },
    { time: '2h from now', task: 'Review Weak Topics', type: 'review', icon: Brain },
    { time: 'Tonight', task: 'Mandatory 6h Recovery Sleep', type: 'sleep', icon: Coffee },
    { time: 'Last 2h', task: 'Quick Recall & Formula Check', type: 'recall', icon: Thermometer }
  ];

  onMount(() => mounted = true);

  function activate() {
    activated = true;
  }
</script>

<div class="crisis-page" class:mounted class:active={activated}>
  <div class="background-glow"></div>

  <header class="page-header">
    <div class="header-left">
        <div class="alert-icon">
            <ShieldAlert size={24} />
        </div>
        <div>
            <h1 class="page-title">Crisis Mode</h1>
            <p class="page-sub">High-Intensity Exam Prep Active</p>
        </div>
    </div>
    <div class="countdown">
        <div class="val">{hoursLeft}</div>
        <div class="unit">Hours<br>Until Exam</div>
    </div>
  </header>

  <main class="crisis-grid">
    <section class="plan-section">
        <div class="section-card">
            <div class="sec-header">
                <h2 class="sec-title">72h Crunch Plan: {subject}</h2>
                <span class="status-tag">Plan Tightened</span>
            </div>

            <div class="timeline">
                {#each crunchPlan as step}
                    <div class="timeline-step">
                        <div class="step-icon">
                            <svelte:component this={step.icon} size={18} />
                        </div>
                        <div class="step-content">
                            <span class="step-time">{step.time}</span>
                            <h3 class="step-task">{step.task}</h3>
                        </div>
                        <button class="step-btn">Ready</button>
                    </div>
                {/each}
            </div>

            {#if !activated}
                <button class="activate-btn" on:click={activate}>
                    Activate Final Crunch Protocol
                    <ArrowRight size={18} />
                </button>
            {:else}
                <div class="protocol-active">
                    <Activity size={16} />
                    <span>Protocol SV-92 Alpha Active: All notifications suppressed.</span>
                </div>
            {/if}
        </div>

        <div class="section-card metrics-row">
            <div class="metric">
                <span class="m-label">Efficiency Required</span>
                <span class="m-val">94%</span>
            </div>
            <div class="metric">
                <span class="m-label">Estimated Anxiety</span>
                <span class="m-val high">High</span>
            </div>
            <div class="metric">
                <span class="m-label">Hydration</span>
                <span class="m-val">Good</span>
            </div>
        </div>
    </section>

    <aside class="advice-panel">
        <div class="section-card advice-card">
            <h3 class="sec-title">Crisis Advice</h3>
            <ul class="advice-list">
                <li>
                    <Coffee size={14} />
                    <strong>Stop Caffeine at 6h out.</strong> Over-caffeine will ruin your recall.
                </li>
                <li>
                    <UserMinus size={14} />
                    <strong>Silence all non-essential humans.</strong> This is your solo sprint.
                </li>
                <li>
                    <AlertTriangle size={14} />
                    <strong>Identity weak points early.</strong> Don't try to learn everything; shore up the high-yield topics.
                </li>
            </ul>
        </div>

        <div class="section-card stress-meter">
            <div class="meter-header">
                <h3 class="sec-title">Stress Level</h3>
                <Thermometer size={14} />
            </div>
            <div class="bar-container">
                <div class="bar-fill" style="width: 82%"></div>
            </div>
            <p class="sec-sub">Take 3 deep breaths if you feel your heart racing above 100bpm.</p>
        </div>
    </aside>
  </main>
</div>

<style>
  .crisis-page {
    /* Crisis is defined by Orange/Red theme */
    --accent: #fb923c;
    --accent-glow: rgba(251,146,60,0.2);
    --border: rgba(251,146,60,0.15);
    
    font-family: var(--font-sans);
    padding: 28px 32px 48px;
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 32px;
    opacity: 0;
    transition: all 0.6s ease;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
  }

  .crisis-page.mounted { opacity: 1; transform: translateY(0); }

  .crisis-page.active {
    --accent: #ef4444;
    --accent-glow: rgba(239,68,68,0.2);
    --border: rgba(239,68,68,0.3);
  }

  .background-glow {
    position: absolute;
    top: -100px;
    right: -100px;
    width: 400px;
    height: 400px;
    background: var(--accent-glow);
    filter: blur(80px);
    border-radius: 50%;
    z-index: -1;
    transition: background 1s ease;
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .header-left { display: flex; gap: 16px; align-items: center; }

  .alert-icon {
    width: 60px;
    height: 60px;
    background: var(--accent-glow);
    color: var(--accent);
    border: 1px solid var(--border);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 20px var(--accent-glow);
  }

  .page-title { font-size: 32px; font-weight: 800; color: var(--text-primary); margin: 0; letter-spacing: -0.02em; }
  .page-sub { font-size: 14px; font-weight: 600; color: var(--accent); margin: 4px 0 0; text-transform: uppercase; letter-spacing: 0.1em; }

  .countdown {
    display: flex;
    align-items: center;
    gap: 16px;
    background: var(--surface);
    border: 2px solid var(--accent);
    padding: 12px 24px;
    border-radius: 16px;
    box-shadow: 0 0 24px var(--accent-glow);
  }

  .countdown .val { font-family: var(--font-mono); font-size: 44px; font-weight: 800; color: var(--text-primary); line-height: 1; }
  .countdown .unit { font-size: 10px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); line-height: 1.2; }

  .crisis-grid {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 24px;
  }

  .section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .sec-header { display: flex; justify-content: space-between; align-items: center; }
  .sec-title { font-size: 18px; font-weight: 700; color: var(--text-primary); margin: 0; }
  .status-tag { font-size: 10px; font-weight: 700; background: var(--accent-glow); color: var(--accent); padding: 4px 10px; border-radius: 6px; }

  .timeline { display: flex; flex-direction: column; gap: 8px; }

  .timeline-step {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    border-radius: 12px;
  }

  .step-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
  }

  .step-content { flex: 1; display: flex; flex-direction: column; gap: 2px; }
  .step-time { font-size: 10px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }
  .step-task { font-size: 14px; font-weight: 600; color: var(--text-primary); margin: 0; }

  .step-btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 11px;
    font-weight: 700;
    padding: 6px 12px;
    border-radius: 8px;
    cursor: pointer;
  }

  .activate-btn {
    background: var(--accent);
    color: var(--bg);
    border: none;
    padding: 18px;
    border-radius: 14px;
    font-size: 16px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    cursor: pointer;
    box-shadow: 0 4px 24px var(--accent-glow);
    transition: all 0.2s;
  }

  .activate-btn:hover { transform: scale(1.02); filter: brightness(1.1); }

  .protocol-active {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid #ef4444;
    padding: 14px;
    border-radius: 12px;
    display: flex;
    gap: 12px;
    align-items: center;
    color: #ef4444;
    font-size: 13px;
    font-weight: 600;
  }

  .metrics-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; text-align: center; }
  .metric { display: flex; flex-direction: column; gap: 4px; }
  .m-label { font-size: 10px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }
  .m-val { font-family: var(--font-mono); font-size: 24px; font-weight: 700; color: var(--text-primary); }
  .m-val.high { color: #ef4444; }

  .advice-panel { display: flex; flex-direction: column; gap: 24px; }

  .advice-list { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 20px; }
  .advice-list li { display: flex; gap: 12px; font-size: 13px; color: var(--text-primary); line-height: 1.5; }
  .advice-list li strong { color: var(--accent); }

  .meter-header { display: flex; justify-content: space-between; align-items: center; }
  .bar-container { height: 8px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow: hidden; margin: 12px 0; }
  .bar-fill { height: 100%; background: linear-gradient(90deg, #fb923c, #ef4444); }

  @media (max-width: 850px) {
    .crisis-grid { grid-template-columns: 1fr; }
    .advice-panel { order: -1; }
  }
</style>
