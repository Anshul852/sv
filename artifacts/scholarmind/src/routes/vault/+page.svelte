<script lang="ts">
  import { onMount } from 'svelte';
  import {
    Shield, Lock, Key, Smartphone, Trash2, Download, RefreshCw,
    CheckCircle2, Database, Eye, EyeOff, AlertTriangle, Activity
  } from 'lucide-svelte';
  import { Button } from '$lib/components/ui';

  let mounted = false;
  let loading = true;
  let showEncryptionDetails = false;
  let selectedCategory: any = null;

  // Privacy metrics
  let privacyMetrics = {
    encryptionStrength: 256,
    dataStoresEncrypted: 5,
    totalDataSize: '3.9 MB',
    lastBackup: '2 hours ago',
    devicesPaired: 2,
    encryptionAlgorithm: 'AES-256-GCM',
    keyRotationDays: 30,
    complianceScore: 98
  };

  // Data categories with detailed info
  let dataCategories = [
    { id: 'sessions', name: "Study Sessions", count: 156, size: "2.4 MB", encrypted: true, lastModified: "1 hour ago", sensitivity: "medium" },
    { id: 'deepwork', name: "Deep Work Sessions", count: 43, size: "890 KB", encrypted: true, lastModified: "3 hours ago", sensitivity: "high" },
    { id: 'events', name: "Academic Events", count: 28, size: "156 KB", encrypted: true, lastModified: "5 hours ago", sensitivity: "low" },
    { id: 'profile', name: "Profile Data", count: 1, size: "12 KB", encrypted: true, lastModified: "1 day ago", sensitivity: "high" },
    { id: 'conversations', name: "Chat Conversations", count: 89, size: "445 KB", encrypted: true, lastModified: "30 minutes ago", sensitivity: "high" }
  ];

  // Encryption status cards
  let statusCards = [
    { label: "Encryption", value: "AES-256-GCM", icon: Lock, status: "active", detail: "Military-grade encryption" },
    { label: "Key Storage", value: "Local Only", icon: Key, status: "active", detail: "Keys never leave device" },
    { label: "Devices", value: `${privacyMetrics.devicesPaired} Paired`, icon: Smartphone, status: "active", detail: "Synced securely" },
    { label: "Last Sync", value: privacyMetrics.lastBackup, icon: RefreshCw, status: "active", detail: "Automatic backup" },
  ];

  onMount(() => {
    setTimeout(() => {
      loading = false;
      mounted = true;
    }, 800);
  });

  function toggleEncryptionDetails() {
    showEncryptionDetails = !showEncryptionDetails;
  }

  function selectCategory(category: any) {
    selectedCategory = selectedCategory?.id === category.id ? null : category;
  }

  function formatBytes(bytes: number) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  function getSensitivityColor(sensitivity: string) {
    switch (sensitivity) {
      case 'high': return '#ff5555';
      case 'medium': return '#ff9500';
      case 'low': return '#b5ff4d';
      default: return '#888';
    }
  }
</script>

<svelte:head>
  <title>Privacy Vault — StudyVault</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet" />
</svelte:head>

<!-- Loading overlay -->
{#if loading}
  <div class="ld-overlay">
    <div class="ld-inner">
      <div class="ld-icon"><Shield size={26} strokeWidth={1.5} /></div>
      <p class="ld-title">INITIALIZING PRIVACY VAULT</p>
      <div class="ld-bar"><div class="ld-fill"></div></div>
      <p class="ld-sub">Verifying encryption keys…</p>
    </div>
  </div>
{/if}

<!-- Main page -->
<div class="page" class:mounted>
  <!-- Meta row -->
  <div class="meta-row">
    <span class="meta-date">PRIVACY VAULT</span>
    <div class="priv-badge">
      <span class="priv-dot"></span>
      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg>
      End-to-End Encrypted · Zero-Knowledge
    </div>
  </div>

  <!-- Greeting -->
  <header class="greet-row">
    <h1>Your <span class="name-hi">Privacy Vault</span></h1>
    <div class="hdr-actions">
      <button class="ghost-btn" on:click={toggleEncryptionDetails}><Activity size={12} /> Details</button>
      <button class="accent-btn" on:click={() => {}}><Download size={12} /> Export</button>
    </div>
  </header>

  <!-- Privacy metrics strip -->
  <div class="stat-strip">
    <div class="stat-card">
      <div class="stat-top">
        <span class="stat-lbl">ENCRYPTION STRENGTH</span>
        <span class="stat-dash">—</span>
      </div>
      <div class="stat-bar"></div>
      <div class="stat-sub lime">{privacyMetrics.encryptionStrength}-BIT</div>
    </div>
    <div class="stat-card">
      <div class="stat-top">
        <span class="stat-lbl">DATA STORES</span>
        <span class="stat-dash">—</span>
      </div>
      <div class="stat-bar"></div>
      <div class="stat-sub cyan">{privacyMetrics.dataStoresEncrypted} ENCRYPTED</div>
    </div>
    <div class="stat-card">
      <div class="stat-top">
        <span class="stat-lbl">TOTAL SIZE</span>
        <span class="stat-dash">—</span>
      </div>
      <div class="stat-bar"></div>
      <div class="stat-sub orange">{privacyMetrics.totalDataSize}</div>
    </div>
    <div class="stat-card">
      <div class="stat-top">
        <span class="stat-lbl">COMPLIANCE SCORE</span>
        <span class="stat-dash">—</span>
      </div>
      <div class="stat-bar-f" style="width:{privacyMetrics.complianceScore}%"></div>
      <div class="stat-sub purple">{privacyMetrics.complianceScore}% GDPR</div>
    </div>
  </div>

  <!-- Main layout -->
  <div class="main-layout">
    <!-- Vault Status Panel -->
    <div class="vault-status">
      <div class="status-header">
        <div class="status-icon">
          <Shield size={24} strokeWidth={1.5} />
        </div>
        <div class="status-info">
          <h2 class="status-title">Vault Status: <span class="status-secure">SECURE</span></h2>
          <p class="status-sub">All data encrypted with {privacyMetrics.encryptionAlgorithm}</p>
        </div>
        <div class="status-actions">
          <button class="icon-btn" on:click={toggleEncryptionDetails} title="Toggle details">
            {#if showEncryptionDetails}
              <EyeOff size={14} />
            {:else}
              <Eye size={14} />
            {/if}
          </button>
        </div>
      </div>

      <!-- Status Grid -->
      <div class="status-grid">
        {#each statusCards as card, index}
          <div class="status-card" style="animation-delay: {index * 0.1}s">
            <div class="card-top">
              <div class="card-icon">
                <!-- FIXED: Used <svelte:component> for dynamic icon rendering -->
                <svelte:component this={card.icon} size={16} strokeWidth={1.5} />
              </div>
              <span class="card-label">{card.label}</span>
            </div>
            <div class="card-value">
              <span class="value-text">{card.value}</span>
              <CheckCircle2 size={12} class="status-check" />
            </div>
            {#if showEncryptionDetails}
              <div class="card-detail">
                <span class="detail-text">{card.detail}</span>
              </div>
            {/if}
          </div>
        {/each}
      </div>

      <!-- Advanced Details (expandable) -->
      {#if showEncryptionDetails}
        <div class="encryption-details">
          <div class="detail-row">
            <span class="detail-key">Key Rotation</span>
            <span class="detail-val">Every {privacyMetrics.keyRotationDays} days</span>
          </div>
          <div class="detail-row">
            <span class="detail-key">Zero-Knowledge</span>
            <span class="detail-val lime">Enabled</span>
          </div>
          <div class="detail-row">
            <span class="detail-key">Backup Location</span>
            <span class="detail-val">Local + Encrypted Cloud</span>
          </div>
          <div class="detail-row">
            <span class="detail-key">Compliance</span>
            <span class="detail-val">GDPR + CCPA + SOC2</span>
          </div>
        </div>
      {/if}
    </div>

    <!-- Data Categories Panel -->
    <div class="data-panel">
      <div class="panel-header">
        <h3 class="panel-title">Encrypted Data Stores</h3>
        <div class="panel-stats">
          <span class="stat-pill">{dataCategories.length} Stores</span>
          <span class="stat-pill">{privacyMetrics.totalDataSize}</span>
        </div>
      </div>

      <div class="data-list">
        {#each dataCategories as category, index}
          <!-- FIXED: Added role and keydown for a11y compliance -->
          <div
            class="data-item"
            class:selected={selectedCategory?.id === category.id}
            role="button"
            tabindex="0"
            on:click={() => selectCategory(category)}
            on:keydown={(e) => e.key === 'Enter' && selectCategory(category)}
            style="animation-delay: {index * 0.08}s"
          >
            <div class="data-main">
              <div class="data-left">
                <div class="data-icon">
                  <Database size={16} strokeWidth={1.5} />
                </div>
                <div class="data-info">
                  <h4 class="data-name">{category.name}</h4>
                  <p class="data-meta">{category.count} records · {category.size}</p>
                </div>
              </div>
              <div class="data-right">
                <div class="sensitivity-indicator" style="color: {getSensitivityColor(category.sensitivity)}">
                  <span class="sens-dot" style="background: {getSensitivityColor(category.sensitivity)}"></span>
                  <span class="sens-label">{category.sensitivity.toUpperCase()}</span>
                </div>
                <div class="encryption-badge">
                  <Lock size={10} />
                  <span>Encrypted</span>
                </div>
              </div>
            </div>

            {#if selectedCategory?.id === category.id}
              <div class="data-details">
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Last Modified</span>
                    <span class="detail-value">{category.lastModified}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Encryption</span>
                    <span class="detail-value lime">{privacyMetrics.encryptionAlgorithm}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Access Log</span>
                    <span class="detail-value">12 accesses today</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Backup Status</span>
                    <span class="detail-value cyan">Up to date</span>
                  </div>
                </div>
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </div>

    <!-- Danger Zone -->
    <div class="danger-panel">
      <div class="danger-header">
        <AlertTriangle size={16} class="danger-icon" />
        <h3 class="danger-title">Danger Zone</h3>
      </div>
      <p class="danger-desc">
        These actions are irreversible. All encrypted blobs will be permanently removed from all devices.
      </p>
      <div class="danger-actions">
        <!-- FIXED: changed className to class -->
        <Button variant="outline" size="sm" class="danger-btn">
          <Download size={14} />
          Export All Data
        </Button>
        <Button variant="destructive" size="sm" class="danger-btn">
          <Trash2 size={14} />
          Delete All Data (GDPR)
        </Button>
      </div>
    </div>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    background: #060608;
    color: #e0e0e0;
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
  :root {
    --bg: #060608;
    --panel: #0c0c10;
    --border: rgba(255, 255, 255, 0.07);
    --lime: #b5ff4d;
    --cyan: #00d4c8;
    --orange: #ff9500;
    --purple: #c084fc;
    --red: #ff5555;
    --dim: rgba(255, 255, 255, 0.38);
    --mono: 'Space Mono', monospace;
  }

  /* Loading */
  .ld-overlay {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: #060608;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fade-out 280ms ease 780ms forwards;
  }
  .ld-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }
  .ld-icon {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    background: rgba(181, 255, 77, 0.1);
    border: 1px solid rgba(181, 255, 77, 0.2);
    color: var(--lime);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: icon-pulse 1.4s ease-in-out infinite;
  }
  .ld-title {
    font-family: var(--mono);
    font-size: 9px;
    letter-spacing: 0.18em;
    color: var(--dim);
    margin: 0;
  }
  .ld-sub {
    font-family: var(--mono);
    font-size: 8px;
    color: rgba(255, 255, 255, 0.18);
    margin: 0;
  }
  .ld-bar {
    width: 130px;
    height: 2px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 2px;
    overflow: hidden;
  }
  .ld-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--lime), var(--cyan));
    animation: bar-fill 900ms ease forwards;
  }

  /* Page */
  .page {
    max-width: 1440px;
    margin: 0 auto;
    padding: 18px 26px 40px;
    opacity: 0;
    transform: translateY(5px);
    transition: opacity 300ms ease, transform 300ms ease;
  }
  .page.mounted {
    opacity: 1;
    transform: none;
  }

  /* Meta */
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
    color: var(--lime);
  }
  .priv-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--lime);
    animation: pulse 2s ease-in-out infinite;
  }

  /* Greeting */
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
  .name-hi {
    color: var(--lime);
  }
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
    background: var(--lime);
    border: none;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 700;
    color: #000;
    transition: filter 0.15s;
  }
  .accent-btn:hover {
    filter: brightness(1.08);
  }

  /* Stat strip */
  .stat-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 18px;
  }
  .stat-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px 11px;
  }
  .stat-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  .stat-lbl {
    font-family: var(--mono);
    font-size: 9px;
    letter-spacing: 0.1em;
    color: var(--dim);
  }
  .stat-dash {
    color: var(--dim);
    font-size: 12px;
  }
  .stat-bar {
    height: 3px;
    width: 50%;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 3px;
    margin-bottom: 9px;
  }
  .stat-bar-f {
    height: 3px;
    background: var(--purple);
    border-radius: 3px;
    margin-bottom: 9px;
    transition: width 0.6s ease;
  }
  .stat-sub {
    font-family: var(--mono);
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.1em;
  }
  .stat-sub.lime { color: var(--lime); }
  .stat-sub.cyan { color: var(--cyan); }
  .stat-sub.orange { color: var(--orange); }
  .stat-sub.purple { color: var(--purple); }

  /* Main layout */
  .main-layout {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .icon-btn {
    background: none;
    border: none;
    color: var(--dim);
    padding: 5px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.15s, background 0.15s;
  }
  .icon-btn:hover {
    color: #fff;
    background: rgba(255, 255, 255, 0.06);
  }

  /* Vault Status Panel */
  .vault-status {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 16px;
  }
  .status-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }
  .status-icon {
    width: 48px;
    height: 48px;
    border-radius: 11px;
    background: rgba(181, 255, 77, 0.1);
    border: 1px solid rgba(181, 255, 77, 0.2);
    color: var(--lime);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .status-info {
    flex: 1;
  }
  .status-title {
    font-size: 18px;
    font-weight: 700;
    color: #fff;
    margin: 0 0 4px;
  }
  .status-secure {
    color: var(--lime);
  }
  .status-sub {
    font-size: 12px;
    color: var(--dim);
    margin: 0;
  }
  .status-actions {
    display: flex;
    gap: 6px;
  }

  /* Status Grid */
  .status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    margin-bottom: 16px;
  }
  .status-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    transition: all 0.2s;
    animation: fadeInUp 300ms ease-out both;
  }
  .status-card:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.12);
  }
  .card-top {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
  }
  .card-icon {
    color: var(--dim);
    flex-shrink: 0;
  }
  .card-label {
    font-size: 10px;
    color: var(--dim);
    font-family: var(--mono);
    letter-spacing: 0.1em;
  }
  .card-value {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .value-text {
    font-size: 14px;
    font-weight: 600;
    color: #fff;
  }
  .status-check {
    color: var(--lime);
    flex-shrink: 0;
  }
  .card-detail {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--border);
  }
  .detail-text {
    font-size: 10px;
    color: var(--dim);
    font-family: var(--mono);
  }

  /* Encryption Details */
  .encryption-details {
    background: rgba(181, 255, 77, 0.03);
    border: 1px solid rgba(181, 255, 77, 0.1);
    border-radius: 8px;
    padding: 12px;
    margin-top: 12px;
  }
  .detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
    font-size: 11px;
  }
  .detail-key {
    color: var(--dim);
    font-family: var(--mono);
  }
  .detail-val {
    color: rgba(255, 255, 255, 0.8);
    font-weight: 500;
  }
  .detail-val.lime { color: var(--lime); }
  .detail-val.cyan { color: var(--cyan); }

  /* Data Panel */
  .data-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 16px;
  }
  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
  }
  .panel-title {
    font-size: 14px;
    font-weight: 700;
    color: #fff;
    margin: 0;
  }
  .panel-stats {
    display: flex;
    gap: 8px;
  }
  .stat-pill {
    font-family: var(--mono);
    font-size: 8px;
    padding: 3px 8px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid var(--border);
    border-radius: 12px;
    color: var(--dim);
  }

  /* Data List */
  .data-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .data-item {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    cursor: pointer;
    transition: all 0.2s;
    animation: fadeInUp 300ms ease-out both;
  }
  .data-item:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.12);
  }
  .data-item.selected {
    background: rgba(181, 255, 77, 0.05);
    border-color: rgba(181, 255, 77, 0.2);
  }
  .data-main {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .data-left {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .data-icon {
    width: 32px;
    height: 32px;
    border-radius: 7px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--border);
    color: var(--dim);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .data-info {
    min-width: 0;
  }
  .data-name {
    font-size: 13px;
    font-weight: 600;
    color: #fff;
    margin: 0 0 2px;
  }
  .data-meta {
    font-size: 10px;
    color: var(--dim);
    font-family: var(--mono);
    margin: 0;
  }
  .data-right {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .sensitivity-indicator {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 9px;
    font-family: var(--mono);
    font-weight: 600;
  }
  .sens-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
  }
  .encryption-badge {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 9px;
    color: var(--lime);
    font-family: var(--mono);
  }

  /* Data Details */
  .data-details {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border);
  }
  .detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
  }
  .detail-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .detail-label {
    font-size: 9px;
    color: var(--dim);
    font-family: var(--mono);
  }
  .detail-value {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.8);
    font-weight: 500;
  }
  .detail-value.lime { color: var(--lime); }
  .detail-value.cyan { color: var(--cyan); }

  /* Danger Panel */
  .danger-panel {
    background: var(--panel);
    border: 1px solid rgba(255, 85, 85, 0.2);
    border-radius: 13px;
    padding: 16px;
  }
  .danger-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }
  .danger-icon {
    color: var(--red);
    flex-shrink: 0;
  }
  .danger-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--red);
    margin: 0;
  }
  .danger-desc {
    font-size: 11px;
    color: var(--dim);
    margin-bottom: 16px;
    line-height: 1.5;
  }
  .danger-actions {
    display: flex;
    gap: 10px;
  }
  .danger-btn {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  /* Keyframes */
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  @keyframes icon-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.07); }
  }
  @keyframes bar-fill {
    from { width: 0; }
    to { width: 100%; }
  }
  @keyframes fade-out {
    to {
      opacity: 0;
      pointer-events: none;
    }
  }

  /* Responsive */
  @media (max-width: 768px) {
    .page { padding: 10px 12px 22px; }
    .stat-strip { grid-template-columns: 1fr 1fr; }
    .status-grid { grid-template-columns: 1fr; }
    .data-main { flex-direction: column; align-items: flex-start; gap: 8px; }
    .data-right { align-self: flex-end; }
    .danger-actions { flex-direction: column; }
  }
</style>