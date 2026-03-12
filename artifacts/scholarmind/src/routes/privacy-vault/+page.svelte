<script lang="ts">
  import { Shield, Lock, Key, EyeOff, RefreshCw, Smartphone, Download, AlertTriangle, CheckCircle } from 'lucide-svelte';
  import { onMount } from 'svelte';

  let keyGenerated = false;
  let keyLoading = false;
  let showPhrase = false;
  let mounted = false;

  const recoveryPhrase = [
    'alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot',
    'golf', 'hotel', 'india', 'juliet', 'kilo', 'lima'
  ];

  function generateKey() {
    keyLoading = true;
    setTimeout(() => {
        keyGenerated = true;
        keyLoading = false;
    }, 2000);
  }

  onMount(() => mounted = true);
</script>

<div class="privacy-page" class:mounted>
  <header class="page-header">
    <div class="title-wrap">
        <div class="icon-box">
            <Lock size={20} />
        </div>
        <div>
            <h1 class="page-title">Privacy Vault</h1>
            <p class="page-sub">Manage your local encryption keys and private data.</p>
        </div>
    </div>
    <div class="shield-badge">
        <Shield size={14} />
        Zero-Knowledge Active
    </div>
  </header>

  <div class="divider"></div>

  <div class="vault-grid">
    <section class="section main-sec">
        <div class="card encryption-status">
            <div class="card-hero">
                {#if keyGenerated}
                    <div class="status-icon active">
                        <CheckCircle size={48} strokeWidth={1.5} />
                    </div>
                    <h2 class="hero-title">Vault is Locked</h2>
                    <p class="hero-sub">Your data is currently encrypted with your master key.</p>
                {:else}
                    <div class="status-icon inactive">
                        <Lock size={48} strokeWidth={1.5} />
                    </div>
                    <h2 class="hero-title">Setup Required</h2>
                    <p class="hero-sub">Generate your local master key to start private syncing.</p>
                {/if}
            </div>

            {#if !keyGenerated}
                <button class="primary-btn" on:click={generateKey} disabled={keyLoading}>
                    {#if keyLoading}
                        <RefreshCw size={18} class="spinner" /> Generating...
                    {:else}
                        <Key size={18} /> Generate Master Key
                    {/if}
                </button>
            {:else}
                <div class="key-info">
                    <div class="key-field">
                        <span class="field-label">Public Key ID</span>
                        <div class="field-value">sv_92k_lx01_4k...</div>
                    </div>
                    <div class="key-field">
                        <span class="field-label">Last Updated</span>
                        <div class="field-value">Currently Active</div>
                    </div>
                </div>
            {/if}
        </div>

        {#if keyGenerated}
            <div class="card recovery-section">
                <div class="sec-header">
                    <h3 class="sec-title">Recovery Phrase</h3>
                    <p class="sec-sub">Crucial for regaining access to your vault if you lose your local key.</p>
                </div>

                <div class="phrase-container" class:blurred={!showPhrase}>
                    {#each recoveryPhrase as word, i}
                        <div class="word-box">
                            <span class="word-num">{i+1}</span>
                            <span class="word">{word}</span>
                        </div>
                    {/each}
                    <div class="blur-overlay">
                        <button class="reveal-btn" on:click={() => showPhrase = !showPhrase}>
                            {#if showPhrase}<EyeOff size={18} /> Hide Phrase{:else}<Lock size={18} /> Reveal Phrase{/if}
                        </button>
                    </div>
                </div>

                <div class="alert warn">
                    <AlertTriangle size={16} />
                    <span>StudyVault employees cannot help you recover this phrase. Keep it offline.</span>
                </div>
                <button class="ghost-btn"><Download size={16} /> Download Paper Wallet</button>
            </div>
        {/if}
    </section>

    <aside class="side-panel">
        <div class="card info-card">
            <h3 class="sec-title">Zero-Knowledge</h3>
            <p class="info-text">
                Your keys never leave your device. All data is encrypted locally before being synced to the cloud. 
                Even StudyVault servers can't "see" what you're studying.
            </p>
            <ul class="benefit-list">
                <li><Smartphone size={14} /> Local Device Storage</li>
                <li><Shield size={14} /> End-to-End Encryption</li>
                <li><EyeOff size={14} /> No Server Side Access</li>
            </ul>
        </div>

        <div class="card security-score">
            <h3 class="sec-title">Security Health</h3>
            <div class="score-viz">
                <div class="score-val">{keyGenerated ? '100%' : '20%'}</div>
                <div class="score-bar"><div class="score-fill" style="width: {keyGenerated ? 100 : 20}%"></div></div>
            </div>
            <p class="sec-sub">Protect your academic independence by maintaining high privacy standards.</p>
        </div>
    </aside>
  </div>
</div>

<style>
  .privacy-page {
    font-family: var(--font-sans);
    padding: 28px 32px 48px;
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
    opacity: 0;
    transition: all 0.5s ease;
  }

  .privacy-page.mounted { opacity: 1; transform: translateY(0); }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .title-wrap { display: flex; gap: 16px; align-items: center; }

  .icon-box {
    width: 44px;
    height: 44px;
    background: var(--accent-glow);
    color: var(--accent);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .page-title { font-size: 24px; font-weight: 700; margin: 0; color: var(--text-primary); }
  .page-sub { font-size: 14px; color: var(--text-muted); margin: 4px 0 0; }

  .shield-badge {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    padding: 6px 12px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .divider { height: 1px; background: var(--border); margin: -8px 0; }

  .vault-grid {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 24px;
  }

  .section { display: flex; flex-direction: column; gap: 24px; }

  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
  }

  .card-hero {
    text-align: center;
    padding: 40px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }

  .status-icon { color: var(--text-muted); opacity: 0.5; }
  .status-icon.active { color: var(--accent); opacity: 1; filter: drop-shadow(0 0 12px var(--accent-glow)); }

  .hero-title { font-size: 22px; font-weight: 700; color: var(--text-primary); margin: 0; }
  .hero-sub { font-size: 14px; color: var(--text-muted); margin: 0; max-width: 300px; }

  .primary-btn {
    background: var(--accent);
    color: var(--bg);
    border: none;
    padding: 14px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    transition: all 0.2s;
  }

  .primary-btn:hover { transform: scale(1.01); filter: brightness(1.1); }
  .primary-btn:disabled { opacity: 0.5; cursor: wait; }

  .key-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
  }

  .key-field .field-label { font-size: 10px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.1em; }
  .field-value { font-family: var(--font-mono); font-size: 13px; color: var(--text-primary); margin-top: 4px; }

  .sec-header { margin-bottom: 20px; }
  .sec-title { font-size: 15px; font-weight: 700; color: var(--text-primary); margin: 0; }
  .sec-sub { font-size: 12px; color: var(--text-muted); margin: 4px 0 0; }

  .phrase-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    position: relative;
    padding: 8px;
    border-radius: 12px;
  }

  .word-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    padding: 10px;
    border-radius: 8px;
    display: flex;
    gap: 10px;
  }

  .word-num { font-size: 10px; color: var(--text-muted); width: 14px; }
  .word { font-family: var(--font-mono); font-size: 13px; font-weight: 600; color: var(--text-primary); }

  .phrase-container.blurred .word-box { filter: blur(4px); opacity: 0.3; }

  .blur-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
  }

  .reveal-btn {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    pointer-events: auto;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  }

  .alert {
    display: flex;
    gap: 12px;
    padding: 12px;
    border-radius: 10px;
    font-size: 12px;
    margin: 20px 0;
  }

  .alert.warn { background: rgba(251,146,60,0.1); color: #fb923c; border: 1px solid rgba(251,146,60,0.2); }

  .ghost-btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 12px;
    border-radius: 10px;
    width: 100%;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  .side-panel { display: flex; flex-direction: column; gap: 24px; }

  .info-text { font-size: 13px; color: var(--text-muted); line-height: 1.6; margin: 12px 0 20px; }

  .benefit-list { list-style: none; display: flex; flex-direction: column; gap: 12px; }
  .benefit-list li { display: flex; align-items: center; gap: 10px; font-size: 12px; color: var(--text-primary); font-weight: 500; }

  .score-viz { margin-top: 16px; }
  .score-val { font-family: var(--font-mono); font-size: 32px; font-weight: 700; color: var(--accent); }
  .score-bar { height: 4px; background: rgba(255,255,255,0.05); border-radius: 4px; margin: 8px 0; overflow: hidden; }
  .score-fill { height: 100%; background: var(--accent); border-radius: 4px; transition: width 1s ease; }

  @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

  @media (max-width: 850px) {
    .vault-grid { grid-template-columns: 1fr; }
    .side-panel { order: -1; }
  }
</style>
