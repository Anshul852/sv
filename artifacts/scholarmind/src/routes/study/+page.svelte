<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { user } from '$lib/stores/auth';
  import { 
    BookOpen, 
    Calendar, 
    Target, 
    TrendingUp, 
    Brain, 
    Shield, 
    Settings, 
    MessageSquare, 
    ChevronLeft, 
    ChevronRight, 
    Zap,
    Clock,
    Activity,
    Save
  } from 'lucide-svelte';
  import PrivacyStatusBar from '$lib/components/dashboard/PrivacyStatusBar.svelte';

  let userProfile = null;
  let loading = true;
  let mounted = false;

  // Study Session State
  let sessionActive = false;
  let sessionInterval: any;
  let elapsedTime = 0;
  let sessionDuration = 45;
  let currentTopic = 'Data Structures';
  let sessionType = 'focused';
  let availableTopics = ['Data Structures', 'Machine Learning', 'Operating Systems', 'Database Systems'];
  let sessionHistory: any[] = [];
  
  let stats = {
    total_sessions: 0,
    focus_hours: 0,
    weekly_goal_pct: 0,
    retention_rate: 0
  };

  $: currentUser = $user;
  $: displayName = userProfile?.display_name || currentUser?.user?.email?.split('@')[0] || 'Student';
  $: greeting = new Date().getHours() < 12 ? 'Good morning' : new Date().getHours() < 18 ? 'Good afternoon' : 'Good evening';
  $: today = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });

  onMount(async () => {
    mounted = true;
    try {
      if (!currentUser) return;
      
      const [profileRes, statsRes] = await Promise.all([
        fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/students/profile`, {
          headers: { Authorization: `Bearer ${currentUser.session?.access_token}` }
        }),
        fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/students/stats`, {
          headers: { Authorization: `Bearer ${currentUser.session?.access_token}` }
        })
      ]);

      if (profileRes.ok) userProfile = await profileRes.json();
      if (statsRes.ok) stats = await statsRes.json();
      
      // Load local history if any
      const localHistory = localStorage.getItem('study_session_history');
      if (localHistory) sessionHistory = JSON.parse(localHistory);

    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      loading = false;
    }
  });

  onDestroy(() => {
    if (sessionInterval) clearInterval(sessionInterval);
  });

  function startSession() {
    sessionActive = true;
    elapsedTime = 0;
    sessionInterval = setInterval(() => {
      elapsedTime++;
      if (elapsedTime >= sessionDuration * 60) {
        completeSession();
      }
    }, 1000);
  }

  function pauseSession() {
    sessionActive = false;
    if (sessionInterval) clearInterval(sessionInterval);
  }

  function completeSession() {
    if (sessionInterval) clearInterval(sessionInterval);
    sessionActive = false;
    
    const newSession = {
      id: Date.now().toString(),
      topic: currentTopic,
      duration: Math.floor(elapsedTime / 60) || sessionDuration,
      date: new Date().toISOString(),
      retention: 85,
      type: sessionType
    };
    
    sessionHistory = [newSession, ...sessionHistory];
    localStorage.setItem('study_session_history', JSON.stringify(sessionHistory));
  }

  function formatTime(s: number) {
    const m = Math.floor(s / 60);
    const rs = s % 60;
    return `${m}:${rs.toString().padStart(2, '0')}`;
  }
</script>

<svelte:head>
  <title>Study Session - StudyVault</title>
</svelte:head>

<div class="page-container" class:mounted>
  {#if loading}
    <div class="loader">
      <div class="spinner"></div>
      <p>Loading your study vault...</p>
    </div>
  {:else}
    <div class="header-section">
      <div class="welcome">
        <h1>{greeting}, <span class="highlight">{displayName}</span></h1>
        <p class="date">{today}</p>
      </div>
      <PrivacyStatusBar />
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <Target size={20} class="icon goal" />
        <div class="stat-info">
          <span class="val">{stats.weekly_goal_pct}%</span>
          <span class="label">Weekly Goal</span>
        </div>
      </div>
      <div class="stat-card">
        <BookOpen size={20} class="icon sessions" />
        <div class="stat-info">
          <span class="val">{stats.total_sessions}</span>
          <span class="label">Completed</span>
        </div>
      </div>
      <div class="stat-card">
        <TrendingUp size={20} class="icon focus" />
        <div class="stat-info">
          <span class="val">{stats.focus_hours}h</span>
          <span class="label">Focus Time</span>
        </div>
      </div>
      <div class="stat-card">
        <Brain size={20} class="icon retention" />
        <div class="stat-info">
          <span class="val">{stats.retention_rate}%</span>
          <span class="label">Retention</span>
        </div>
      </div>
    </div>

    <div class="main-layout">
      <!-- Session Panel -->
      <section class="session-panel card">
        <div class="panel-header">
          <h2>Active Session</h2>
          {#if sessionActive}
            <span class="status pulse">LIVE</span>
          {:else}
            <span class="status">READY</span>
          {/if}
        </div>

        <div class="session-controls">
          <div class="time-display">
            <Clock size={32} />
            <span class="timer">{formatTime(elapsedTime)}</span>
            <span class="duration-target">/ {sessionDuration}m target</span>
          </div>

          <div class="topic-selector">
            <label for="topic">Current Focus</label>
            <select id="topic" bind:value={currentTopic} disabled={sessionActive}>
              {#each availableTopics as topic}
                <option value={topic}>{topic}</option>
              {/each}
            </select>
          </div>

          <div class="actions">
            {#if !sessionActive}
              <button class="btn btn-primary" on:click={startSession}>
                <Zap size={18} /> Start Session
              </button>
            {:else}
              <button class="btn btn-warning" on:click={pauseSession}>Pause</button>
              <button class="btn btn-success" on:click={completeSession}>Complete</button>
            {/if}
          </div>
        </div>
      </section>

      <!-- History & Tools -->
      <div class="side-layout">
        <section class="tools card">
          <h3>Planning Tools</h3>
          <div class="tool-list">
            <button class="tool-item">
              <Calendar size={16} /> Schedule
            </button>
            <button class="tool-item">
              <Activity size={16} /> Analytics
            </button>
            <button class="tool-item">
              <Shield size={16} /> Privacy
            </button>
          </div>
        </section>

        <section class="history card">
          <h3>Recent activity</h3>
          <div class="history-list">
            {#each sessionHistory.slice(0, 5) as session}
              <div class="history-item">
                <span class="h-topic">{session.topic}</span>
                <span class="h-meta">{session.duration}m · {new Date(session.date).toLocaleDateString()}</span>
              </div>
            {:else}
              <p class="empty">No recent sessions found.</p>
            {/each}
          </div>
        </section>
      </div>
    </div>
  {/if}
</div>

<style>
  .page-container {
    padding: 24px;
    max-width: 1200px;
    margin: 0 auto;
    opacity: 0;
    transition: opacity 0.4s ease;
  }
  .page-container.mounted { opacity: 1; }

  .loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 60vh;
    gap: 16px;
    color: var(--dim);
  }

  .header-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
  }

  h1 { font-size: 32px; font-weight: 800; letter-spacing: -0.5px; }
  .highlight { color: var(--lime); }
  .date { color: var(--dim); font-size: 14px; margin-top: 4px; }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
  }

  .stat-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .icon { padding: 10px; border-radius: 12px; }
  .icon.goal { color: var(--purple); background: rgba(192, 132, 252, 0.1); }
  .icon.sessions { color: var(--lime); background: rgba(181, 255, 77, 0.1); }
  .icon.focus { color: var(--cyan); background: rgba(0, 212, 200, 0.1); }
  .icon.retention { color: var(--orange); background: rgba(255, 149, 0, 0.1); }

  .stat-info .val { display: block; font-size: 24px; font-weight: 700; color: #fff; }
  .stat-info .label { font-size: 12px; color: var(--dim); text-transform: uppercase; letter-spacing: 0.5px; }

  .main-layout {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 24px;
  }

  .card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
  }

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
  }
  .panel-header h2 { font-size: 20px; font-weight: 700; }
  .status { font-size: 10px; font-weight: 800; border: 1px solid var(--border); padding: 4px 8px; border-radius: 6px; color: var(--dim); }
  .status.pulse { color: var(--lime); border-color: var(--lime); animation: pulse 2s infinite; }

  .time-display {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 32px;
    color: #fff;
  }
  .timer { font-size: 64px; font-weight: 800; font-family: var(--mono); }
  .duration-target { color: var(--dim); font-size: 16px; }

  .topic-selector { margin-bottom: 32px; }
  .topic-selector label { display: block; font-size: 12px; color: var(--dim); margin-bottom: 8px; text-transform: uppercase; }
  select { width: 100%; padding: 12px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 10px; color: #fff; }

  .actions { display: flex; gap: 12px; }
  .btn { 
    padding: 12px 24px; 
    border-radius: 12px; 
    font-weight: 700; 
    display: flex; 
    align-items: center; 
    gap: 8px;
    cursor: pointer;
    border: none;
    transition: transform 0.2s;
  }
  .btn:hover { transform: translateY(-2px); }
  .btn-primary { background: var(--lime); color: #000; }
  .btn-warning { background: rgba(255,149,0,0.1); color: var(--orange); border: 1px solid var(--orange); }
  .btn-success { background: rgba(181,255,77,0.1); color: var(--lime); border: 1px solid var(--lime); }

  .side-layout { display: flex; flex-direction: column; gap: 24px; }
  
  h3 { font-size: 14px; font-weight: 700; color: var(--dim); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }

  .tool-list { display: grid; gap: 10px; }
  .tool-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    padding: 12px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #fff;
    font-size: 14px;
    text-align: left;
    width: 100%;
  }

  .history-list { display: grid; gap: 12px; }
  .history-item {
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
  }
  .history-item:last-child { border: none; }
  .h-topic { display: block; font-weight: 600; color: #fff; font-size: 14px; }
  .h-meta { font-size: 12px; color: var(--dim); }
  .empty { font-size: 13px; color: var(--dim); font-style: italic; }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }

  @media (max-width: 900px) {
    .main-layout { grid-template-columns: 1fr; }
  }
</style>
