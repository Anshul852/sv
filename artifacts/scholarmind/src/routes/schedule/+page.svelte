<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { user, session } from '$lib/stores/auth';
  import { Calendar, Clock, Plus, BookOpen, Brain, RotateCcw, Zap, ChevronLeft, ChevronRight, Activity, CalendarCheck, TrendingUp, Target, Gauge, Map, Sparkles, BarChart3, CheckCircle2, Circle, AlertCircle } from 'lucide-svelte';
  import MiniCalendar from '$lib/components/schedule/MiniCalendar.svelte';
  import StudyHeatmap from '$lib/components/schedule/StudyHeatmap.svelte';
  import CalendarSync from '$lib/components/schedule/CalendarSync.svelte';

  // ── Types ──────────────────────────────────────────────
  interface ScheduleItem {
    id: string;
    time: string;
    subject: string;
    type: 'study' | 'deep-work' | 'review' | 'practice';
    duration: string;
    durationMinutes: number;
    status: 'completed' | 'in-progress' | 'upcoming';
    difficulty?: 'easy' | 'medium' | 'hard';
  }

  interface RoadmapWeek {
    week: number;
    label: string;
    sessions: { day: string; subject: string; duration: string; type: string }[];
    completionTarget: number;
  }

  interface Prediction {
    subject: string;
    currentProgress: number;
    predictedCompletion: string;
    daysLeft: number;
    status: 'on-track' | 'at-risk' | 'ahead';
    color: string;
  }

  // ── Config ─────────────────────────────────────────────
  const typeConfig: Record<string, { accent: string; glow: string; label: string; icon: any }> = {
    study:       { accent: '#a3e635', glow: 'rgba(163,230,53,0.15)',  label: 'Study',     icon: BookOpen  },
    'deep-work': { accent: '#38bdf8', glow: 'rgba(56,189,248,0.15)',  label: 'Deep Work', icon: Brain     },
    review:      { accent: '#f59e0b', glow: 'rgba(245,158,11,0.15)',  label: 'Review',    icon: RotateCcw },
    practice:    { accent: '#e879f9', glow: 'rgba(232,121,249,0.15)', label: 'Practice',  icon: Zap       },
  };

  const difficultyConfig: Record<string, { color: string; bg: string }> = {
    easy:   { color: '#34d399', bg: 'rgba(52,211,153,0.08)'  },
    medium: { color: '#f59e0b', bg: 'rgba(245,158,11,0.08)'  },
    hard:   { color: '#f87171', bg: 'rgba(248,113,113,0.08)' },
  };

  const velocityConfig = {
    slow:   { label: 'Slow',   color: '#f59e0b', bg: 'rgba(245,158,11,0.12)',   sessionsPerDay: 2, sessionLen: 45,  breakLen: 20, description: '2 sessions/day · 45 min each · long breaks' },
    medium: { label: 'Medium', color: '#38bdf8', bg: 'rgba(56,189,248,0.12)',   sessionsPerDay: 3, sessionLen: 60,  breakLen: 15, description: '3 sessions/day · 60 min each · standard breaks' },
    fast:   { label: 'Fast',   color: '#a3e635', bg: 'rgba(163,230,53,0.12)',   sessionsPerDay: 5, sessionLen: 90,  breakLen: 10, description: '5 sessions/day · 90 min each · short breaks' },
  };

  // ── State ──────────────────────────────────────────────
  let schedule: ScheduleItem[] = [];
  let loading = true;
  let error = false;
  let mounted = false;
  let selectedDay = 'today';
  let pollInterval: ReturnType<typeof setInterval>;

  let velocity: 'slow' | 'medium' | 'fast' = 'medium';
  let roadmapGenerated = false;
  let roadmapLoading = false;
  let roadmap: RoadmapWeek[] = [];
  let predictions: Prediction[] = [];
  let activeTab: 'schedule' | 'roadmap' | 'prediction' = 'schedule';

  $: stats = {
    total:     schedule.length,
    hours:     schedule.reduce((s, i) => s + i.durationMinutes, 0) / 60,
    completed: schedule.filter(i => i.status === 'completed').length,
    upcoming:  schedule.filter(i => i.status === 'upcoming').length,
  };

  $: now = new Date();

  $: dateLabel = (() => {
    const d = new Date();
    if (selectedDay === 'yesterday') d.setDate(d.getDate() - 1);
    if (selectedDay === 'tomorrow')  d.setDate(d.getDate() + 1);
    return d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
  })();

  $: vc = velocityConfig[velocity];

  // ── Helpers ────────────────────────────────────────────
  function cfg(type: string) { return typeConfig[type] ?? typeConfig.study; }

  function parseTime(t: string): Date {
    try {
      const today = new Date();
      const [time, period] = t.split(' ');
      let [h, m] = time.split(':').map(Number);
      if (period === 'PM' && h !== 12) h += 12;
      if (period === 'AM' && h === 12) h = 0;
      return new Date(today.getFullYear(), today.getMonth(), today.getDate(), h, m ?? 0);
    } catch { return new Date(); }
  }

  function isActive(item: ScheduleItem, i: number): boolean {
    if (selectedDay !== 'today') return false;
    const start = parseTime(item.time);
    const next  = schedule[i + 1];
    const end   = next ? parseTime(next.time) : new Date(start.getTime() + item.durationMinutes * 60000);
    return now >= start && now < end;
  }

  function isPast(item: ScheduleItem): boolean {
    if (selectedDay !== 'today') return selectedDay === 'yesterday';
    return now > parseTime(item.time);
  }

  // ── Roadmap Generator ──────────────────────────────────
  function generateRoadmap() {
    roadmapLoading = true;
    const subjects = ['Data Structures', 'Machine Learning', 'Algorithms', 'Database Systems', 'Computer Networks'];
    const types    = ['study', 'deep-work', 'review', 'practice'];
    const days     = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const vc       = velocityConfig[velocity];

    setTimeout(() => {
      roadmap = Array.from({ length: 4 }, (_, wi) => ({
        week: wi + 1,
        label: `Week ${wi + 1} — ${['Foundation', 'Deep Dive', 'Practice', 'Mastery'][wi]}`,
        sessions: days.slice(0, velocity === 'slow' ? 5 : velocity === 'medium' ? 6 : 7).map((day, di) => ({
          day,
          subject: subjects[(di + wi) % subjects.length],
          duration: `${vc.sessionLen}m`,
          type: types[(di + wi) % types.length],
        })),
        completionTarget: Math.round(((wi + 1) / 4) * 100),
      }));

      // Generate predictions
      const progressBase = velocity === 'slow' ? 0.6 : velocity === 'medium' ? 1.0 : 1.5;
      predictions = subjects.map((sub, i) => {
        const progress  = Math.min(95, Math.round((i * 17 + 20) * progressBase));
        const remaining = 100 - progress;
        const daysLeft  = Math.ceil(remaining / (vc.sessionsPerDay * progressBase * 3));
        const target    = new Date();
        target.setDate(target.getDate() + daysLeft);
        const status = daysLeft < 7 ? 'ahead' : daysLeft < 21 ? 'on-track' : 'at-risk';
        return {
          subject: sub,
          currentProgress: progress,
          predictedCompletion: target.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          daysLeft,
          status,
          color: status === 'ahead' ? '#a3e635' : status === 'on-track' ? '#38bdf8' : '#f87171',
        };
      });

      roadmapGenerated = true;
      roadmapLoading   = false;
      activeTab        = 'roadmap';
    }, 1400);
  }

  // ── Data ───────────────────────────────────────────────
  function mapItems(raw: any[]): ScheduleItem[] {
    return raw.map(s => ({
      id:              s.id ?? Math.random().toString(36).slice(2),
      time:            s.time ?? s.start_time ?? s.scheduled_time ?? '9:00 AM',
      subject:         s.subject ?? s.topic ?? s.title ?? 'Study Session',
      type:            s.type ?? s.session_type ?? 'study',
      duration:        s.duration ?? '1h',
      durationMinutes: s.duration_minutes ?? 60,
      status:          s.status ?? 'upcoming',
      difficulty:      s.difficulty ?? 'medium',
    }));
  }

  function useFallback() {
    schedule = mapItems([
      { id:'1', time:'9:00 AM',  subject:'Data Structures',  type:'study',     duration:'1h 30m', durationMinutes:90,  status:'completed',   difficulty:'medium' },
      { id:'2', time:'11:00 AM', subject:'Machine Learning',  type:'deep-work', duration:'2h',     durationMinutes:120, status:'in-progress', difficulty:'hard'   },
      { id:'3', time:'2:00 PM',  subject:'Deep Work',         type:'deep-work', duration:'1h',     durationMinutes:60,  status:'upcoming',    difficulty:'hard'   },
      { id:'4', time:'4:00 PM',  subject:'Review Session',    type:'review',    duration:'45m',    durationMinutes:45,  status:'upcoming',    difficulty:'easy'   },
    ]);
  }

  async function fetchSchedule() {
    const currentSession = $session;
    if (!currentSession?.access_token) { useFallback(); loading = false; return; }
    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL || '/api'}/students/schedule`,
        { headers: { Authorization: `Bearer ${currentSession.access_token}` } }
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const raw  = Array.isArray(data) ? data : data.schedule ?? [];
      if (raw.length) schedule = mapItems(raw);
      else useFallback();
      error = false;
    } catch (e) {
      error = true;
      useFallback();
    } finally {
      loading = false;
    }
  }

  onMount(async () => {
    await fetchSchedule();
    mounted = true;
    pollInterval = setInterval(fetchSchedule, 60_000);
  });

  onDestroy(() => clearInterval(pollInterval));
</script>

<svelte:head><title>Schedule — StudyVault</title></svelte:head>

<div class="page" class:mounted>

  <!-- ── Header ── -->
  <header class="page-header">
    <div class="header-left">
      <div class="header-icon-wrap"><Calendar size={14} strokeWidth={2} /></div>
      <div>
        <h1 class="page-title">Schedule</h1>
        <p class="page-sub">{dateLabel}</p>
      </div>
    </div>
    <button class="add-btn" on:click={() => goto('/study')}>
      <Plus size={14} strokeWidth={2.5} /> Add Session
    </button>
  </header>

  <div class="divider" />

  <!-- ── Velocity Selector ── -->
  <div class="velocity-card">
    <div class="velocity-header">
      <div class="velocity-title-row">
        <div class="velocity-icon"><Gauge size={14} /></div>
        <div>
          <p class="velocity-title">Learner Velocity</p>
          <p class="velocity-sub">Adjusts session length, frequency, and roadmap intensity</p>
        </div>
      </div>
      <div class="velocity-tabs">
        {#each (['slow','medium','fast'] as const) as v}
          <button
            class="velocity-tab"
            class:active={velocity === v}
            style={velocity === v ? `background:${velocityConfig[v].bg}; color:${velocityConfig[v].color}; border-color:${velocityConfig[v].color}40` : ''}
            on:click={() => { velocity = v; roadmapGenerated = false; }}
          >
            {#if v === 'slow'}🐢{:else if v === 'medium'}⚡{:else}🚀{/if}
            {velocityConfig[v].label}
          </button>
        {/each}
      </div>
    </div>
    <div class="velocity-details">
      <span class="velocity-desc">{vc.description}</span>
      <div class="velocity-badges">
        <span class="vbadge" style="color:{vc.color}; background:{vc.bg}">{vc.sessionsPerDay} sessions/day</span>
        <span class="vbadge" style="color:{vc.color}; background:{vc.bg}">{vc.sessionLen}m sessions</span>
        <span class="vbadge" style="color:{vc.color}; background:{vc.bg}">{vc.breakLen}m breaks</span>
      </div>
    </div>
    <button
      class="generate-btn"
      class:loading={roadmapLoading}
      on:click={generateRoadmap}
      disabled={roadmapLoading}
    >
      {#if roadmapLoading}
        <div class="spinner"></div> Generating Roadmap…
      {:else}
        <Map size={14} />
        {roadmapGenerated ? 'Regenerate Roadmap' : 'Generate Learning Roadmap'}
      {/if}
    </button>
  </div>

  <!-- ── Tabs ── -->
  {#if roadmapGenerated}
    <div class="tabs-bar">
      {#each [
        { key: 'schedule',   label: 'Today\'s Schedule', icon: Calendar },
        { key: 'roadmap',    label: 'Roadmap',           icon: Map },
        { key: 'prediction', label: 'Prediction Engine', icon: TrendingUp },
      ] as tab}
        <button
          class="tab-btn"
          class:active={activeTab === tab.key}
          on:click={() => activeTab = tab.key}
        >
          <svelte:component this={tab.icon} size={13} />
          {tab.label}
        </button>
      {/each}
    </div>
  {/if}

  <!-- ── Main Grid ── -->
  <div class="schedule-grid">
    <div class="main-content">

      <!-- ── SCHEDULE TAB ── -->
      {#if activeTab === 'schedule'}
        <!-- Heatmap -->
        <section class="section-card"><StudyHeatmap /></section>

        <!-- Stats -->
        <div class="stats-row">
          {#each [
            { label: 'Sessions', sub: "Today's total",  value: loading ? '—' : String(stats.total),           accent: '#a3e635', glow: 'rgba(163,230,53,0.15)',  bar: stats.total / 6       },
            { label: 'Hours',    sub: 'Study time',      value: loading ? '—' : stats.hours.toFixed(1) + 'h', accent: '#38bdf8', glow: 'rgba(56,189,248,0.15)',  bar: stats.hours / 8       },
            { label: 'Done',     sub: 'Completed',       value: loading ? '—' : String(stats.completed),      accent: '#f59e0b', glow: 'rgba(245,158,11,0.15)',  bar: stats.total ? stats.completed / stats.total : 0 },
            { label: 'Left',     sub: 'Remaining',       value: loading ? '—' : String(stats.upcoming),       accent: '#e879f9', glow: 'rgba(232,121,249,0.15)', bar: stats.total ? stats.upcoming / stats.total : 0  },
          ] as s, i}
            <div class="stat-card" style="--accent:{s.accent}; --glow:{s.glow}; animation-delay:{i*70}ms">
              <div class="stat-top"><span class="stat-sub">{s.sub}</span></div>
              <div class="stat-value">{s.value}</div>
              <div class="stat-label">{s.label}</div>
              <div class="stat-bar"><div class="stat-bar-fill" style="width:{(mounted && s.bar) ? Math.min(s.bar*100,100) : 0}%"></div></div>
            </div>
          {/each}
        </div>

        <!-- Day tabs -->
        <div class="section-header">
          <div class="day-tabs">
            <button class="nav-arrow" on:click={() => selectedDay = selectedDay === 'today' ? 'yesterday' : selectedDay === 'tomorrow' ? 'today' : 'yesterday'}>
              <ChevronLeft size={14} />
            </button>
            {#each [{key:'yesterday',label:'Yesterday'},{key:'today',label:'Today'},{key:'tomorrow',label:'Tomorrow'}] as d}
              <button class="day-tab" class:active={selectedDay === d.key} on:click={() => selectedDay = d.key}>{d.label}</button>
            {/each}
            <button class="nav-arrow" on:click={() => selectedDay = selectedDay === 'today' ? 'tomorrow' : selectedDay === 'yesterday' ? 'today' : 'tomorrow'}>
              <ChevronRight size={14} />
            </button>
          </div>
          <span class="session-count">{schedule.length} sessions</span>
        </div>

        <!-- Timeline -->
        <div class="timeline">
          {#if loading}
            {#each [1,2,3,4] as _, i}
              <div class="timeline-item skeleton" style="animation-delay:{i*60}ms">
                <div class="skel skel-time"></div>
                <div class="skel skel-dot"></div>
                <div class="skel-body"><div class="skel skel-title"></div><div class="skel skel-meta"></div></div>
                <div class="skel skel-btn"></div>
              </div>
            {/each}
          {:else if schedule.length === 0}
            <div class="empty-state">
              <div class="empty-icon"><Calendar size={24} /></div>
              <p class="empty-title">No sessions scheduled</p>
              <p class="empty-sub">Your schedule is clear. Time to plan!</p>
              <button class="empty-cta" on:click={() => goto('/study')}>Plan a Session</button>
            </div>
          {:else}
            {#each schedule as item, i}
              {@const c      = cfg(item.type)}
              {@const active = isActive(item, i)}
              {@const past   = isPast(item) && !active}
              {@const diff   = difficultyConfig[item.difficulty ?? 'medium'] ?? difficultyConfig.medium}
              <div class="timeline-item" class:active class:past style="--accent:{c.accent}; --glow:{c.glow}; animation-delay:{i*70}ms">
                <div class="item-time">
                  <span class="time-str">{item.time}</span>
                  {#if active}<span class="live-dot"></span>{/if}
                </div>
                <div class="dot-col">
                  <div class="item-dot" style="border-color:{active ? c.accent : past ? 'rgba(255,255,255,0.1)' : c.accent + '50'}; background:{active ? c.accent : 'transparent'}">
                    {#if active}<div class="dot-ripple" style="background:{c.accent}"></div>{/if}
                  </div>
                  {#if i < schedule.length - 1}<div class="connector" class:past></div>{/if}
                </div>
                <div class="item-content">
                  <div class="item-header">
                    <div class="type-pill" style="color:{c.accent}; background:{c.accent}12; border:1px solid {c.accent}25">
                      <svelte:component this={c.icon} size={9} strokeWidth={2.5} />
                      {c.label}
                    </div>
                    <span class="item-duration"><Clock size={9} strokeWidth={2} /> {item.duration}</span>
                  </div>
                  <p class="item-subject" class:past>{item.subject}</p>
                  {#if item.difficulty}
                    <span class="diff-chip" style="color:{diff.color}; background:{diff.bg}">{item.difficulty}</span>
                  {/if}
                </div>
                <button
                  class="action-btn"
                  style="background:{active ? c.accent : 'rgba(255,255,255,0.05)'}; color:{active ? '#000' : 'rgba(255,255,255,0.5)'}; border-color:{active ? c.accent : 'rgba(255,255,255,0.08)'}"
                  on:click={() => goto('/study')}
                >
                  {#if item.status === 'completed'}Done{:else if item.status === 'in-progress'}Resume{:else}Start{/if}
                </button>
              </div>
            {/each}
          {/if}
        </div>

      <!-- ── ROADMAP TAB ── -->
      {:else if activeTab === 'roadmap'}
        <div class="roadmap-section">
          <div class="roadmap-header">
            <Map size={16} color="#a3e635" />
            <div>
              <p class="rm-title">4-Week Learning Roadmap</p>
              <p class="rm-sub">Generated for <span style="color:{vc.color}">{vc.label} velocity</span> · {vc.sessionsPerDay} sessions/day</p>
            </div>
          </div>
          {#each roadmap as week, wi}
            <div class="week-card" style="animation-delay:{wi*80}ms">
              <div class="week-top">
                <div class="week-label">{week.label}</div>
                <div class="week-target">
                  <Target size={11} />
                  {week.completionTarget}% target
                </div>
              </div>
              <div class="week-progress">
                <div class="week-bar"><div class="week-fill" style="width:{week.completionTarget}%; background:{vc.color}"></div></div>
              </div>
              <div class="sessions-grid">
                {#each week.sessions as sess}
                  {@const tc = typeConfig[sess.type] || typeConfig.study}
                  <div class="sess-chip" style="border-color:{tc.accent}25; background:{tc.accent}08">
                    <span class="sess-day">{sess.day}</span>
                    <span class="sess-subj">{sess.subject}</span>
                    <span class="sess-dur" style="color:{tc.accent}">{sess.duration}</span>
                  </div>
                {/each}
              </div>
            </div>
          {/each}
        </div>

      <!-- ── PREDICTION TAB ── -->
      {:else if activeTab === 'prediction'}
        <div class="prediction-section">
          <div class="pred-header">
            <TrendingUp size={16} color="#38bdf8" />
            <div>
              <p class="pred-title">Prediction Engine</p>
              <p class="pred-sub">AI-estimated completion dates based on <span style="color:{vc.color}">{vc.label}</span> velocity</p>
            </div>
          </div>

          <!-- Timeline visualization -->
          <div class="pred-timeline">
            {#each predictions as pred, i}
              {@const statusIcon = pred.status === 'ahead' ? CheckCircle2 : pred.status === 'on-track' ? Circle : AlertCircle}
              <div class="pred-item" style="animation-delay:{i*60}ms">
                <div class="pred-left">
                  <svelte:component this={statusIcon} size={16} color={pred.color} />
                  <div class="pred-info">
                    <p class="pred-subject">{pred.subject}</p>
                    <div class="pred-bar-wrap">
                      <div class="pred-bar">
                        <div class="pred-fill" style="width:{pred.currentProgress}%; background:{pred.color}; box-shadow:0 0 8px {pred.color}60"></div>
                      </div>
                      <span class="pred-pct" style="color:{pred.color}">{pred.currentProgress}%</span>
                    </div>
                  </div>
                </div>
                <div class="pred-right">
                  <div class="pred-date" style="color:{pred.color}">{pred.predictedCompletion}</div>
                  <div class="pred-days">{pred.daysLeft} days left</div>
                  <div class="pred-status" style="background:{pred.color}18; color:{pred.color}">
                    {pred.status === 'ahead' ? '✓ Ahead' : pred.status === 'on-track' ? '→ On Track' : '⚠ At Risk'}
                  </div>
                </div>
              </div>
            {/each}
          </div>

          <!-- Summary card -->
          <div class="pred-summary">
            <div class="pred-sum-title"><BarChart3 size={13} color="#a3e635" /> Velocity Impact Analysis</div>
            <div class="pred-sum-grid">
              {#each (['slow','medium','fast'] as const) as v}
                {@const vc2 = velocityConfig[v]}
                <div class="pred-sum-card" class:highlight={velocity === v} style={velocity === v ? `border-color:${vc2.color}40; background:${vc2.bg}` : ''}>
                  <div class="pred-sum-vel" style={velocity === v ? `color:${vc2.color}` : ''}>{v === 'slow' ? '🐢' : v === 'medium' ? '⚡' : '🚀'} {vc2.label}</div>
                  <div class="pred-sum-metric" style={velocity === v ? `color:${vc2.color}` : ''}>{v === 'slow' ? '~6 weeks' : v === 'medium' ? '~4 weeks' : '~2.5 weeks'}</div>
                  <div class="pred-sum-label">to complete</div>
                </div>
              {/each}
            </div>
          </div>
        </div>
      {/if}
    </div>

    <!-- ── Side Panel ── -->
    <aside class="side-panel">
      <div class="panel-section"><MiniCalendar /></div>
      <div class="panel-section"><CalendarSync /></div>
      <div class="quick-links">
        <button class="quick-btn" on:click={() => goto('/study')}><BookOpen size={14} strokeWidth={1.8} /> Study Planning</button>
        <button class="quick-btn" on:click={() => goto('/dashboard')}><Brain size={14} strokeWidth={1.8} /> Dashboard</button>
      </div>
    </aside>
  </div>

  {#if error}<p class="error-note">Could not sync — showing demo data</p>{/if}
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Geist:wght@400;500;600&display=swap");

  .page {
    font-family: "Geist", system-ui, sans-serif;
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding: 28px 32px 48px;
    max-width: 1000px;
    width: 100%;
    min-height: 100vh;
    opacity: 0;
    transform: translateY(6px);
    transition: opacity 300ms ease, transform 300ms ease;
  }
  .page.mounted { opacity: 1; transform: translateY(0); }

  /* Grid */
  .schedule-grid { display: grid; grid-template-columns: 1fr 300px; gap: 32px; align-items: flex-start; }
  @media (max-width: 850px) { .schedule-grid { grid-template-columns: 1fr; } .side-panel { order: -1; } }
  .main-content  { display: flex; flex-direction: column; gap: 24px; }
  .side-panel    { display: flex; flex-direction: column; gap: 20px; position: sticky; top: 24px; }
  .section-card  { width: 100%; }
  .panel-section { width: 100%; }

  /* Header */
  .page-header { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
  .header-left { display: flex; align-items: center; gap: 12px; }
  .header-icon-wrap { width: 34px; height: 34px; border-radius: 9px; background: rgba(163,230,53,0.12); color: #a3e635; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .page-title { font-size: 20px; font-weight: 700; color: rgba(255,255,255,0.92); letter-spacing: -0.4px; margin: 0; line-height: 1.1; }
  .page-sub   { font-size: 11px; color: rgba(255,255,255,0.28); margin: 2px 0 0; letter-spacing: 0.02em; }
  .add-btn { display: flex; align-items: center; gap: 6px; padding: 8px 14px; background: #a3e635; color: #000; border: none; border-radius: 8px; font-family: "Geist", system-ui, sans-serif; font-size: 12px; font-weight: 700; cursor: pointer; transition: filter 150ms ease; }
  .add-btn:hover { filter: brightness(1.1); }
  .divider { height: 1px; background: rgba(255,255,255,0.05); margin: -8px 0; }

  /* Velocity Card */
  .velocity-card {
    background: #0e0e10;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .velocity-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
  .velocity-title-row { display: flex; align-items: center; gap: 10px; }
  .velocity-icon { width: 30px; height: 30px; border-radius: 8px; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; color: rgba(255,255,255,0.5); }
  .velocity-title { font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.85); margin: 0; }
  .velocity-sub   { font-size: 11px; color: rgba(255,255,255,0.3); margin: 2px 0 0; }
  .velocity-tabs  { display: flex; gap: 6px; flex-wrap: wrap; }
  .velocity-tab {
    padding: 7px 14px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    background: transparent;
    font-family: "Geist", system-ui, sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: rgba(255,255,255,0.4);
    cursor: pointer;
    transition: all 180ms ease;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .velocity-tab:hover { border-color: rgba(255,255,255,0.15); color: rgba(255,255,255,0.7); }
  .velocity-tab.active { font-weight: 700; }
  .velocity-details { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .velocity-desc  { font-size: 11px; color: rgba(255,255,255,0.25); }
  .velocity-badges { display: flex; gap: 6px; flex-wrap: wrap; }
  .vbadge { font-size: 10px; font-weight: 600; padding: 3px 8px; border-radius: 5px; letter-spacing: 0.02em; }
  .generate-btn {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 10px 18px;
    background: rgba(163,230,53,0.12);
    border: 1px solid rgba(163,230,53,0.25);
    border-radius: 9px;
    font-family: "Geist", system-ui, sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: #a3e635;
    cursor: pointer;
    transition: all 180ms ease;
    align-self: flex-start;
  }
  .generate-btn:hover:not(:disabled) { background: rgba(163,230,53,0.18); border-color: rgba(163,230,53,0.4); }
  .generate-btn:disabled { opacity: 0.6; cursor: not-allowed; }
  .generate-btn.loading { opacity: 0.8; }
  .spinner { width: 12px; height: 12px; border: 2px solid rgba(163,230,53,0.3); border-top-color: #a3e635; border-radius: 50%; animation: spin 0.7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Tabs */
  .tabs-bar { display: flex; gap: 4px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 4px; width: fit-content; }
  .tab-btn { display: flex; align-items: center; gap: 6px; padding: 7px 14px; border: none; border-radius: 7px; background: transparent; font-family: "Geist", system-ui, sans-serif; font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.35); cursor: pointer; transition: all 180ms ease; white-space: nowrap; }
  .tab-btn:hover  { color: rgba(255,255,255,0.65); }
  .tab-btn.active { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.9); font-weight: 600; }

  /* Stats */
  .stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
  .stat-card { position: relative; background: #0e0e10; border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 14px 14px 12px; display: flex; flex-direction: column; gap: 2px; overflow: hidden; opacity: 0; transform: translateY(8px); animation: rise 300ms cubic-bezier(0.22,1,0.36,1) forwards; transition: border-color 180ms ease, box-shadow 180ms ease; }
  .stat-card::before { content: ""; position: absolute; inset: 0; background: radial-gradient(ellipse at top left, var(--glow), transparent 65%); opacity: 0; transition: opacity 220ms ease; pointer-events: none; }
  .stat-card:hover { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent), 0 6px 24px var(--glow); }
  .stat-card:hover::before { opacity: 1; }
  .stat-top { margin-bottom: 8px; }
  .stat-sub   { font-size: 9px; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; color: rgba(255,255,255,0.25); }
  .stat-value { font-family: "Barlow Condensed", sans-serif; font-size: 44px; font-weight: 800; line-height: 1; letter-spacing: -1px; background: linear-gradient(175deg, #fff 50%, var(--accent) 160%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  .stat-label { font-family: "Barlow Condensed", sans-serif; font-size: 12px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); opacity: 0.65; margin-bottom: 10px; }
  .stat-bar { height: 2px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
  .stat-bar-fill { height: 100%; background: var(--accent); border-radius: 2px; box-shadow: 0 0 6px var(--accent); transition: width 900ms cubic-bezier(0.22,1,0.36,1); }

  /* Section header + Day tabs */
  .section-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
  .day-tabs { display: flex; align-items: center; gap: 4px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 9px; padding: 3px; }
  .day-tab { padding: 6px 12px; border: none; border-radius: 6px; background: transparent; font-family: "Geist", system-ui, sans-serif; font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.35); cursor: pointer; transition: all 150ms ease; }
  .day-tab:hover  { color: rgba(255,255,255,0.7); }
  .day-tab.active { background: #a3e635; color: #000; font-weight: 700; }
  .nav-arrow { width: 26px; height: 26px; border: none; border-radius: 5px; background: transparent; color: rgba(255,255,255,0.25); display: flex; align-items: center; justify-content: center; cursor: pointer; transition: color 150ms ease; }
  .nav-arrow:hover { color: rgba(255,255,255,0.6); }
  .session-count { font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; color: rgba(255,255,255,0.2); }

  /* Timeline */
  .timeline { display: flex; flex-direction: column; gap: 0; }
  .timeline-item { display: grid; grid-template-columns: 76px 20px 1fr auto; gap: 0 12px; align-items: flex-start; opacity: 0; animation: rise 280ms cubic-bezier(0.22,1,0.36,1) forwards; }
  .timeline-item.skeleton { opacity: 1; animation: none; }
  .item-time { display: flex; flex-direction: column; align-items: flex-end; padding-top: 4px; gap: 4px; }
  .time-str { font-family: "Barlow Condensed", sans-serif; font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.3); letter-spacing: 0.03em; white-space: nowrap; transition: color 200ms ease; }
  .timeline-item.active .time-str { color: rgba(255,255,255,0.85); }
  .live-dot { width: 6px; height: 6px; border-radius: 50%; background: #a3e635; box-shadow: 0 0 6px #a3e635; animation: blink 1.4s ease infinite; align-self: flex-end; }
  .dot-col { display: flex; flex-direction: column; align-items: center; }
  .item-dot { position: relative; width: 12px; height: 12px; border-radius: 50%; border: 1.5px solid; flex-shrink: 0; margin-top: 4px; transition: all 300ms ease; z-index: 1; }
  .dot-ripple { position: absolute; inset: -4px; border-radius: 50%; opacity: 0; animation: ripple 1.8s ease-out infinite; z-index: -1; }
  .connector { width: 1px; min-height: 60px; flex: 1; background: rgba(255,255,255,0.08); transition: background 200ms ease; }
  .connector.past { background: rgba(255,255,255,0.04); }
  .item-content { padding: 0 0 20px; display: flex; flex-direction: column; gap: 4px; }
  .item-header { display: flex; align-items: center; gap: 6px; margin-bottom: 2px; }
  .type-pill { display: flex; align-items: center; gap: 4px; font-size: 9px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; padding: 2px 6px; border-radius: 4px; }
  .item-duration { display: flex; align-items: center; gap: 3px; font-size: 10px; color: rgba(255,255,255,0.2); margin-left: auto; }
  .item-subject { font-size: 14px; font-weight: 500; color: rgba(255,255,255,0.88); margin: 0; transition: color 200ms ease; }
  .item-subject.past { color: rgba(255,255,255,0.25); text-decoration: line-through; text-decoration-color: rgba(255,255,255,0.1); }
  .diff-chip { font-size: 9px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; padding: 2px 6px; border-radius: 4px; align-self: flex-start; }
  .action-btn { margin-top: 2px; padding: 6px 12px; border: 1px solid; border-radius: 7px; font-family: "Geist", system-ui, sans-serif; font-size: 11px; font-weight: 600; cursor: pointer; transition: filter 150ms ease; white-space: nowrap; align-self: flex-start; }
  .action-btn:hover { filter: brightness(1.15); }

  /* Skeleton */
  .skel { border-radius: 4px; background: rgba(255,255,255,0.05); animation: shimmer 1.4s infinite; }
  .skel-dot   { width: 12px; height: 12px; border-radius: 50%; margin-top: 4px; }
  .skel-time  { width: 56px; height: 10px; margin-top: 6px; margin-left: auto; }
  .skel-body  { display: flex; flex-direction: column; gap: 7px; padding-top: 4px; }
  .skel-title { width: 55%; height: 10px; }
  .skel-meta  { width: 30%; height: 8px;  }
  .skel-btn   { width: 56px; height: 28px; border-radius: 7px; margin-top: 4px; }

  /* Empty */
  .empty-state { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 48px 0; text-align: center; }
  .empty-icon  { width: 48px; height: 48px; border-radius: 12px; background: rgba(255,255,255,0.04); color: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; margin-bottom: 4px; }
  .empty-title { font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.5); margin: 0; }
  .empty-sub   { font-size: 12px; color: rgba(255,255,255,0.2); margin: 0 0 12px; }
  .empty-cta   { padding: 8px 16px; background: #a3e635; color: #000; border: none; border-radius: 8px; font-size: 12px; font-weight: 700; cursor: pointer; transition: filter 150ms ease; }
  .empty-cta:hover { filter: brightness(1.1); }

  /* Roadmap */
  .roadmap-section { display: flex; flex-direction: column; gap: 16px; }
  .roadmap-header  { display: flex; align-items: center; gap: 10px; padding-bottom: 4px; }
  .rm-title { font-size: 15px; font-weight: 700; color: rgba(255,255,255,0.9); margin: 0; }
  .rm-sub   { font-size: 11px; color: rgba(255,255,255,0.35); margin: 2px 0 0; }
  .week-card { background: #0e0e10; border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 16px 18px; display: flex; flex-direction: column; gap: 12px; opacity: 0; animation: rise 300ms ease forwards; }
  .week-top    { display: flex; align-items: center; justify-content: space-between; }
  .week-label  { font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.8); }
  .week-target { display: flex; align-items: center; gap: 4px; font-size: 11px; color: rgba(255,255,255,0.3); }
  .week-progress { width: 100%; }
  .week-bar  { height: 3px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
  .week-fill { height: 100%; border-radius: 2px; transition: width 800ms ease; }
  .sessions-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 6px; }
  .sess-chip { display: flex; flex-direction: column; gap: 2px; padding: 8px 10px; border: 1px solid; border-radius: 8px; }
  .sess-day  { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: rgba(255,255,255,0.3); }
  .sess-subj { font-size: 10px; font-weight: 600; color: rgba(255,255,255,0.75); line-height: 1.3; }
  .sess-dur  { font-size: 10px; font-weight: 700; }

  /* Prediction */
  .prediction-section { display: flex; flex-direction: column; gap: 16px; }
  .pred-header { display: flex; align-items: center; gap: 10px; padding-bottom: 4px; }
  .pred-title  { font-size: 15px; font-weight: 700; color: rgba(255,255,255,0.9); margin: 0; }
  .pred-sub    { font-size: 11px; color: rgba(255,255,255,0.35); margin: 2px 0 0; }
  .pred-timeline { display: flex; flex-direction: column; gap: 10px; }
  .pred-item { display: flex; align-items: center; justify-content: space-between; gap: 12px; background: #0e0e10; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 14px 16px; opacity: 0; animation: rise 280ms ease forwards; }
  .pred-left { display: flex; align-items: center; gap: 10px; flex: 1; min-width: 0; }
  .pred-info { flex: 1; min-width: 0; }
  .pred-subject { font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.85); margin: 0 0 8px; }
  .pred-bar-wrap { display: flex; align-items: center; gap: 8px; }
  .pred-bar  { flex: 1; height: 4px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
  .pred-fill { height: 100%; border-radius: 3px; transition: width 800ms ease; }
  .pred-pct  { font-size: 10px; font-weight: 700; min-width: 30px; text-align: right; }
  .pred-right { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; flex-shrink: 0; }
  .pred-date   { font-size: 13px; font-weight: 700; }
  .pred-days   { font-size: 10px; color: rgba(255,255,255,0.3); }
  .pred-status { font-size: 9px; font-weight: 700; padding: 3px 8px; border-radius: 5px; letter-spacing: 0.04em; }
  .pred-summary { background: #0e0e10; border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 16px 18px; }
  .pred-sum-title { display: flex; align-items: center; gap: 7px; font-size: 12px; font-weight: 700; color: rgba(255,255,255,0.6); margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.05em; }
  .pred-sum-grid  { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; }
  .pred-sum-card  { border: 1px solid rgba(255,255,255,0.07); border-radius: 9px; padding: 12px; display: flex; flex-direction: column; gap: 4px; transition: all 200ms ease; }
  .pred-sum-card.highlight { }
  .pred-sum-vel    { font-size: 12px; font-weight: 700; color: rgba(255,255,255,0.5); }
  .pred-sum-metric { font-family: "Barlow Condensed", sans-serif; font-size: 22px; font-weight: 800; color: rgba(255,255,255,0.7); }
  .pred-sum-label  { font-size: 10px; color: rgba(255,255,255,0.25); }

  /* Quick links */
  .quick-links { display: flex; flex-direction: column; gap: 10px; margin-top: 10px; }
  .quick-btn { display: flex; align-items: center; justify-content: center; gap: 7px; padding: 11px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 9px; font-family: "Geist", system-ui, sans-serif; font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.45); cursor: pointer; transition: all 150ms ease; }
  .quick-btn:hover { background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.12); color: rgba(255,255,255,0.75); }
  .error-note { font-size: 10px; color: #f87171; opacity: 0.6; margin: -12px 0 0; text-align: right; }

  /* Animations */
  @keyframes rise    { to { opacity:1; transform:translateY(0); } from { opacity:0; transform:translateY(8px); } }
  @keyframes shimmer { from { background-position:200% 0; } to { background-position:-200% 0; } }
  @keyframes ripple  { 0% { transform:scale(1); opacity:0.5; } 70% { transform:scale(2.8); opacity:0; } 100% { transform:scale(2.8); opacity:0; } }
  @keyframes blink   { 0%, 100% { opacity:1; } 50% { opacity:0.3; } }

  @media (max-width: 860px) { .stats-row { grid-template-columns: repeat(2, 1fr); } .page { padding: 20px 16px 40px; } }
  @media (max-width: 560px) { .timeline-item { grid-template-columns: 60px 16px 1fr auto; gap: 0 8px; } .stat-value { font-size: 36px; } }
</style>
