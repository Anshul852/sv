<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { user, session } from '$lib/stores/auth';
  import { Calendar, Clock, Plus, BookOpen, Brain, RotateCcw, Zap, ChevronLeft, ChevronRight, Activity, CalendarCheck, Settings, BarChart3, Sparkles, Grid3x3, List } from 'lucide-svelte';
  import MiniCalendar from '$lib/components/schedule/MiniCalendar.svelte';
  import StudyHeatmap from '$lib/components/schedule/StudyHeatmap.svelte';
  import CalendarSync from '$lib/components/schedule/CalendarSync.svelte';
  import AIScheduleGenerator from '$lib/components/schedule/AIScheduleGenerator.svelte';

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
    isAIGenerated?: boolean;
    generatedWith?: {
      processingStyle: 'linear' | 'relational' | 'systemic';
      learningType: 'visual' | 'auditory' | 'kinesthetic' | 'omni';
      examType?: string;
      course?: string;
    };
  }

  // ── Config ─────────────────────────────────────────────
  const typeConfig: Record<string, { accent: string; glow: string; label: string; icon: any }> = {
    study:      { accent: '#a3e635', glow: 'rgba(163,230,53,0.15)',  label: 'Study',     icon: BookOpen  },
    'deep-work':{ accent: '#38bdf8', glow: 'rgba(56,189,248,0.15)',  label: 'Deep Work', icon: Brain     },
    review:     { accent: '#f59e0b', glow: 'rgba(245,158,11,0.15)',  label: 'Review',    icon: RotateCcw },
    practice:   { accent: '#e879f9', glow: 'rgba(232,121,249,0.15)', label: 'Practice',  icon: Zap       },
  };

  const difficultyConfig: Record<string, { color: string; bg: string }> = {
    easy:   { color: '#34d399', bg: 'rgba(52,211,153,0.08)'  },
    medium: { color: '#f59e0b', bg: 'rgba(245,158,11,0.08)'  },
    hard:   { color: '#f87171', bg: 'rgba(248,113,113,0.08)' },
  };

  // ── State ──────────────────────────────────────────────
  let schedule: ScheduleItem[] = [];
  let loading = true;
  let error = false;
  let mounted = false;
  let selectedDay = 'today';
  let pollInterval: ReturnType<typeof setInterval>;
  let viewMode: 'timeline' | 'calendar' | 'grid' = 'timeline';
  let aiGeneratorOpen = false;
  let selectedWeek = 0;
  let currentDate = new Date();

  $: stats = {
    total:     schedule.length,
    hours:     schedule.reduce((s, i) => s + i.durationMinutes, 0) / 60,
    completed: schedule.filter(i => i.status === 'completed').length,
    upcoming:  schedule.filter(i => i.status === 'upcoming').length,
    aiGenerated: schedule.filter(i => i.isAIGenerated).length,
  };

  $: now = new Date();

  $: dateLabel = (() => {
    const d = new Date();
    if (selectedDay === 'yesterday') d.setDate(d.getDate() - 1);
    if (selectedDay === 'tomorrow')  d.setDate(d.getDate() + 1);
    return d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
  })();

  // ── Calendar Grid Helpers ──────────────────────────────
  function getWeekDays(weekOffset: number) {
    const days = [];
    const d = new Date(currentDate);
    d.setDate(d.getDate() + (weekOffset * 7) - d.getDay());
    for (let i = 0; i < 7; i++) {
      days.push(new Date(d));
      d.setDate(d.getDate() + 1);
    }
    return days;
  }

  function getHourSlots() {
    return Array.from({ length: 14 }, (_, i) => {
      const hour = i + 7; // 7 AM to 8 PM
      return {
        hour,
        display: hour < 12 ? `${hour}:00 AM` : hour === 12 ? '12:00 PM' : `${hour - 12}:00 PM`
      };
    });
  }

  // ── Helpers ────────────────────────────────────────────
  function cfg(type: string) {
    return typeConfig[type] ?? typeConfig.study;
  }

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
      isAIGenerated:   s.isAIGenerated ?? false,
      generatedWith:   s.generatedWith,
    }));
  }

  function useFallback() {
    schedule = mapItems([
      { id:'1', time:'9:00 AM',  subject:'Data Structures',  type:'study',     duration:'1h 30m', durationMinutes:90,  status:'completed', difficulty:'medium' },
      { id:'2', time:'11:00 AM', subject:'Machine Learning',  type:'deep-work', duration:'2h',     durationMinutes:120, status:'in-progress', difficulty:'hard' },
      { id:'3', time:'2:00 PM',  subject:'Deep Work',         type:'deep-work', duration:'1h',     durationMinutes:60,  status:'upcoming',  difficulty:'hard'   },
      { id:'4', time:'4:00 PM',  subject:'Review Session',    type:'review',    duration:'45m',    durationMinutes:45,  status:'upcoming',  difficulty:'easy'   },
    ]);
  }

  async function fetchSchedule() {
    const currentSession = $session;
    if (!currentSession?.access_token) { useFallback(); loading = false; return; }

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/students/schedule`,
        { headers: { Authorization: `Bearer ${currentSession.access_token}` } }
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const raw  = Array.isArray(data) ? data : data.schedule ?? [];
      if (raw.length) schedule = mapItems(raw);
      else useFallback();
      error = false;
    } catch (e) {
      console.error('Schedule fetch failed:', e);
      error = true;
      useFallback();
    } finally {
      loading = false;
    }
  }

  function handleAIScheduleGenerated(event: any) {
    const newItems = event.detail.schedule;
    schedule = [...schedule, ...mapItems(newItems)];
    aiGeneratorOpen = false;
  }

  onMount(async () => {
    await fetchSchedule();
    mounted = true;
    pollInterval = setInterval(fetchSchedule, 60_000);
  });

  onDestroy(() => clearInterval(pollInterval));
</script>

<svelte:head>
  <title>Schedule — StudyVault</title>
</svelte:head>

<div class="page" class:mounted>

  <!-- ── Header ── -->
  <header class="page-header">
    <div class="header-left">
      <div class="header-icon-wrap">
        <Calendar size={14} strokeWidth={2} />
      </div>
      <div>
        <h1 class="page-title">Schedule</h1>
        <p class="page-sub">{dateLabel}</p>
      </div>
    </div>
    <div class="header-actions">
      <div class="view-toggle">
        <button class="toggle-btn" class:active={viewMode === 'timeline'} on:click={() => viewMode = 'timeline'} title="Timeline View">
          <List size={14} strokeWidth={2} />
        </button>
        <button class="toggle-btn" class:active={viewMode === 'calendar'} on:click={() => viewMode = 'calendar'} title="Calendar View">
          <Calendar size={14} strokeWidth={2} />
        </button>
        <button class="toggle-btn" class:active={viewMode === 'grid'} on:click={() => viewMode = 'grid'} title="Grid View">
          <Grid3x3 size={14} strokeWidth={2} />
        </button>
      </div>
      <button class="ai-gen-btn" on:click={() => aiGeneratorOpen = true}>
        <Sparkles size={14} strokeWidth={2} />
        AI Generate
      </button>
      <button class="add-btn" on:click={() => goto('/study')}>
        <Plus size={14} strokeWidth={2.5} />
        Add Session
      </button>
    </div>
  </header>

  <div class="divider" />

  <!-- ── Main Grid ── -->
  <div class="schedule-grid">
    <!-- ── Main Content ── -->
    <div class="main-content">
      <!-- ── Heatmap ── -->
      <section class="section-card">
        <StudyHeatmap />
      </section>

      <!-- ── Stats ── -->
      <div class="stats-row">
        {#each [
          { label: 'Sessions', sub: "Today's total",  value: loading ? '—' : String(stats.total),            accent: '#a3e635', glow: 'rgba(163,230,53,0.15)',  bar: stats.total / 6       },
          { label: 'Hours',    sub: 'Study time',      value: loading ? '—' : stats.hours.toFixed(1) + 'h',  accent: '#38bdf8', glow: 'rgba(56,189,248,0.15)',  bar: stats.hours / 8       },
          { label: 'Done',     sub: 'Completed',       value: loading ? '—' : String(stats.completed),       accent: '#f59e0b', glow: 'rgba(245,158,11,0.15)',  bar: stats.total ? stats.completed / stats.total : 0 },
          { label: 'AI Gen',   sub: 'AI Generated',    value: loading ? '—' : String(stats.aiGenerated),     accent: '#e879f9', glow: 'rgba(232,121,249,0.15)', bar: stats.total ? stats.aiGenerated / stats.total : 0  },
        ] as s, i}
          <div class="stat-card" style="--accent:{s.accent}; --glow:{s.glow}; animation-delay:{i*70}ms">
            <div class="stat-top">
              <span class="stat-sub">{s.sub}</span>
            </div>
            <div class="stat-value">{s.value}</div>
            <div class="stat-label">{s.label}</div>
            <div class="stat-bar"><div class="stat-bar-fill" style="width:{(mounted && s.bar) ? Math.min(s.bar*100,100) : 0}%" /></div>
          </div>
        {/each}
      </div>

      <!-- ── View Container ── -->
      {#if viewMode === 'timeline'}
        <!-- ── Day tabs ── -->
        <div class="section-header">
          <div class="day-tabs">
            <button class="nav-arrow" on:click={() => selectedDay = selectedDay === 'today' ? 'yesterday' : selectedDay === 'tomorrow' ? 'today' : 'yesterday'}>
              <ChevronLeft size={14} />
            </button>
            {#each [{key:'yesterday',label:'Yesterday'},{key:'today',label:'Today'},{key:'tomorrow',label:'Tomorrow'}] as d}
              <button
                class="day-tab"
                class:active={selectedDay === d.key}
                on:click={() => selectedDay = d.key}
              >{d.label}</button>
            {/each}
            <button class="nav-arrow" on:click={() => selectedDay = selectedDay === 'today' ? 'tomorrow' : selectedDay === 'yesterday' ? 'today' : 'tomorrow'}>
              <ChevronRight size={14} />
            </button>
          </div>
          <span class="session-count">{schedule.length} sessions</span>
        </div>

        <!-- ── Timeline ── -->
        <div class="timeline">
          {#if loading}
            {#each [1,2,3,4] as _, i}
              <div class="timeline-item skeleton" style="animation-delay:{i*60}ms">
                <div class="skel skel-time" />
                <div class="skel skel-dot" />
                <div class="skel-body">
                  <div class="skel skel-title" />
                  <div class="skel skel-meta" />
                </div>
                <div class="skel skel-btn" />
              </div>
            {/each}
          {:else if schedule.length === 0}
            <div class="empty-state">
              <div class="empty-icon"><Calendar size={24} /></div>
              <p class="empty-title">No sessions scheduled</p>
              <p class="empty-sub">Your schedule is clear. Time to plan!</p>
              <button class="empty-cta" on:click={() => aiGeneratorOpen = true}>Generate AI Schedule</button>
            </div>
          {:else}
            {#each schedule as item, i}
              {@const c       = cfg(item.type)}
              {@const active  = isActive(item, i)}
              {@const past    = isPast(item) && !active}
              {@const diff    = difficultyConfig[item.difficulty ?? 'medium'] ?? difficultyConfig.medium}

              <div
                class="timeline-item"
                class:active
                class:past
                class:ai-generated={item.isAIGenerated}
                style="--accent:{c.accent}; --glow:{c.glow}; animation-delay:{i*70}ms"
              >
                <!-- Time -->
                <div class="item-time">
                  <span class="time-str">{item.time}</span>
                  {#if active}<span class="live-dot" />{/if}
                </div>

                <!-- Dot + connector -->
                <div class="dot-col">
                  <div class="item-dot" style="border-color:{active ? c.accent : past ? 'rgba(255,255,255,0.1)' : c.accent + '50'}; background:{active ? c.accent : 'transparent'}">
                    {#if active}<div class="dot-ripple" style="background:{c.accent}" />{/if}
                  </div>
                  {#if i < schedule.length - 1}
                    <div class="connector" class:past />
                  {/if}
                </div>

                <!-- Content -->
                <div class="item-content">
                  <div class="item-header">
                    <div class="type-pill" style="color:{c.accent}; background:{c.accent}12; border:1px solid {c.accent}25">
                      <svelte:component this={c.icon} size={9} strokeWidth={2.5} />
                      {c.label}
                    </div>
                    {#if item.isAIGenerated}
                      <span class="ai-badge">
                        <Sparkles size={8} strokeWidth={2} />
                        AI
                      </span>
                    {/if}
                    <span class="item-duration">
                      <Clock size={9} strokeWidth={2} />
                      {item.duration}
                    </span>
                  </div>
                  <p class="item-subject" class:past>{item.subject}</p>
                  {#if item.difficulty}
                    <span class="diff-chip" style="color:{diff.color}; background:{diff.bg}">{item.difficulty}</span>
                  {/if}
                  {#if item.generatedWith}
                    <div class="ai-meta">
                      <span class="ai-meta-label">{item.generatedWith.processingStyle}</span>
                      <span class="ai-meta-label">{item.generatedWith.learningType}</span>
                      {#if item.generatedWith.course}
                        <span class="ai-meta-label">{item.generatedWith.course}</span>
                      {/if}
                    </div>
                  {/if}
                </div>

                <!-- Action -->
                <button
                  class="action-btn"
                  style="background:{active ? c.accent : 'rgba(255,255,255,0.05)'}; color:{active ? '#000' : 'rgba(255,255,255,0.5)'}; border-color:{active ? c.accent : 'rgba(255,255,255,0.08)'}"
                  on:click={() => goto('/study')}
                >
                  {#if item.status === 'completed'}Done
                  {:else if item.status === 'in-progress'}Resume
                  {:else}Start{/if}
                </button>
              </div>
            {/each}
          {/if}
        </div>
      {:else if viewMode === 'calendar'}
        <!-- ── Calendar Grid View ── -->
        <div class="calendar-view">
          <div class="week-nav">
            <button class="week-nav-btn" on:click={() => selectedWeek--}>
              <ChevronLeft size={14} />
            </button>
            <span class="week-label">Week of {getWeekDays(selectedWeek)[0].toLocaleDateString()}</span>
            <button class="week-nav-btn" on:click={() => selectedWeek++}>
              <ChevronRight size={14} />
            </button>
          </div>

          <div class="calendar-grid">
            <div class="time-column">
              <div class="time-header" />
              {#each getHourSlots() as slot}
                <div class="time-slot">{slot.display}</div>
              {/each}
            </div>

            {#each getWeekDays(selectedWeek) as day, dayIdx}
              <div class="day-column">
                <div class="day-header">{day.toLocaleDateString('en-US', { weekday: 'short', month: 'numeric', day: 'numeric' })}</div>
                {#each getHourSlots() as slot}
                  <div class="hour-block">
                    {#each schedule.filter(item => {
                      const itemHour = parseTime(item.time).getHours();
                      return itemHour === slot.hour;
                    }) as schedItem}
                      {@const c = cfg(schedItem.type)}
                      <div class="calendar-event" style="background:{c.accent}20; border-left:3px solid {c.accent}">
                        <div class="event-title">{schedItem.subject}</div>
                        <div class="event-time">{schedItem.duration}</div>
                      </div>
                    {/each}
                  </div>
                {/each}
              </div>
            {/each}
          </div>
        </div>
      {:else if viewMode === 'grid'}
        <!-- ── Grid View ── -->
        <div class="grid-view">
          {#if loading}
            <p>Loading...</p>
          {:else if schedule.length === 0}
            <div class="empty-state">
              <div class="empty-icon"><Calendar size={24} /></div>
              <p class="empty-title">No sessions scheduled</p>
              <p class="empty-sub">Your schedule is clear. Time to plan!</p>
              <button class="empty-cta" on:click={() => aiGeneratorOpen = true}>Generate AI Schedule</button>
            </div>
          {:else}
            {#each schedule as item}
              {@const c = cfg(item.type)}
              {@const diff = difficultyConfig[item.difficulty ?? 'medium'] ?? difficultyConfig.medium}
              <div class="grid-card" style="border-left:4px solid {c.accent}">
                <div class="grid-header">
                  <span class="grid-time">{item.time}</span>
                  {#if item.isAIGenerated}
                    <Sparkles size={12} />
                  {/if}
                </div>
                <h3 class="grid-subject">{item.subject}</h3>
                <div class="grid-meta">
                  <span class="grid-type" style="color:{c.accent}">{c.label}</span>
                  <span class="grid-duration">{item.duration}</span>
                </div>
                <div class="grid-footer">
                  <span class="diff-chip" style="color:{diff.color}; background:{diff.bg}">{item.difficulty}</span>
                  <button class="grid-btn" on:click={() => goto('/study')}>Start</button>
                </div>
              </div>
            {/each}
          {/if}
        </div>
      {/if}
    </div>

    <!-- ── Side Panel ── -->
    <aside class="side-panel">
      <div class="panel-section">
        <MiniCalendar />
      </div>

      <div class="panel-section">
        <CalendarSync />
      </div>

      <div class="quick-links">
        <button class="quick-btn" on:click={() => aiGeneratorOpen = true}>
          <Sparkles size={14} strokeWidth={1.8} />
          AI Schedule
        </button>
        <button class="quick-btn" on:click={() => goto('/study')}>
          <BookOpen size={14} strokeWidth={1.8} />
          Study Planning
        </button>
        <button class="quick-btn" on:click={() => goto('/dashboard')}>
          <Brain size={14} strokeWidth={1.8} />
          Dashboard
        </button>
      </div>
    </aside>
  </div>

  {#if error}
    <p class="error-note">Could not sync — showing demo data</p>
  {/if}

  <!-- ── AI Schedule Generator Modal ── -->
  {#if aiGeneratorOpen}
    <AIScheduleGenerator on:close={() => aiGeneratorOpen = false} on:schedule-generated={handleAIScheduleGenerated} />
  {/if}
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Geist:wght@400;500;600&display=swap");

  /* ── Page ── */
  .page {
    font-family: "Geist", system-ui, sans-serif;
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding: 28px 32px 48px;
    max-width: 1200px;
    width: 100%;
    min-height: 100vh;
    opacity: 0;
    transform: translateY(6px);
    transition: opacity 300ms ease, transform 300ms ease;
  }

  .page.mounted { opacity: 1; transform: translateY(0); }

  /* ── Grid Layout ── */
  .schedule-grid {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 32px;
    align-items: flex-start;
  }

  @media (max-width: 850px) {
    .schedule-grid {
      grid-template-columns: 1fr;
    }
    .side-panel {
      order: -1;
    }
  }

  .main-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .side-panel {
    display: flex;
    flex-direction: column;
    gap: 20px;
    position: sticky;
    top: 24px;
  }

  .section-card {
    width: 100%;
  }

  .panel-section {
    width: 100%;
  }

  .quick-links {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 10px;
  }

  /* ── Header ── */
  .page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .header-icon-wrap {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background: rgba(163, 230, 53, 0.12);
    color: #a3e635;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .page-title {
    font-size: 20px;
    font-weight: 700;
    color: rgba(255,255,255,0.92);
    letter-spacing: -0.4px;
    margin: 0;
    line-height: 1.1;
  }

  .page-sub {
    font-size: 11px;
    color: rgba(255,255,255,0.28);
    margin: 2px 0 0;
    letter-spacing: 0.02em;
  }

  .header-actions {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .view-toggle {
    display: flex;
    gap: 4px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 4px;
  }

  .toggle-btn {
    width: 32px;
    height: 32px;
    border: none;
    background: transparent;
    color: rgba(255,255,255,0.3);
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 150ms ease;
  }

  .toggle-btn.active {
    background: #a3e635;
    color: #000;
  }

  .toggle-btn:hover {
    color: rgba(255,255,255,0.6);
  }

  .ai-gen-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    background: rgba(232, 121, 249, 0.1);
    color: #e879f9;
    border: 1px solid rgba(232, 121, 249, 0.2);
    border-radius: 8px;
    font-family: "Geist", system-ui, sans-serif;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    letter-spacing: 0.02em;
    transition: all 150ms ease;
  }

  .ai-gen-btn:hover {
    background: rgba(232, 121, 249, 0.15);
    border-color: rgba(232, 121, 249, 0.4);
  }

  .add-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    background: #a3e635;
    color: #000;
    border: none;
    border-radius: 8px;
    font-family: "Geist", system-ui, sans-serif;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    letter-spacing: 0.02em;
    transition: filter 150ms ease, transform 150ms ease;
    flex-shrink: 0;
  }

  .add-btn:hover  { filter: brightness(1.1); }
  .add-btn:active { transform: scale(0.97); }

  /* ── Divider ── */
  .divider {
    height: 1px;
    background: rgba(255,255,255,0.05);
    margin: -8px 0;
  }

  /* ── Stats ── */
  .stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
  }

  .stat-card {
    position: relative;
    background: #0e0e10;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 14px 14px 12px;
    display: flex;
    flex-direction: column;
    gap: 2px;
    overflow: hidden;
    opacity: 0;
    transform: translateY(8px);
    animation: rise 300ms cubic-bezier(0.22,1,0.36,1) forwards;
    transition: border-color 180ms ease, box-shadow 180ms ease;
  }

  .stat-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at top left, var(--glow), transparent 65%);
    opacity: 0;
    transition: opacity 220ms ease;
    pointer-events: none;
  }

  .stat-card:hover { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent), 0 6px 24px var(--glow); }
  .stat-card:hover::before { opacity: 1; }

  .stat-top { margin-bottom: 8px; }

  .stat-sub {
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.25);
  }

  .stat-value {
    font-family: "Barlow Condensed", sans-serif;
    font-size: 44px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -1px;
    font-variant-numeric: tabular-nums;
    background: linear-gradient(175deg, #fff 50%, var(--accent) 160%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .stat-label {
    font-family: "Barlow Condensed", sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    opacity: 0.65;
    margin-bottom: 10px;
  }

  .stat-bar {
    height: 2px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    overflow: hidden;
  }

  .stat-bar-fill {
    height: 100%;
    background: var(--accent);
    border-radius: 2px;
    box-shadow: 0 0 6px var(--accent);
    transition: width 900ms cubic-bezier(0.22,1,0.36,1);
  }

  /* ── Calendar View ── */
  .calendar-view {
    background: #0e0e10;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 20px;
    overflow-x: auto;
  }

  .week-nav {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-bottom: 20px;
  }

  .week-nav-btn {
    width: 28px;
    height: 28px;
    border: 1px solid rgba(255,255,255,0.1);
    background: transparent;
    border-radius: 6px;
    color: rgba(255,255,255,0.4);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 150ms ease;
  }

  .week-nav-btn:hover {
    border-color: rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.7);
  }

  .week-label {
    font-size: 13px;
    font-weight: 600;
    color: rgba(255,255,255,0.6);
    min-width: 180px;
    text-align: center;
  }

  .calendar-grid {
    display: grid;
    grid-template-columns: 80px repeat(7, 1fr);
    gap: 1px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px;
    overflow: hidden;
  }

  .time-column {
    background: rgba(255,255,255,0.02);
    border-right: 1px solid rgba(255,255,255,0.05);
  }

  .time-header {
    height: 40px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
  }

  .time-slot {
    height: 60px;
    padding: 4px;
    font-size: 10px;
    color: rgba(255,255,255,0.25);
    border-bottom: 1px solid rgba(255,255,255,0.03);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .day-column {
    display: flex;
    flex-direction: column;
    background: rgba(0,0,0,0.2);
  }

  .day-header {
    height: 40px;
    padding: 8px;
    font-size: 11px;
    font-weight: 600;
    color: rgba(255,255,255,0.6);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .hour-block {
    height: 60px;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    padding: 2px;
    position: relative;
  }

  .calendar-event {
    padding: 4px;
    border-radius: 4px;
    font-size: 9px;
    color: rgba(255,255,255,0.8);
    overflow: hidden;
    cursor: pointer;
    transition: all 150ms ease;
  }

  .calendar-event:hover {
    filter: brightness(1.2);
  }

  .event-title {
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .event-time {
    font-size: 8px;
    color: rgba(255,255,255,0.5);
    margin-top: 2px;
  }

  /* ── Grid View ── */
  .grid-view {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }

  .grid-card {
    background: #0e0e10;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    transition: all 200ms ease;
    cursor: pointer;
  }

  .grid-card:hover {
    background: #151517;
    border-color: rgba(255,255,255,0.1);
  }

  .grid-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .grid-time {
    font-size: 12px;
    font-weight: 600;
    color: rgba(255,255,255,0.5);
  }

  .grid-subject {
    font-size: 14px;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
    margin: 0;
  }

  .grid-meta {
    display: flex;
    gap: 8px;
    font-size: 11px;
  }

  .grid-type {
    font-weight: 600;
  }

  .grid-duration {
    color: rgba(255,255,255,0.4);
  }

  .grid-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
  }

  .grid-btn {
    padding: 6px 12px;
    background: rgba(163, 230, 53, 0.1);
    border: 1px solid rgba(163, 230, 53, 0.2);
    color: #a3e635;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    transition: all 150ms ease;
  }

  .grid-btn:hover {
    background: #a3e635;
    color: #000;
    border-color: #a3e635;
  }

  /* ── Timeline ── */
  .timeline {
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .timeline-item {
    display: grid;
    grid-template-columns: 76px 20px 1fr auto;
    gap: 0 12px;
    align-items: flex-start;
    opacity: 0;
    animation: rise 280ms cubic-bezier(0.22,1,0.36,1) forwards;
  }

  .timeline-item.ai-generated {
    border-left: 2px dashed rgba(232, 121, 249, 0.3);
    padding-left: 12px;
    margin-left: -12px;
  }

  .timeline-item.skeleton { opacity: 1; animation: none; }

  /* Time col */
  .item-time {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    padding-top: 4px;
    gap: 4px;
  }

  .time-str {
    font-family: "Barlow Condensed", sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: rgba(255,255,255,0.3);
    letter-spacing: 0.03em;
    white-space: nowrap;
    transition: color 200ms ease;
  }

  .timeline-item.active .time-str { color: rgba(255,255,255,0.85); }

  .live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #a3e635;
    box-shadow: 0 0 6px #a3e635;
    animation: blink 1.4s ease infinite;
    align-self: flex-end;
  }

  /* Dot col */
  .dot-col {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .item-dot {
    position: relative;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 1.5px solid;
    flex-shrink: 0;
    margin-top: 4px;
    transition: background 300ms ease, border-color 300ms ease;
    z-index: 1;
  }

  .dot-ripple {
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    opacity: 0;
    animation: ripple 1.8s ease-out infinite;
    z-index: -1;
  }

  .connector {
    width: 1px;
    min-height: 60px;
    flex: 1;
    background: rgba(255,255,255,0.08);
    transition: background 200ms ease;
  }

  .connector.past { background: rgba(255,255,255,0.04); }

  /* Content */
  .item-content {
    padding: 0 0 20px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .item-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 2px;
    flex-wrap: wrap;
  }

  .type-pill {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 4px;
  }

  .ai-badge {
    display: flex;
    align-items: center;
    gap: 2px;
    font-size: 8px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 4px;
    color: #e879f9;
    background: rgba(232, 121, 249, 0.1);
    border: 1px solid rgba(232, 121, 249, 0.2);
  }

  .item-duration {
    display: flex;
    align-items: center;
    gap: 3px;
    font-size: 10px;
    color: rgba(255,255,255,0.2);
    margin-left: auto;
  }

  .item-subject {
    font-size: 14px;
    font-weight: 500;
    color: rgba(255,255,255,0.88);
    margin: 0;
    transition: color 200ms ease;
  }

  .item-subject.past {
    color: rgba(255,255,255,0.25);
    text-decoration: line-through;
    text-decoration-color: rgba(255,255,255,0.1);
  }

  .diff-chip {
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 4px;
    align-self: flex-start;
  }

  .ai-meta {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 4px;
  }

  .ai-meta-label {
    font-size: 8px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 3px;
    background: rgba(232, 121, 249, 0.08);
    color: #e879f9;
  }

  /* Action */
  .action-btn {
    margin-top: 2px;
    padding: 6px 12px;
    border: 1px solid;
    border-radius: 7px;
    font-family: "Geist", system-ui, sans-serif;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    transition: filter 150ms ease, transform 150ms ease;
    white-space: nowrap;
    align-self: flex-start;
  }

  .action-btn:hover  { filter: brightness(1.15); }
  .action-btn:active { transform: scale(0.96); }

  /* Section header */
  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .day-tabs {
    display: flex;
    align-items: center;
    gap: 4px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 9px;
    padding: 3px;
  }

  .day-tab {
    padding: 6px 12px;
    border: none;
    border-radius: 6px;
    background: transparent;
    font-family: "Geist", system-ui, sans-serif;
    font-size: 12px;
    font-weight: 500;
    color: rgba(255,255,255,0.35);
    cursor: pointer;
    transition: background 150ms ease, color 150ms ease;
  }

  .day-tab:hover  { color: rgba(255,255,255,0.7); }
  .day-tab.active { background: #a3e635; color: #000; font-weight: 700; }

  .nav-arrow {
    width: 26px;
    height: 26px;
    border: none;
    border-radius: 5px;
    background: transparent;
    color: rgba(255,255,255,0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: color 150ms ease;
  }

  .nav-arrow:hover { color: rgba(255,255,255,0.6); }

  .session-count {
    font-size: 10px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: rgba(255,255,255,0.2);
  }

  /* Skeleton */
  .skel {
    border-radius: 4px;
    background: rgba(255,255,255,0.05);
    background-size: 200% 100%;
    animation: shimmer 1.4s infinite;
  }

  .skel-dot   { width: 12px; height: 12px; border-radius: 50%; margin-top: 4px; }
  .skel-time  { width: 56px; height: 10px; margin-top: 6px; margin-left: auto; }
  .skel-body  { display: flex; flex-direction: column; gap: 7px; padding-top: 4px; }
  .skel-title { width: 55%; height: 10px; }
  .skel-meta  { width: 30%; height: 8px;  }
  .skel-btn   { width: 56px; height: 28px; border-radius: 7px; margin-top: 4px; }

  /* Empty */
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 48px 0;
    text-align: center;
  }

  .empty-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    color: rgba(255,255,255,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 4px;
  }

  .empty-title {
    font-size: 14px;
    font-weight: 600;
    color: rgba(255,255,255,0.5);
    margin: 0;
  }

  .empty-sub {
    font-size: 12px;
    color: rgba(255,255,255,0.2);
    margin: 0 0 12px;
  }

  .empty-cta {
    padding: 8px 16px;
    background: rgba(232, 121, 249, 0.1);
    color: #e879f9;
    border: 1px solid rgba(232, 121, 249, 0.2);
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: all 150ms ease;
  }

  .empty-cta:hover {
    background: rgba(232, 121, 249, 0.15);
    border-color: rgba(232, 121, 249, 0.4);
  }

  /* Quick links */
  .quick-links {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 10px;
  }

  .quick-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    padding: 11px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 9px;
    font-family: "Geist", system-ui, sans-serif;
    font-size: 12px;
    font-weight: 500;
    color: rgba(255,255,255,0.45);
    cursor: pointer;
    transition: background 150ms ease, border-color 150ms ease, color 150ms ease;
  }

  .quick-btn:hover {
    background: rgba(255,255,255,0.04);
    border-color: rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.75);
  }

  /* Error */
  .error-note {
    font-size: 10px;
    color: #f87171;
    opacity: 0.6;
    margin: -12px 0 0;
    text-align: right;
  }

  /* Keyframes */
  @keyframes rise {
    to   { opacity: 1; transform: translateY(0); }
    from { opacity: 0; transform: translateY(8px); }
  }

  @keyframes shimmer {
    from { background-position: 200% 0; }
    to   { background-position: -200% 0; }
  }

  @keyframes ripple {
    0%  { transform: scale(1);   opacity: 0.5; }
    70% { transform: scale(2.8); opacity: 0;   }
    100%{ transform: scale(2.8); opacity: 0;   }
  }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
  }

  /* Responsive */
  @media (max-width: 860px) {
    .stats-row { grid-template-columns: repeat(2, 1fr); }
    .page { padding: 20px 16px 40px; }
    .calendar-grid { grid-template-columns: 60px repeat(7, 1fr); }
  }

  @media (max-width: 560px) {
    .timeline-item { grid-template-columns: 60px 16px 1fr auto; gap: 0 8px; }
    .quick-links     { flex-direction: row; }
    .stat-value    { font-size: 36px; }
    .grid-view { grid-template-columns: 1fr; }
  }
</style>
