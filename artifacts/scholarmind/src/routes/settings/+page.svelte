<script lang="ts">
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/auth';
  import { usageStore } from '$lib/stores/usageStore';
  
  let activeTab = 'profile';
  let userProfile: any = null;
  let usageData: any = null;
  let processingStyle = 'linear';
  
  $: currentUser = $user;
  $: userEmail = currentUser ? (currentUser as any)?.user?.email ?? '' : '';
  $: authToken = currentUser ? (currentUser as any)?.session?.access_token ?? '' : '';
  
  import { User, Lock, BarChart3, Brain } from 'lucide-svelte';
  
  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'privacy', label: 'Privacy', icon: Lock },
    { id: 'usage', label: 'Usage', icon: BarChart3 },
    { id: 'processing', label: 'Processing Style', icon: Brain }
  ];
  
  onMount(async () => {
    if (currentUser) {
      try {
        // Fetch user profile
        const profileResponse = await fetch(
          `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/api/students/profile`,
          {
            headers: {
              Authorization: `Bearer ${authToken}`
            }
          }
        );
        
        if (profileResponse.ok) {
          userProfile = await profileResponse.json();
          processingStyle = userProfile.processing_style || 'linear';
        }
        
        // Fetch usage data
        const usageResponse = await fetch(
          `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/api/students/usage`,
          {
            headers: {
              Authorization: `Bearer ${authToken}`
            }
          }
        );
        
        if (usageResponse.ok) {
          usageData = await usageResponse.json();
        }
      } catch (error) {
        console.error('Failed to fetch settings data:', error);
      }
    }
  });
  
  async function updateProcessingStyle(style: string) {
    processingStyle = style;
    
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/api/students/processing-style`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${authToken}`
          },
          body: JSON.stringify({ processing_style: style })
        }
      );
      
      if (response.ok) {
        // Update local profile
        if (userProfile) {
          userProfile.processing_style = style;
        }
      }
    } catch (error) {
      console.error('Failed to update processing style:', error);
    }
  }
  
  async function deleteAccount() {
    if (!currentUser || !confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      return;
    }
    
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/api/students/account`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${authToken}`
          }
        }
      );
      
      if (response.ok) {
        // Log out and redirect to home
        await fetch('/api/auth/logout', { method: 'POST' });
        window.location.href = '/';
      }
    } catch (error) {
      console.error('Failed to delete account:', error);
      alert('Failed to delete account. Please try again.');
    }
  }
  
  function exportData() {
    // Export user data (simplified version)
    const exportData = {
      profile: userProfile,
      usage: usageData,
      exportDate: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'studyvault-data-export.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
</script>

<div class="settings-page">
  <div class="settings-container">
    <!-- Header -->
    <div class="settings-header">
      <h1 class="page-title">Settings</h1>
      <p class="page-subtitle">Manage your StudyVault experience</p>
    </div>
    
    <!-- Tab Navigation -->
    <div class="tab-navigation">
      {#each tabs as tab}
        <button 
          class="tab-button" 
          class:active={activeTab === tab.id}
          on:click={() => activeTab = tab.id}
        >
          <svelte:component this={tab.icon} class="tab-icon" size={18} />
          <span class="tab-label">{tab.label}</span>
        </button>
      {/each}
    </div>
    
    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Profile Tab -->
      {#if activeTab === 'profile'}
        <div class="tab-panel">
          <h2 class="panel-title">Profile Information</h2>
          
          {#if userProfile}
            <div class="profile-info">
              <div class="info-group">
                <label class="info-label">Name</label>
                <span class="info-value">{userProfile.display_name || 'Not set'}</span>
              </div>
              
              <div class="info-group">
                <label class="info-label">Email</label>
                <span class="info-value">{userEmail}</span>
              </div>
              
              <div class="info-group">
                <label class="info-label">Subject</label>
                <span class="info-value">{userProfile.subject || 'Not set'}</span>
              </div>
              
              <div class="info-group">
                <label class="info-label">Learning Style</label>
                <span class="info-value">{userProfile.learning_style || 'Not detected'}</span>
              </div>
              
              <div class="info-group">
                <label class="info-label">Member Since</label>
                <span class="info-value">
                  {userProfile.created_at ? new Date(userProfile.created_at).toLocaleDateString() : 'Unknown'}
                </span>
              </div>
            </div>
          {:else}
            <div class="loading-state">
              <p>Loading profile information...</p>
            </div>
          {/if}
        </div>
      {/if}
      
      <!-- Privacy Tab -->
      {#if activeTab === 'privacy'}
        <div class="tab-panel">
          <h2 class="panel-title">Privacy & Data</h2>
          
          <div class="privacy-sections">
            <div class="privacy-section">
              <h3 class="section-title">Data Collection</h3>
              <div class="privacy-item">
                <span class="item-label">Chat Messages</span>
                <span class="item-value">Not stored in database</span>
              </div>
              <div class="privacy-item">
                <span class="item-label">Study Sessions</span>
                <span class="item-value">Stored locally only</span>
              </div>
              <div class="privacy-item">
                <span class="item-label">Usage Analytics</span>
                <span class="item-value">Memory only, not shared</span>
              </div>
            </div>
            
            <div class="privacy-section">
              <h3 class="section-title">Data Control</h3>
              <div class="privacy-item">
                <span class="item-label">Export Data</span>
                <button class="action-button" on:click={exportData}>
                  Download My Data
                </button>
              </div>
              <div class="privacy-item">
                <span class="item-label">Delete Account</span>
                <button class="action-button danger" on:click={deleteAccount}>
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      {/if}
      
      <!-- Usage Tab -->
      {#if activeTab === 'usage'}
        <div class="tab-panel">
          <h2 class="panel-title">Usage Statistics</h2>
          
          {#if usageData}
            <div class="usage-stats">
              <div class="usage-card">
                <h3 class="card-title">Today's Usage</h3>
                <div class="stat-item">
                  <span class="stat-label">Chat Minutes</span>
                  <span class="stat-value">{usageData.dailyChatMinutes || 0} min</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">App Opens</span>
                  <span class="stat-value">{usageData.dailyAppOpens || 0}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Plan Revisions</span>
                  <span class="stat-value">{usageData.dailyPlanRevisions || 0}</span>
                </div>
              </div>
              
              <div class="usage-card">
                <h3 class="card-title">This Week</h3>
                <div class="stat-item">
                  <span class="stat-label">Total Sessions</span>
                  <span class="stat-value">{usageData.weeklySessions || 0}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Study Hours</span>
                  <span class="stat-value">{usageData.weeklyStudyHours || 0}h</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Average Session</span>
                  <span class="stat-value">{usageData.averageSessionLength || 0}min</span>
                </div>
              </div>
            </div>
          {:else}
            <div class="loading-state">
              <p>Loading usage data...</p>
            </div>
          {/if}
        </div>
      {/if}
      
      <!-- Processing Style Tab -->
      {#if activeTab === 'processing'}
        <div class="tab-panel">
          <h2 class="panel-title">Processing Style</h2>
          <p class="panel-description">
            Choose how you prefer to receive and process information. This affects how content is presented to you.
          </p>
          
          <div class="processing-options">
            <div class="option-card" class:selected={processingStyle === 'linear'}>
              <div class="option-header">
                <h3 class="option-title">Linear</h3>
                <p class="option-description">
                  Step-by-step, sequential learning. Complete one concept before moving to the next.
                </p>
              </div>
              <button 
                class="select-button"
                on:click={() => updateProcessingStyle('linear')}
              >
                {processingStyle === 'linear' ? 'Selected' : 'Select Linear'}
              </button>
            </div>
            
            <div class="option-card" class:selected={processingStyle === 'relational'}>
              <div class="option-header">
                <h3 class="option-title">Relational</h3>
                <p class="option-description">
                  Connect new concepts to what you already know. Uses analogies and comparisons.
                </p>
              </div>
              <button 
                class="select-button"
                on:click={() => updateProcessingStyle('relational')}
              >
                {processingStyle === 'relational' ? 'Selected' : 'Select Relational'}
              </button>
            </div>
            
            <div class="option-card" class:selected={processingStyle === 'systemic'}>
              <div class="option-header">
                <h3 class="option-title">Systemic</h3>
                <p class="option-description">
                  Big picture first, then details. Shows how concepts fit into the overall system.
                </p>
              </div>
              <button 
                class="select-button"
                on:click={() => updateProcessingStyle('systemic')}
              >
                {processingStyle === 'systemic' ? 'Selected' : 'Select Systemic'}
              </button>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  .settings-page {
    min-height: 100vh;
    background: var(--bg);
    color: var(--text-primary);
    font-family: var(--font-sans);
    padding: 40px 20px;
  }
  
  .settings-container {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .settings-header {
    text-align: center;
    margin-bottom: 40px;
  }
  
  .page-title {
    font-size: 32px;
    font-weight: 700;
    margin: 0 0 12px 0;
    color: var(--text-primary);
  }
  
  .page-subtitle {
    font-size: 16px;
    color: var(--text-muted);
    margin: 0;
    line-height: 1.5;
  }
  
  .tab-navigation {
    display: flex;
    gap: 8px;
    margin-bottom: 32px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0;
  }
  
  .tab-button {
    background: transparent;
    border: none;
    padding: 16px 24px;
    border-radius: var(--radius-input) var(--radius-input) 0 0;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-muted);
    border-bottom: 2px solid transparent;
  }
  
  .tab-button:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.05);
  }
  
  .tab-button.active {
    color: var(--accent);
    border-bottom-color: var(--accent);
  }
  
  .tab-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
  }
  
  .tab-label {
    font-weight: 600;
  }
  
  .tab-content {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 32px;
    min-height: 400px;
  }
  
  .tab-panel {
    animation: fadeIn 0.3s ease;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  .panel-title {
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 24px 0;
    color: var(--text-primary);
  }
  
  .panel-description {
    font-size: 16px;
    color: var(--text-muted);
    margin: 0 0 32px 0;
    line-height: 1.5;
  }
  
  .profile-info {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .info-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-input);
  }
  
  .info-label {
    font-weight: 600;
    color: var(--text-muted);
  }
  
  .info-value {
    color: var(--text-primary);
    font-weight: 500;
  }
  
  .privacy-sections {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 32px;
  }
  
  .privacy-section {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-input);
    padding: 24px;
  }
  
  .section-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 16px 0;
    color: var(--text-primary);
  }
  
  .privacy-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
  }
  
  .privacy-item:last-child {
    border-bottom: none;
  }
  
  .action-button {
    background: var(--accent);
    color: #000;
    border: none;
    padding: 8px 16px;
    border-radius: var(--radius-input);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .action-button:hover {
    filter: brightness(1.1);
  }
  
  .action-button.danger {
    background: #ef4444;
    color: white;
  }
  
  .usage-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
  }
  
  .usage-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-input);
    padding: 24px;
  }
  
  .card-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 16px 0;
    color: var(--text-primary);
  }
  
  .stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
  }
  
  .stat-item:last-child {
    border-bottom: none;
  }
  
  .stat-label {
    color: var(--text-muted);
    font-size: 14px;
  }
  
  .stat-value {
    color: var(--text-primary);
    font-weight: 600;
  }
  
  .processing-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
  }
  
  .option-card {
    background: var(--bg);
    border: 2px solid var(--border);
    border-radius: var(--radius-input);
    padding: 24px;
    transition: all 0.2s ease;
  }
  
  .option-card.selected {
    border-color: var(--accent);
  }
  
  .option-header {
    margin-bottom: 16px;
  }
  
  .option-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: var(--text-primary);
  }
  
  .option-description {
    font-size: 14px;
    color: var(--text-muted);
    line-height: 1.4;
    margin: 0;
  }
  
  .select-button {
    width: 100%;
    background: transparent;
    color: var(--text-muted);
    border: 1px solid var(--border);
    padding: 12px;
    border-radius: var(--radius-input);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .select-button:hover {
    border-color: var(--accent);
    color: var(--text-primary);
  }
  
  .loading-state {
    text-align: center;
    padding: 40px;
    color: var(--text-muted);
  }
  
  @media (max-width: 768px) {
    .settings-page {
      padding: 20px 16px;
    }
    
    .tab-navigation {
      flex-wrap: wrap;
    }
    
    .privacy-sections,
    .usage-stats,
    .processing-options {
      grid-template-columns: 1fr;
    }
  }
</style>
