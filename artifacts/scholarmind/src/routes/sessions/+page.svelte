<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { user } from "$lib/stores/auth";
    import {
        Play,
        Pause,
        Square,
        Clock,
        BookOpen,
        Brain,
        BarChart3,
        Plus,
        ChevronDown,
        Zap,
    } from "lucide-svelte";

    // ── Types ──────────────────────────────────────────────
    interface Session {
        id: string;
        subject: string;
        topic: string;
        duration: string;
        retention: number;
        date: string;
        anxiety: "low" | "medium" | "high";
    }

    // ── Timer state ────────────────────────────────────────
    let isActive = false;
    let isPaused = false;
    let elapsed = 0;
    let mounted = false;
    let timer: ReturnType<typeof setInterval>;

    // ── Session setup ──────────────────────────────────────
    let subject = "Algorithms";
    let topic = "Graph Traversals";
    let anxiety: "low" | "medium" | "high" = "low";

    // ── Past sessions ──────────────────────────────────────
    let pastSessions: Session[] = [];
    let loadingSessions = true;

    // ── Config ─────────────────────────────────────────────
    const anxietyConfig = {
        low: { color: "#34d399", bg: "rgba(52,211,153,0.08)", label: "Low" },
        medium: {
            color: "#f59e0b",
            bg: "rgba(245,158,11,0.08)",
            label: "Medium",
        },
        high: { color: "#f87171", bg: "rgba(248,113,113,0.08)", label: "High" },
    };

    function retentionColor(r: number): string {
        if (r >= 80) return "#a3e635";
        if (r >= 60) return "#f59e0b";
        return "#f87171";
    }

    // ── Timer ──────────────────────────────────────────────
    function formatTime(s: number): string {
        const h = Math.floor(s / 3600);
        const m = Math.floor((s % 3600) / 60);
        const sec = s % 60;
        return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
    }

    function startSession() {
        isActive = true;
        isPaused = false;
        timer = setInterval(() => {
            elapsed += 1;
        }, 1000);
    }

    function pauseSession() {
        isPaused = !isPaused;
        if (isPaused) clearInterval(timer);
        else
            timer = setInterval(() => {
                elapsed += 1;
            }, 1000);
    }

    function endSession() {
        isActive = false;
        isPaused = false;
        clearInterval(timer);
        elapsed = 0;
    }

    $: formattedTime = formatTime(elapsed);
    $: progress = Math.min((elapsed / 5400) * 100, 100); // 90 min target

    // ── Fetch past sessions ────────────────────────────────
    async function fetchSessions() {
        const currentUser = $user;
        if (!currentUser?.session?.access_token) {
            useFallback();
            return;
        }

        try {
            const res = await fetch(
                `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/api/students/sessions`,
                {
                    headers: {
                        Authorization: `Bearer ${currentUser.session.access_token}`,
                    },
                },
            );
            if (!res.ok) throw new Error();
            const data = await res.json();
            pastSessions = (
                Array.isArray(data) ? data : (data.sessions ?? [])
            ).map((s: any) => ({
                id: s.id ?? Math.random().toString(36).slice(2),
                subject: s.subject ?? s.topic_area ?? "Study",
                topic: s.topic ?? s.subtopic ?? "Session",
                duration: s.duration ?? "—",
                retention: s.retention_score ?? s.retention ?? 0,
                date: s.date ?? s.created_at ?? "—",
                anxiety: s.anxiety_level ?? s.anxiety ?? "low",
            }));
        } catch {
            useFallback();
        } finally {
            loadingSessions = false;
        }
    }

    function useFallback() {
        pastSessions = [
            {
                id: "1",
                subject: "Algorithms",
                topic: "Dynamic Programming",
                duration: "1h 30m",
                retention: 85,
                date: "Today",
                anxiety: "low",
            },
            {
                id: "2",
                subject: "Linear Algebra",
                topic: "Eigenvalues",
                duration: "45m",
                retention: 72,
                date: "Yesterday",
                anxiety: "medium",
            },
            {
                id: "3",
                subject: "OS",
                topic: "Memory Management",
                duration: "1h 15m",
                retention: 68,
                date: "Yesterday",
                anxiety: "high",
            },
            {
                id: "4",
                subject: "Databases",
                topic: "SQL Joins",
                duration: "50m",
                retention: 91,
                date: "2 days ago",
                anxiety: "low",
            },
        ];
        loadingSessions = false;
    }

    onMount(async () => {
        mounted = true;
        await fetchSessions();
    });

    onDestroy(() => clearInterval(timer));
</script>

<svelte:head><title>Study Sessions — StudyVault</title></svelte:head>

<div class="page" class:mounted>
    <!-- ── Header ── -->
    <header class="page-header">
        <div class="header-left">
            <div class="header-icon">
                <BookOpen size={14} strokeWidth={2} />
            </div>
            <div>
                <h1 class="page-title">Study Sessions</h1>
                <p class="page-sub">Track learning with retention scoring</p>
            </div>
        </div>
    </header>

    <div class="divider" />

    <!-- ── Active Session Card ── -->
    <div class="session-card" class:active={isActive}>
        <!-- Timer display -->
        <div class="timer-row">
            <div class="timer-left">
                <span class="timer-label"
                    >{isActive
                        ? isPaused
                            ? "Paused"
                            : "In Progress"
                        : "Ready to start"}</span
                >
                <div class="timer-display">{formattedTime}</div>
                <span class="timer-target">/ 90:00 target</span>
            </div>

            <!-- Circular progress -->
            <div class="timer-ring-wrap">
                <svg viewBox="0 0 80 80" class="timer-ring">
                    <circle
                        cx="40"
                        cy="40"
                        r="34"
                        fill="none"
                        stroke="rgba(255,255,255,0.05)"
                        stroke-width="5"
                    />
                    <circle
                        cx="40"
                        cy="40"
                        r="34"
                        fill="none"
                        stroke={isActive ? "#a3e635" : "rgba(255,255,255,0.1)"}
                        stroke-width="5"
                        stroke-linecap="round"
                        stroke-dasharray="{(progress / 100) * 213.6} 213.6"
                        transform="rotate(-90 40 40)"
                        style="transition: stroke-dasharray 1s linear, stroke 300ms ease; filter: drop-shadow(0 0 4px #a3e635);"
                    />
                    <text
                        x="40"
                        y="44"
                        text-anchor="middle"
                        fill={isActive ? "#a3e635" : "rgba(255,255,255,0.3)"}
                        font-size="11"
                        font-weight="700"
                        font-family="Barlow Condensed, sans-serif"
                    >
                        {Math.round(progress)}%
                    </text>
                </svg>
            </div>
        </div>

        <!-- Session meta -->
        <div class="meta-row">
            <div class="meta-field">
                <span class="meta-label">Subject</span>
                <span class="meta-value">{subject}</span>
            </div>
            <div class="meta-divider" />
            <div class="meta-field">
                <span class="meta-label">Topic</span>
                <span class="meta-value">{topic}</span>
            </div>
            <div class="meta-divider" />
            <div class="meta-field">
                <span class="meta-label">Anxiety</span>
                <span
                    class="meta-value"
                    style="color:{anxietyConfig[anxiety].color}"
                    >{anxietyConfig[anxiety].label}</span
                >
            </div>
        </div>

        <!-- Controls -->
        <div class="controls-row">
            {#if !isActive}
                <button class="btn-primary" on:click={startSession}>
                    <Play size={14} strokeWidth={2.5} />
                    Start Session
                </button>
            {:else}
                <button class="btn-secondary" on:click={pauseSession}>
                    {#if isPaused}
                        <Play size={14} strokeWidth={2.5} />
                        Resume
                    {:else}
                        <Pause size={14} strokeWidth={2.5} />
                        Pause
                    {/if}
                </button>
                <button class="btn-danger" on:click={endSession}>
                    <Square size={13} strokeWidth={2.5} />
                    End Session
                </button>
            {/if}
        </div>

        <!-- Glow when active -->
        {#if isActive && !isPaused}
            <div class="active-glow" />
        {/if}
    </div>

    <!-- ── Recent Sessions ── -->
    <div class="section-header">
        <span class="section-dot" />
        <h2 class="section-title">Recent Sessions</h2>
        <span class="session-count">{pastSessions.length} total</span>
    </div>

    <div class="sessions-list">
        {#if loadingSessions}
            {#each [1, 2, 3, 4] as _, i}
                <div
                    class="session-row skeleton"
                    style="animation-delay:{i * 60}ms"
                >
                    <div class="skel skel-icon" />
                    <div class="skel-body">
                        <div class="skel skel-title" />
                        <div class="skel skel-sub" />
                    </div>
                    <div class="skel skel-stat" />
                    <div class="skel skel-stat" />
                </div>
            {/each}
        {:else}
            {#each pastSessions as s, i}
                {@const ac = anxietyConfig[s.anxiety]}
                {@const rc = retentionColor(s.retention)}
                <div class="session-row" style="animation-delay:{i * 55}ms">
                    <!-- Icon -->
                    <div class="session-icon">
                        <BookOpen size={13} strokeWidth={1.8} />
                    </div>

                    <!-- Info -->
                    <div class="session-info">
                        <p class="session-name">
                            {s.subject}
                            <span class="session-topic">— {s.topic}</span>
                        </p>
                        <p class="session-meta">
                            <Clock size={9} strokeWidth={2} />
                            {s.date} · {s.duration}
                        </p>
                    </div>

                    <!-- Retention -->
                    <div class="stat-col">
                        <div class="stat-value" style="color:{rc}">
                            {s.retention}%
                        </div>
                        <div class="stat-bar-mini">
                            <div
                                class="stat-bar-fill"
                                style="width:{s.retention}%; background:{rc}"
                            />
                        </div>
                        <span class="stat-label">retention</span>
                    </div>

                    <!-- Anxiety -->
                    <div class="stat-col">
                        <span
                            class="anxiety-chip"
                            style="color:{ac.color}; background:{ac.bg}"
                        >
                            <Brain size={9} strokeWidth={2} />
                            {ac.label}
                        </span>
                        <span class="stat-label">anxiety</span>
                    </div>
                </div>
            {/each}
        {/if}
    </div>
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Geist:wght@400;500;600&display=swap");

    /* ── Page ── */
    .page {
        font-family: "Geist", system-ui, sans-serif;
        display: flex;
        flex-direction: column;
        gap: 20px;
        padding: 28px 32px 48px;
        max-width: 860px;
        width: 100%;
        opacity: 0;
        transform: translateY(6px);
        transition:
            opacity 300ms ease,
            transform 300ms ease;
    }

    .page.mounted {
        opacity: 1;
        transform: translateY(0);
    }

    /* ── Header ── */
    .page-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .header-icon {
        width: 34px;
        height: 34px;
        border-radius: 9px;
        background: rgba(163, 230, 53, 0.1);
        color: #a3e635;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .page-title {
        font-size: 20px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.92);
        letter-spacing: -0.4px;
        margin: 0;
        line-height: 1.1;
    }

    .page-sub {
        font-size: 11px;
        color: rgba(255, 255, 255, 0.28);
        margin: 2px 0 0;
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.05);
        flex-shrink: 0;
    }

    /* ── Session card ── */
    .session-card {
        position: relative;
        background: #0e0e10;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 24px;
        display: flex;
        flex-direction: column;
        gap: 20px;
        overflow: hidden;
        transition:
            border-color 300ms ease,
            box-shadow 300ms ease;
    }

    .session-card.active {
        border-color: rgba(163, 230, 53, 0.3);
        box-shadow:
            0 0 0 1px rgba(163, 230, 53, 0.15),
            0 12px 40px rgba(163, 230, 53, 0.08);
    }

    .active-glow {
        position: absolute;
        top: -40px;
        right: -40px;
        width: 160px;
        height: 160px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            rgba(163, 230, 53, 0.12),
            transparent 70%
        );
        pointer-events: none;
        animation: pulse-glow 2s ease-in-out infinite;
    }

    /* ── Timer row ── */
    .timer-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
    }

    .timer-left {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .timer-label {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.25);
    }

    .timer-display {
        font-family: "Barlow Condensed", sans-serif;
        font-size: 52px;
        font-weight: 800;
        color: #fff;
        letter-spacing: -1px;
        line-height: 1;
        font-variant-numeric: tabular-nums;
    }

    .timer-target {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.2);
    }

    .timer-ring-wrap {
        width: 80px;
        height: 80px;
        flex-shrink: 0;
    }
    .timer-ring {
        width: 100%;
        height: 100%;
    }

    /* ── Meta row ── */
    .meta-row {
        display: flex;
        align-items: center;
        gap: 0;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 9px;
        overflow: hidden;
    }

    .meta-field {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 3px;
        padding: 12px 14px;
    }

    .meta-divider {
        width: 1px;
        height: 36px;
        background: rgba(255, 255, 255, 0.06);
        flex-shrink: 0;
    }

    .meta-label {
        font-size: 9px;
        font-weight: 600;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.22);
    }

    .meta-value {
        font-size: 13px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.8);
    }

    /* ── Controls ── */
    .controls-row {
        display: flex;
        gap: 8px;
    }

    .btn-primary {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 9px 18px;
        background: #a3e635;
        color: #000;
        border: none;
        border-radius: 8px;
        font-family: "Geist", system-ui, sans-serif;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        transition:
            filter 150ms ease,
            transform 150ms ease;
    }

    .btn-primary:hover {
        filter: brightness(1.1);
    }
    .btn-primary:active {
        transform: scale(0.97);
    }

    .btn-secondary {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 9px 16px;
        background: rgba(255, 255, 255, 0.06);
        color: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        font-family: "Geist", system-ui, sans-serif;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: background 150ms ease;
    }

    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.09);
    }

    .btn-danger {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 9px 16px;
        background: rgba(248, 113, 113, 0.08);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.2);
        border-radius: 8px;
        font-family: "Geist", system-ui, sans-serif;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: background 150ms ease;
    }

    .btn-danger:hover {
        background: rgba(248, 113, 113, 0.14);
    }

    /* ── Section header ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 7px;
    }

    .section-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #a3e635;
        flex-shrink: 0;
    }

    .section-title {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.28);
        margin: 0;
    }

    .session-count {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.18);
        margin-left: auto;
        letter-spacing: 0.04em;
    }

    /* ── Sessions list ── */
    .sessions-list {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .session-row {
        display: grid;
        grid-template-columns: 32px 1fr auto auto;
        gap: 12px;
        align-items: center;
        padding: 12px 14px;
        border-radius: 9px;
        border: 1px solid transparent;
        opacity: 0;
        animation: rise 280ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
        transition:
            background 150ms ease,
            border-color 150ms ease;
        cursor: default;
    }

    .session-row:hover {
        background: rgba(255, 255, 255, 0.03);
        border-color: rgba(255, 255, 255, 0.06);
    }

    .session-row.skeleton {
        opacity: 1;
        animation: none;
    }

    /* Icon */
    .session-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: rgba(163, 230, 53, 0.07);
        color: #a3e635;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    /* Info */
    .session-info {
        display: flex;
        flex-direction: column;
        gap: 3px;
        min-width: 0;
    }

    .session-name {
        font-size: 13px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.82);
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .session-topic {
        color: rgba(255, 255, 255, 0.35);
        font-weight: 400;
    }

    .session-meta {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 10px;
        color: rgba(255, 255, 255, 0.22);
        margin: 0;
    }

    /* Stat col */
    .stat-col {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 3px;
        min-width: 60px;
    }

    .stat-value {
        font-family: "Barlow Condensed", sans-serif;
        font-size: 18px;
        font-weight: 700;
        line-height: 1;
        letter-spacing: -0.5px;
    }

    .stat-bar-mini {
        width: 48px;
        height: 2px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 2px;
        overflow: hidden;
    }

    .stat-bar-fill {
        height: 100%;
        border-radius: 2px;
        transition: width 700ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    .stat-label {
        font-size: 9px;
        color: rgba(255, 255, 255, 0.2);
        letter-spacing: 0.04em;
    }

    .anxiety-chip {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.04em;
        padding: 3px 7px;
        border-radius: 5px;
    }

    /* ── Skeleton ── */
    .skel {
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.05);
        background-size: 200% 100%;
        animation: shimmer 1.4s infinite;
    }

    .skel-body {
        display: flex;
        flex-direction: column;
        gap: 6px;
        flex: 1;
    }
    .skel-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        flex-shrink: 0;
    }
    .skel-title {
        width: 55%;
        height: 10px;
    }
    .skel-sub {
        width: 35%;
        height: 8px;
    }
    .skel-stat {
        width: 52px;
        height: 28px;
        border-radius: 6px;
    }

    /* ── Keyframes ── */
    @keyframes rise {
        from {
            opacity: 0;
            transform: translateY(6px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes shimmer {
        from {
            background-position: 200% 0;
        }
        to {
            background-position: -200% 0;
        }
    }

    @keyframes pulse-glow {
        0%,
        100% {
            opacity: 0.6;
            transform: scale(1);
        }
        50% {
            opacity: 1;
            transform: scale(1.15);
        }
    }

    @media (max-width: 640px) {
        .page {
            padding: 20px 16px 40px;
        }
        .timer-display {
            font-size: 40px;
        }
        .session-row {
            grid-template-columns: 32px 1fr auto;
        }
        .session-row .stat-col:last-child {
            display: none;
        }
    }
</style>
